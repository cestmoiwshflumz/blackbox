# src/ui/gamescreen_mp.py

import pygame
from typing import List, Tuple, Optional, Union
import yaml

from src.ui.window import Window
from src.game.gameboard import GameBoard
from src.game.player import Player
from src.game.ray import Ray
from src.game.atom import Atom
from src.utils.constants import (
    COLOR_WHITE,
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
)
from src.utils.log_instances import game_logger as logging


class GameScreenMP:
    """
    Represents the game screen for the Black Box game in multiplayer mode.

    This class manages the game loop, player interactions, and rendering of the game screen.

    Attributes:
        window (Window): The game window.
        game_board (GameBoard): The game board.
        players (List[Player]): List of players in the game.
        current_player (Player): The current player.
        cell_size (int): The size of each cell on the game board.
        board_offset (Tuple[int, int]): The offset of the game board on the screen.
        font (pygame.font.Font): The font used for rendering text.
        history (bool): Whether to show the history of rays or not.
    """

    def __init__(
        self,
        window: Window,
        game_board1: GameBoard,
        game_board2: GameBoard,
        player1: Player,
        player2: Player,
    ):
        """
        Initialize the GameScreen.

        Args:
            window (Window): The game window.
            game_board1 (GameBoard): The game board for player 1.
            game_board2 (GameBoard): The game board for player 2.
            player1 (Player): Player 1.
            player2 (Player): Player 2.

        Raises:
            ValueError: If the window, game_board, or player is None.
        """
        if not all([window, game_board1, game_board2, player1, player2]):
            raise ValueError("Window, game_boards, and players must not be None")

        self.window = window
        self.game_board1 = game_board1
        self.game_board2 = game_board2
        self.players = [player1, player2]
        self.current_player = player1
        self.cell_size = min(window.width, window.height) // (game_board1.size + 2)
        self.board_offset = (
            (window.width - self.cell_size * game_board1.size) // 2,
            (window.height - self.cell_size * game_board1.size) // 2,
        )
        self.font = pygame.font.Font(None, 24)
        self.history = False

        # Load and validate the game configuration
        self.config = self._load_config("config/config.yaml")

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
            logging.info("Menu configuration loaded and validated")
            return config
        except Exception as e:
            logging.error(
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

    def draw_debug(self) -> None:
        """
        Draw the entire game screen with debug option enabled which allow user to see all the rays and atoms.

        This method clears the screen, draws the grid, rays, guesses, and score,
        then updates the display.
        """
        try:
            if self.current_player == self.players[0]:
                self.window.clear()
                self.draw_grid()
                self.draw_atoms(self.game_board1.atoms)
                if not self.history:
                    self.draw_Active_rays_debug()
                    self.draw_current_guess()
                else:
                    self.draw_all_rays_debug()
                    self.draw_all_guesses()
                self.draw_guesses()
                self.draw_score()
                self.draw_buttons()
                self.window.update()
            else:
                self.window.clear()
                self.draw_grid()
                self.draw_atoms(self.game_board2.atoms)
                if not self.history:
                    self.draw_Active_rays_debug()
                    self.draw_current_guess()
                else:
                    self.draw_all_rays_debug()
                    self.draw_all_guesses()
                self.draw_guesses()
                self.draw_score()
                self.draw_buttons()
                self.window.update()
        except pygame.error as e:
            logging.error(f"Error drawing game screen: {e}")

    def draw_normal(self) -> None:
        """
        Draw the entire game screen to actually play the game.

        This method clears the screen, draws the grid, rays, guesses, and score,
        then updates the display.
        """
        try:
            self.window.clear()
            self.draw_grid()
            if not self.history:
                self.draw_active_rays_normal()
                self.draw_current_guess()
            else:
                self.draw_all_rays_normal()
                self.draw_all_guesses()
            self.draw_guesses()
            self.draw_score()
            self.draw_buttons()
            self.window.update()
        except pygame.error as e:
            logging.error(f"Error drawing game screen: {e}")

    def draw(self) -> None:
        """
        Draw the entire game screen based on the current debug option.
        """
        if self.config["options"]["debug"]:
            self.draw_debug()
        else:
            self.draw_normal()

    def draw_grid(self) -> None:
        """
        Draw the game grid on the screen.

        This method draws both vertical and horizontal lines to create the game grid.
        """
        try:
            for i in range(self.game_board1.size + 1):
                start_x = self.board_offset[0] + i * self.cell_size
                start_y = self.board_offset[1]
                end_x = start_x
                end_y = start_y + self.game_board1.size * self.cell_size
                self.window.draw_line(COLOR_WHITE, (start_x, start_y), (end_x, end_y))

                start_x = self.board_offset[0]
                start_y = self.board_offset[1] + i * self.cell_size
                end_x = start_x + self.game_board1.size * self.cell_size
                end_y = start_y
                self.window.draw_line(COLOR_WHITE, (start_x, start_y), (end_x, end_y))
        except pygame.error as e:
            logging.error(f"Error drawing grid: {e}")

    def draw_atoms(self, atoms: List[Atom]) -> None:
        """
        Draw atoms on the game screen.

        Args:
            atoms (List[Atom]): The list of atoms to draw.
        """
        try:
            for atom in atoms:
                pos = self.get_screen_position(atom.get_position())
                self.window.draw_circle(COLOR_BLUE, pos, self.cell_size // 4)
        except pygame.error as e:
            logging.error(f"Error drawing atoms: {e}")

    def get_screen_position(self, board_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Convert a board position to screen coordinates.

        Args:
            board_pos (Tuple[int, int]): The position on the game board.

        Returns:
            Tuple[int, int]: The corresponding position on the screen.
        """
        return (
            self.board_offset[0] + board_pos[0] * self.cell_size + self.cell_size // 2,
            self.board_offset[1] + board_pos[1] * self.cell_size + self.cell_size // 2,
        )

    def get_board_position(self, screen_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Convert screen coordinates to a board position.

        Args:
            screen_pos (Tuple[int, int]): The position on the screen.

        Returns:
            Tuple[int, int]: The corresponding position on the game board.
        """
        return (
            (screen_pos[0] - self.board_offset[0]) // self.cell_size,
            (screen_pos[1] - self.board_offset[1]) // self.cell_size,
        )
