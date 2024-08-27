# src/gameloop.py

import pygame
from typing import Optional
import yaml
from typing import Union

from src.ui.window import Window
from src.ui.menu import run_menu
from src.ui.gamescreen import GameScreen
from src.game.gameboard import GameBoard
from src.game.player import Player
from src.utils.log_instances import game_logger
from src.utils.constants import DEFAULT_GRID_SIZE, DEFAULT_DIFFICULTY


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
        self.game_screen: Optional[GameScreen] = None
        self.logger.info("GameLoop initialized")
        self.difficulty = (
            "hard"
            if self.config["options"]["difficulty"] == 1
            else "medium" if self.config["options"]["difficulty"] == 0 else "easy"
        )
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
                elif self.game_state == "PLAYING":
                    self.play_game()
                elif self.game_state == "GAME_OVER":
                    self.show_game_over()
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
            self.game_board = GameBoard(self.difficulty)
            self.player = Player("Player 1", self.game_board)
            self.game_screen = GameScreen(self.window, self.game_board, self.player)
            self.game_state = "PLAYING"
        except Exception as e:
            self.logger.error(f"Error starting new game: {e}", exc_info=True)
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

    def show_game_over(self) -> None:
        """
        Display the game over screen and handle input for returning to the main menu.
        """
        try:
            self.logger.info("Showing game over screen")
            font = pygame.font.Font(None, 36)
            text = font.render(
                "Game Over! Press SPACE to return to menu", True, (255, 255, 255)
            )
            text_rect = text.get_rect(
                center=(self.window.width // 2, self.window.height // 2)
            )
            self.window.get_screen().blit(text, text_rect)
            self.window.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_state = "QUIT"
                        waiting = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = "MAIN_MENU"
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
