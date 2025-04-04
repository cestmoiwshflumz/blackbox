# src/gameloop.py

import pygame
from typing import Optional
import yaml
from typing import Union, List

from src.ui.window import Window
from src.ui.menu import run_menu
from src.ui.gamescreen_solo import GameScreen
from src.ui.gamescreen_mp import GameScreenMP
from src.game.gameboard import GameBoard
from src.game.player import Player
from src.utils.log_instances import game_logger
from src.utils.constants import COLOR_WHITE


class GameLoop:
    """
    Manages the main game loop and game state transitions.

    This class is responsible for initializing the game, handling state transitions,
    and managing the overall flow of the game.

    Attributes:
        logger: The logger instance for logging game events.
        window (Window): The game window instance.
        game_state (str): The current state of the game.
        clock (pygame.time.Clock): The game clock for controlling frame rate.
        game_board (Optional[GameBoard]): The current game board instance.
        player (Optional[Player]): The current player instance.
        game_screen (Optional[GameScreen]): The current game screen instance.
    """

    def __init__(self):
        """Initialize the GameLoop instance."""
        self.logger = game_logger
        self.config = self._load_config("config/config.yaml")
        self.window: Window = Window()
        self.game_state: str = "MAIN_MENU"
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.game_board: Optional[GameBoard] = None
        self.player: Optional[Player] = None
        self.game_screen: Union[Optional[GameScreen] | Optional[GameScreenMP]] = None
        self.logger.info("GameLoop initialized")
        self.difficulty = (
            "hard"
            if self.config["options"]["difficulty"] == 1
            else "medium" if self.config["options"]["difficulty"] == 0 else "easy"
        )
        self.bo5 = [0, 0]
        self.logger.info(f"Game difficulty set to: {self.difficulty}")

    def _load_config(self, config_path: str) -> dict:
        """
        Load and validate the configuration from a YAML file.

        Args:
            config_path (str): The path to the configuration file.

        Returns:
            dict: The loaded configuration dictionary.
        """
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            # Validate required config keys
            required_keys = ["options.difficulty", "options.sound", "options.debug"]
            for key in required_keys:
                if self._nested_get(config, key.split(".")) is None:
                    raise ValueError(f"Missing required config key: {key}")
            self.logger.info("Menu configuration loaded and validated")
            return config
        except Exception as e:
            self.logger.error(
                f"Failed to load or validate menu configuration: {e}", exc_info=True
            )
            # Return a default configuration
            return {"options": {"difficulty": 0, "sound": True, "debug": False}}

    def _nested_get(self, d: dict, keys: list) -> Union[dict, None]:
        """
        Get a nested value from a dictionary using a list of keys.

        Args:
            d (dict): The dictionary to search.
            keys (list): The list of keys representing the path to the desired value.

        Returns:
            Any: The value at the specified nested location, or None if not found.
        """
        for key in keys:
            d = d.get(key)
            if d is None:
                return None
        return d

    def _refresh_config(self) -> None:
        """
        Refresh the game configuration based on the current settings.
        """
        self.config = self._load_config("config/config.yaml")
        self.difficulty = (
            "hard"
            if self.config["options"]["difficulty"] == 1
            else "medium" if self.config["options"]["difficulty"] == 0 else "easy"
        )

    def run(self) -> None:
        """
        Run the main game loop.

        This method handles the game state transitions and calls the appropriate
        methods based on the current game state.
        """
        self.logger.info("Starting game loop")
        while True:
            try:
                if self.game_state == "MAIN_MENU":
                    self.game_state = run_menu(self.window)
                elif self.game_state == "START_GAME":
                    self.start_new_game()
                elif self.game_state == "MULTIPLAYER":
                    self.start_new_game_mp(self.bo5)
                elif self.game_state == "PLAYING":
                    self.play_game()
                elif self.game_state == "GAME_OVER":
                    self.show_game_over()
                elif self.game_state == "PLAYING_MP":
                    self.play_game_mp()
                elif self.game_state == "GAME_OVER_MP":
                    self.show_game_over_mp()
                elif self.game_state == "QUIT":
                    self.quit_game()
                    break
                else:
                    self.logger.error(f"Unknown game state: {self.game_state}")
                    self.game_state = "MAIN_MENU"

                self.clock.tick(60)  # Limit the frame rate to 60 FPS
            except Exception as e:
                self.logger.error(
                    f"An error occurred in the game loop: {e}", exc_info=True
                )
                self.game_state = "MAIN_MENU"

    def start_new_game(self) -> None:
        """
        Start a new game by initializing the game board, player, and game screen.
        """
        try:
            self.logger.info("Starting new game")
            self._refresh_config()
            self.game_board = GameBoard(self.difficulty)
            self.player = Player("Player 1", self.game_board)
            self.game_screen = GameScreen(self.window, self.game_board, self.player)
            self.game_state = "PLAYING"
        except Exception as e:
            self.logger.error(f"Error starting new game: {e}", exc_info=True)
            self.game_state = "MAIN_MENU"

    def start_new_game_mp(self, bo5: List[int]) -> None:
        """
        Start a new multiplayer game by initializing the game boards, players, and game screen.
        """
        try:
            self.logger.info("Starting new multiplayer game")
            self._refresh_config()
            self.game_board1 = GameBoard(self.difficulty, mp=True)
            self.game_board2 = GameBoard(self.difficulty, mp=True)
            self.player1 = Player("Player 1", self.game_board1)
            self.player2 = Player("Player 2", self.game_board2)
            self.game_screen = GameScreenMP(
                self.window,
                self.game_board1,
                self.game_board2,
                self.player1,
                self.player2,
                bo5,
            )
            waiting = True
            while waiting:
                atoms = self.game_screen.place_atoms()
                if atoms:
                    waiting = False
            self.game_state = "PLAYING_MP"
        except Exception as e:
            self.logger.error(
                f"Error starting new multiplayer game: {e}", exc_info=True
            )
            self.game_state = "MAIN_MENU"

    def play_game(self) -> None:
        """
        Handle the main gameplay loop, including drawing the game screen and processing input.
        """
        try:
            if self.game_screen is None:
                raise ValueError("Game screen is not initialized")

            self.game_screen.draw()
            action = self.game_screen.handle_input()

            if action == "QUIT":
                self.game_state = "QUIT"
            elif action == "MAIN_MENU":
                self.game_state = "MAIN_MENU"
            elif self.check_game_over():
                self.game_state = "GAME_OVER"
        except Exception as e:
            self.logger.error(f"Error during gameplay: {e}", exc_info=True)
            self.game_state = "MAIN_MENU"

    def play_game_mp(self) -> None:
        """
        Handle the main multiplayer gameplay loop, including drawing the game screen and processing input.
        """
        try:
            if self.game_screen is None:
                raise ValueError("Game screen is not initialized")

            self.game_screen.draw()
            action = self.game_screen.handle_input()

            if action == "QUIT":
                self.game_state = "QUIT"
            elif action == "MAIN_MENU":
                self.game_state = "MAIN_MENU"
            elif self.check_game_over_mp():
                self.game_state = "GAME_OVER_MP"
        except Exception as e:
            self.logger.error(f"Error during multiplayer gameplay: {e}", exc_info=True)
            self.game_state = "MAIN_MENU"

    def check_game_over(self) -> bool:
        """
        Check if the game is over based on the player's score and guessed atoms.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        try:
            if self.player is None or self.game_board is None:
                raise ValueError("Player or game board is not initialized")

            if self.player.get_score() <= 0:
                self.logger.info("Game over: Player ran out of points")
                return True
            if self.game_board.all_atoms_guessed(self.player.get_guessed_atoms()):
                self.logger.info("Game over: All atoms guessed correctly")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error checking game over condition: {e}")
            return True

    def check_game_over_mp(self) -> bool:
        """
        Check if the multiplayer game is over based on the player's score and guessed atoms.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        try:
            if self.player1 is None or self.game_board1 is None:
                raise ValueError("Player or game board is not initialized")

            if self.player1.get_score() <= 0:
                self.bo5[1] += 1
                self.logger.info("Game over: Player 1 ran out of points")
                return True
            if self.game_board2.all_atoms_guessed(self.player1.get_guessed_atoms()):
                self.bo5[0] += 1
                self.logger.info("Game over: All atoms guessed correctly by Player 1")
                return True
            if self.player2.get_score() <= 0:
                self.bo5[0] += 1
                self.logger.info("Game over: Player 2 ran out of points")
                return True
            if self.game_board1.all_atoms_guessed(self.player2.get_guessed_atoms()):
                self.bo5[1] += 1
                self.logger.info("Game over: All atoms guessed correctly by Player 2")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error checking multiplayer game over condition: {e}")
            return True

    def show_game_over(self) -> None:
        """
        Display the game over screen and handle input for returning to the main menu.
        """
        try:
            self.window.clear()

            if self.player.get_score() <= 0:
                self.game_screen.show_game_over()
            else:
                self.game_screen.show_game_finished()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_state = "QUIT"
                        waiting = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game_state = "MAIN_MENU"
                        waiting = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = "START_GAME"
                        waiting = False
        except Exception as e:
            self.logger.error(f"Error displaying game over screen: {e}")
            self.game_state = "MAIN_MENU"

    def show_game_over_mp(self) -> None:
        """
        Display the multiplayer game over screen and handle input for returning to the main menu.
        """
        try:
            self.window.clear()

            if self.bo5[0] == 3:
                self.game_screen.show_game_finished("Player 1")
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.game_state = "QUIT"
                            waiting = False
                        elif (
                            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                        ):
                            self.game_state = "MAIN_MENU"
                            waiting = False
            elif self.bo5[1] == 3:
                self.game_screen.show_game_finished("Player 2")
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.game_state = "QUIT"
                            waiting = False
                        elif (
                            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                        ):
                            self.game_state = "MAIN_MENU"
                            waiting = False
            else:
                if self.player1.get_score() <= 0 or self.player2.get_score() <= 0:
                    self.game_screen.show_game_over()
                elif self.game_board2.all_atoms_guessed(
                    self.player1.get_guessed_atoms()
                ) or self.game_board1.all_atoms_guessed(
                    self.player2.get_guessed_atoms()
                ):
                    self.game_screen.show_game_over()

                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.game_state = "QUIT"
                            waiting = False
                        elif (
                            event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                        ):
                            self.game_state = "MULTIPLAYER"
                            waiting = False
        except Exception as e:
            self.logger.error(f"Error displaying multiplayer game over screen: {e}")
            self.game_state = "MAIN_MENU"

    def show_game_finished(self) -> None:
        """
        Display the game finished screen.

        This method shows the final score and a message indicating the end of the game.
        """
        try:
            self.window.clear()
            font = pygame.font.Font(None, 36)
            game_finished_text = font.render(
                "Game Finished, Press Space to go to main menu.", True, COLOR_WHITE
            )
            score_text = font.render(
                f"Final Score: {self.player.get_score()}", True, COLOR_WHITE
            )

            self.window.get_screen().blit(
                game_finished_text,
                (
                    self.window.width // 2 - game_finished_text.get_width() // 2,
                    self.window.height // 2 - 50,
                ),
            )
            self.window.get_screen().blit(
                score_text,
                (
                    self.window.width // 2 - score_text.get_width() // 2,
                    self.window.height // 2 + 50,
                ),
            )

            self.window.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_state = "QUIT"
                        waiting = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.game_state = "MAIN_MENU"
                        waiting = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = "START_GAME"
                        waiting = False
        except Exception as e:
            self.logger.error(f"Error displaying game over screen: {e}")
            self.game_state = "MAIN_MENU"

    def quit_game(self) -> None:
        """
        Perform cleanup operations and quit the game.
        """
        try:
            self.logger.info("Quitting game")
            self.window.quit()
        except Exception as e:
            self.logger.error(f"Error quitting game: {e}")


if __name__ == "__main__":
    game = GameLoop()
    game.run()
