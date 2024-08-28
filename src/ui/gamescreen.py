# src/ui/gamescreen.py

import pygame
from typing import List, Tuple, Optional, Union
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


class GameScreen:
    """
    Represents the game screen for the Black Box game.

    This class is responsible for rendering the game board, handling user input,
    and managing the visual representation of the game state.

    Attributes:
        window (Window): The game window.
        game_board (GameBoard): The game board.
        player (Player): The current player.
        cell_size (int): The size of each cell on the game board.
        board_offset (Tuple[int, int]): The offset of the board from the window edges.
        font (pygame.font.Font): The font used for rendering text.
    """

    def __init__(self, window: Window, game_board: GameBoard, player: Player):
        """
        Initialize the GameScreen.

        Args:
            window (Window): The game window.
            game_board (GameBoard): The game board.
            player (Player): The current player.

        Raises:
            ValueError: If the window, game_board, or player is None.
        """
        if not all([window, game_board, player]):
            raise ValueError("Window, game_board, and player must not be None")

        self.window = window
        self.game_board = game_board
        self.player = player
        self.cell_size = min(window.width, window.height) // (game_board.size + 2)
        self.board_offset = (
            (window.width - self.cell_size * game_board.size) // 2,
            (window.height - self.cell_size * game_board.size) // 2,
        )
        self.font = pygame.font.Font(None, 24)
        self.history = False

    def draw_debug(self) -> None:
        """
        Draw the entire game screen with debug option enabled which allow user to see all the rays and atoms.

        This method clears the screen, draws the grid, rays, guesses, and score,
        then updates the display.
        """
        try:
            self.window.clear()
            self.draw_grid()
            self.draw_atoms(self.game_board.atoms)
            self.draw_Active_rays()
            self.draw_guesses()
            self.draw_score()
            self.draw_buttons()
            self.window.update()
        except pygame.error as e:
            logging.error(f"Error drawing game screen: {e}")

    def draw(self) -> None:
        """
        Draw the entire game screen.

        This method clears the screen, draws the grid, rays, guesses, and score,
        then updates the display.
        """
        try:
            self.window.clear()
            self.draw_grid()
            self.draw_atoms(self.game_board.atoms)
            if not self.history:
                self.draw_Active_rays()
            else:
                self.draw_all_rays()
            self.draw_guesses()
            self.draw_score()
            self.draw_buttons()
            self.window.update()
        except pygame.error as e:
            logging.error(f"Error drawing game screen: {e}")

    def draw_grid(self) -> None:
        """
        Draw the game grid on the screen.

        This method draws both vertical and horizontal lines to create the game grid.
        """
        try:
            for i in range(self.game_board.size + 1):
                start_x = self.board_offset[0] + i * self.cell_size
                start_y = self.board_offset[1]
                end_x = start_x
                end_y = start_y + self.game_board.size * self.cell_size
                self.window.draw_line(COLOR_WHITE, (start_x, start_y), (end_x, end_y))

                start_x = self.board_offset[0]
                start_y = self.board_offset[1] + i * self.cell_size
                end_x = start_x + self.game_board.size * self.cell_size
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

    def draw_Active_rays(self) -> None:
        """
        Draw fired rays of the current turn on the game screen.

        This method iterates through all fired rays of the current turn and draws them on the screen.
        """
        for ray in self.player.get_active_turn_rays():
            self.draw_ray(ray)

        for guess in self.player.get_active_turn_guesses():
            self.draw_guess(guess)

    def draw_all_rays(self) -> None:
        """
        Draw all rays fired on the game screen.

        This method iterates through all fired rays and draws them on the screen.
        """
        for ray in self.player.get_fired_rays():
            self.draw_ray(ray)

    def draw_ray(self, ray: Ray) -> None:
        """
        Draw a single ray on the game screen.

        Args:
            ray (Ray): The ray to be drawn.
        """
        if self.check_ray_detoured(ray):
            pass
        try:
            color = COLOR_RED if ray.exit_point is None else COLOR_GREEN
            for i in range(len(ray.path) - 1):
                start = self.get_screen_position(ray.path[i])
                end = self.get_screen_position(ray.path[i + 1])
                self.window.draw_line(color, start, end, 2)
        except pygame.error as e:
            logging.error(f"Error drawing ray: {e}", exc_info=True)

    def draw_guesses(self) -> None:
        """
        Draw all guessed atom positions on the game screen.

        This method iterates through all guessed atoms and draws them on the screen.
        """
        try:
            for guess in self.player.get_guesses():
                pos = self.get_screen_position(guess)
                self.window.draw_circle(COLOR_GREEN, pos, self.cell_size // 4)
        except pygame.error as e:
            logging.error(f"Error drawing guesses: {e}", exc_info=True)

    def draw_current_guess(self) -> None:
        """
        Draw the current guessed atom position on the game screen.
        """
        try:
            pos = self.get_screen_position(self.player.get_active_turn_guesses())
            self.window.draw_circle(COLOR_BLUE, pos, self.cell_size // 4)
        except pygame.error as e:
            logging.error(f"Error drawing current guess: {e}", exc_info=True)

    def draw_all_guesses(self) -> None:
        """
        Draw all guessed atom positions on the game screen.

        This method iterates through all guessed atoms and draws them on the screen.
        """
        try:
            for guess in self.player.get_guesses():
                pos = self.get_screen_position(guess)
                self.window.draw_circle(COLOR_BLUE, pos, self.cell_size // 4)
        except pygame.error as e:
            logging.error(f"Error drawing guesses: {e}", exc_info=True)

    def draw_score(self) -> None:
        """
        Draw the current player's score on the game screen.
        """
        try:
            score_text = f"Score: {self.player.get_score()}"
            text_surface = self.font.render(score_text, True, COLOR_WHITE)
            self.window.get_screen().blit(text_surface, (10, 10))
        except pygame.error as e:
            logging.error(f"Error drawing score: {e}", exc_info=True)

    def draw_button(
        self,
        text: str,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        color: Tuple[int, int, int],
    ) -> None:
        """
        Draw a button on the game screen.

        Args:
            text (str): The text to display on the button.
            pos (Tuple[int, int]): The position of the button on the screen.
            size (Tuple[int, int]): The size of the button.
            color (Tuple[int, int, int]): The color of the button.
        """
        try:
            rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
            pygame.draw.rect(self.window.get_screen(), color, rect)
            text_surface = self.font.render(text, True, COLOR_WHITE)
            text_rect = text_surface.get_rect(center=rect.center)
            self.window.get_screen().blit(text_surface, text_rect)
        except pygame.error as e:
            logging.error(f"Error drawing button: {e}", exc_info=True)

    def draw_buttons(self) -> None:
        """
        Draw all buttons on the game screen.
        """
        self.draw_button("Next turn", (10, 100), (100, 40), COLOR_BLUE)
        self.draw_button("Show History", (10, 150), (100, 40), COLOR_BLUE)
        self.draw_button("Quit", (10, 200), (100, 40), COLOR_RED)

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

    def get_detour_positions(self, screen_pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Convert screen coordinates to a board position.

        Args:
            screen_pos (Tuple[int, int]): The position on the screen.

        Returns:
            Tuple[int, int]: The corresponding position on the game board.
        """
        return (
            (screen_pos[0] - self.board_offset[0]) // (self.cell_size // 2),
            (screen_pos[1] - self.board_offset[1]) // (self.cell_size // 2),
        )

    def check_ray_detoured(self, ray: Ray) -> bool:
        """
        Check if a ray has been detoured by atoms.

        Args:
            ray (Ray): The ray to check.

        Returns:
            bool: True if the ray has been detoured, False otherwise.
        """
        return ray.is_detoured

    def handle_draw_detour(self, ray: Ray) -> None:
        """
        Handle the drawing of a detoured ray.

        Args:
            ray (Ray): The detoured ray to draw.
        """
        color = COLOR_GREEN
        try:
            for i in range(len(ray.path) - 1):
                start = self.get_detour_positions(ray.path[i])
                end = self.get_detour_positions(ray.path[i + 1])
                self.window.draw_line(color, start, end, 2)
        except pygame.error as e:
            logging.error(f"Error drawing detoured ray: {e}", exc_info=True)
        except Exception as e:
            logging.error(f"Error handling detoured ray: {e}", exc_info=True)

    def handle_input(self) -> str:
        """
        Handle user input events.

        Returns:
            str: A string indicating the action to be taken ('QUIT', 'MAIN_MENU', or 'CONTINUE').
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    r = self.handle_left_click(event.pos)
                    if r:
                        return r
                elif event.button == 3:  # Right click
                    self.handle_right_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MAIN_MENU"
        return "CONTINUE"

    def handle_left_click(self, pos: Tuple[int, int]) -> Union[str, None]:
        """
        Handle left mouse click events.

        This method is responsible for firing rays when the player clicks on the edge of the board.

        Args:
            pos (Tuple[int, int]): The position of the mouse click on the screen.
        """
        # Handle clicks on the edge of the board
        try:
            board_pos = self.get_board_position(pos)
            if self.is_valid_ray_start(board_pos):
                direction = self.get_ray_direction(board_pos)
                if direction:
                    ray = self.player.fire_ray(board_pos[0], board_pos[1], direction)
                    self.draw()
        except ValueError as e:
            logging.error(f"Error handling left click: {e}", exc_info=True)

        # Handle clicks on the buttons
        try:
            if 10 <= pos[0] <= 110 and 100 <= pos[1] <= 140:
                self.player.refresh_turn()
            elif 10 <= pos[0] <= 110 and 150 <= pos[1] <= 190:
                self.history = not self.history
            elif 10 <= pos[0] <= 110 and 200 <= pos[1] <= 240:
                return "MAIN_MENU"
        except ValueError as e:
            logging.error(f"Error handling left click: {e}", exc_info=True)
        except Exception as e:
            logging.error(f"Error handling left click: {e}", exc_info=True)

    def handle_right_click(self, pos: Tuple[int, int]) -> None:
        """
        Handle right mouse click events.

        This method is responsible for placing or removing atom guesses when the player right-clicks on the board.

        Args:
            pos (Tuple[int, int]): The position of the mouse click on the screen.
        """
        try:
            board_pos = self.get_board_position(pos)
            if self.is_valid_guess_position(board_pos):
                self.player.guess_atom_position(board_pos)
                self.draw()
        except ValueError as e:
            logging.error(f"Error handling right click: {e}")

    def is_valid_ray_start(self, pos: Tuple[int, int]) -> bool:
        """
        Check if the given position is a valid starting point for a ray.

        Args:
            pos (Tuple[int, int]): The position to check.

        Returns:
            bool: True if the position is on the edge of the board, False otherwise.
        """
        x, y = pos
        return (
            x == -1 or x == self.game_board.size or y == -1 or y == self.game_board.size
        ) and not (
            (x == -1 and y == -1)
            or (x == -1 and y == self.game_board.size)
            or (x == self.game_board.size and y == -1)
            or (x == self.game_board.size and y == self.game_board.size)
        )

    def get_ray_direction(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Get the direction of a ray based on its starting position.

        Args:
            pos (Tuple[int, int]): The starting position of the ray.

        Returns:
            Optional[Tuple[int, int]]: The direction of the ray as (dx, dy), or None if invalid.
        """
        x, y = pos
        if x == -1:
            return (1, 0)
        elif x == self.game_board.size:
            return (-1, 0)
        elif y == -1:
            return (0, 1)
        elif y == self.game_board.size:
            return (0, -1)
        return None

    def is_valid_guess_position(self, pos: Tuple[int, int]) -> bool:
        """
        Check if the given position is a valid position for guessing an atom.

        Args:
            pos (Tuple[int, int]): The position to check.

        Returns:
            bool: True if the position is within the board and not on the edge, False otherwise.
        """
        x, y = pos
        return 0 <= x < self.game_board.size and 0 <= y < self.game_board.size

    def highlight_cell(self, pos: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Highlight a cell on the game board.

        Args:
            pos (Tuple[int, int]): The position of the cell to highlight.
            color (Tuple[int, int, int]): The color to use for highlighting.
        """
        try:
            screen_pos = self.get_screen_position(pos)
            rect = pygame.Rect(
                screen_pos[0], screen_pos[1], self.cell_size, self.cell_size
            )
            self.window.draw_rect(color, rect)
        except pygame.error as e:
            logging.error(f"Error highlighting cell: {e}")

    def show_game_over(self) -> None:
        """
        Display the game over screen.

        This method shows the final score and a message indicating the end of the game.
        """
        try:
            self.window.clear()
            game_over_text = self.font.render("Game Over", True, COLOR_WHITE)
            score_text = self.font.render(
                f"Final Score: {self.player.get_score()}", True, COLOR_WHITE
            )

            self.window.get_screen().blit(
                game_over_text,
                (
                    self.window.width // 2 - game_over_text.get_width() // 2,
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
            pygame.time.wait(3000)  # Wait for 3 seconds before returning to main menu
        except pygame.error as e:
            logging.error(f"Error showing game over screen: {e}")

    def update(self) -> None:
        """
        Update the game state and redraw the screen.

        This method should be called once per frame to keep the game display current.
        """
        try:
            self.draw()
            if self.game_board.all_atoms_guessed(self.player.get_guessed_atoms()):
                self.show_game_over()
        except Exception as e:
            logging.error(f"Error updating game screen: {e}")
