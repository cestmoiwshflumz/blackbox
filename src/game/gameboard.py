# src/game/gameboard.py

import random
from typing import List, Tuple, Optional


from src.utils.constants import DEFAULT_GRID_SIZE
from src.utils.log_instances import gameboard_logger as logging
from src.game.atom import Atom


class GameBoard:
    """
    Represents the game board for the Black Box game.

    This class manages the grid, atom placement, and provides methods to interact
    with the game board state.

    Attributes:
        size (int): The size of the grid (size x size).
        difficulty (str): The difficulty level of the game ('easy', 'medium', or 'hard').
        grid (List[List[Optional[Atom]]]): The 2D grid representing the game board.
        atoms (List[Atom]): List of atom positions on the board.
        edge_markers (List[int]): List of numbers for edge markers.
    """

    def __init__(self, difficulty: str, mp: bool = False):
        """
        Initialize the GameBoard.

        Args:
            size (int): The size of the grid. Defaults to 8.
            difficulty (str): The difficulty level. Defaults to 'medium'.

        Raises:
            ValueError: If the size is less than 4 or the difficulty is invalid.
        """

        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError(
                "Invalid difficulty level. Choose 'easy', 'medium', or 'hard'"
            )

        self.difficulty = difficulty
        self.size = 8 if difficulty == "medium" else 10 if difficulty == "hard" else 6

        logging.debug(
            f"Initializing game board with size {self.size} and difficulty {self.difficulty}"
        )

        self.grid: List[List[Optional[Atom]]] = [
            [None for _ in range(self.size)] for _ in range(self.size)
        ]
        self.atoms: List[Atom] = []
        self.edge_markers: List[int] = list(range(1, 4 * self.size + 1))

        self._initialize_grid()
        if not mp:
            self._place_atoms()

    def _initialize_grid(self) -> None:
        """Initialize the empty grid."""
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]

    def _place_atoms(self) -> None:
        """
        Place atoms on the grid based on the difficulty level.

        The number of atoms placed depends on the difficulty:
        - Easy: 3-4 atoms
        - Medium: 4-5 atoms
        - Hard: 5-6 atoms
        """
        num_atoms = {
            "easy": random.randint(3, 4),
            "medium": random.randint(4, 5),
            "hard": random.randint(5, 6),
        }[self.difficulty]

        while len(self.atoms) < num_atoms:
            x = random.randint(1, self.size - 2)
            y = random.randint(1, self.size - 2)
            if self.grid[y][x] is None:
                atom = Atom(x, y)
                self.atoms.append(atom)
                self.grid[y][x] = atom

    def set_cell(self, x: int, y: int, value: Optional[Atom]) -> None:
        """
        Set the content of a cell on the grid.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
            value (Optional[Atom]): The value to set in the cell (Atom or None for empty).
        """
        if value is not None:
            self.grid[y][x] = value
            self.place_atom(value)

    def place_atom(self, atom: Atom) -> None:
        """
        Place an atom on the grid.

        Args:
            atom (Atom): The Atom object to place on the grid.
        """
        if self.grid[atom.x][atom.y] is None:
            self.atoms.append(atom)

    def is_empty(self, x: int, y: int) -> bool:
        """
        Check if a cell is empty.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            bool: True if the cell is empty, False otherwise.

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        self._validate_coordinates(x, y)
        return self.grid[y][x] is None

    def has_atom(self, x: int, y: int) -> bool:
        """
        Check if a cell contains an atom.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            bool: True if the cell contains an atom, False otherwise.

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        self._validate_coordinates(x, y)
        return isinstance(self.grid[y][x], Atom)

    def is_edge(self, x: int, y: int) -> bool:
        """
        Check if a cell is on the edge of the grid.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            bool: True if the cell is on the edge, False otherwise.

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        self._validate_coordinates(x, y)
        return x == -1 or x == self.size or y == -1 or y == self.size

    def get_cell(self, x: int, y: int) -> Optional[Atom]:
        """
        Get the content of a cell.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            Optional[Atom]: The content of the cell (None if empty, 'A' if atom).

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        self._validate_coordinates(x, y)
        return self.grid[y][x]

    def get_atom(self, x: int, y: int) -> Optional[Atom]:
        """
        Get the atom at the specified coordinates.

        Args:
            x (int): The x-coordinate of the atom.
            y (int): The y-coordinate of the atom.

        Returns:
            Optional[Atom]: The Atom object at the specified coordinates.
        """
        return next((atom for atom in self.atoms if atom.x == x and atom.y == y), None)

    def set_cell(self, value: Atom) -> None:
        """
        Set the content of a cell.

        Args:
            value (Atom): The value to set in the cell (Atom).

        Raises:
            ValueError: If the coordinates are out of bounds or the value is invalid.
        """
        self._validate_coordinates(value.x, value.y)
        if value is not None and not isinstance(value, Atom):
            raise ValueError(
                "Invalid cell value. Use None for empty or an Atom instance."
            )
        self.grid[value.y][value.x] = value

    def all_atoms_guessed(self, guessed_atoms: List[Atom]) -> bool:
        """
        Check if all atoms have been correctly guessed.

        Args:
            guessed_atoms (List[Tuple[int, int]]): List of guessed atom positions.

        Returns:
            bool: True if all atoms have been guessed correctly, False otherwise.
        """
        return set(self.atoms) == set(guessed_atoms)

    def get_board_state(self) -> List[List[Optional[Atom]]]:
        """
        Get the current state of the board.

        Returns:
            List[List[Optional[Atom]]]: A deep copy of the current grid.
        """
        return [row[:] for row in self.grid]

    def _validate_coordinates(self, x: int, y: int) -> None:
        """
        Validate that the given coordinates are within the grid bounds.

        Args:
            x (int): The x-coordinate to validate.
            y (int): The y-coordinate to validate.

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        if not (-1 <= x <= self.size and -1 <= y <= self.size):
            raise ValueError(
                f"Coordinates ({x}, {y}) are out of bounds for a {self.size}x{self.size} grid."
            )

    def __str__(self) -> str:
        """
        Return a string representation of the game board.

        Returns:
            str: A formatted string representing the current state of the game board.
        """
        board_str = "  " + " ".join(f"{i:2}" for i in range(self.size)) + "\n"
        for y in range(self.size):
            board_str += (
                f"{y:2} "
                + " ".join(
                    "A" if isinstance(cell, Atom) else "·" for cell in self.grid[y]
                )
                + "\n"
            )
        return board_str


# Example usage and testing
if __name__ == "__main__":
    try:
        board = GameBoard(size=8, difficulty="medium")
        logging.info("Game board created successfully")
        logging.info(f"Board state:\n{board}")

        # Test some methods
        logging.info(f"Is (0, 0) empty? {board.is_empty(0, 0)}")
        logging.info(f"Is (0, 0) on edge? {board.is_edge(0, 0)}")

        # Place an atom for testing
        test_atom_x, test_atom_y = 3, 3
        board.set_cell(test_atom_x, test_atom_y, "A")
        logging.info(f"Placed test atom at ({test_atom_x}, {test_atom_y})")

        logging.info(
            f"Is ({test_atom_x}, {test_atom_y}) empty? {board.is_empty(test_atom_x, test_atom_y)}"
        )
        logging.info(
            f"Has atom at ({test_atom_x}, {test_atom_y})? {board.has_atom(test_atom_x, test_atom_y)}"
        )

        # Test error handling
        try:
            board.get_cell(10, 10)
        except ValueError as e:
            logging.error(f"Error: {e}")

        # Test all_atoms_guessed method
        all_atoms = board.atoms + [(test_atom_x, test_atom_y)]
        logging.info(
            f"All atoms guessed correctly? {board.all_atoms_guessed(all_atoms)}"
        )

        # Display final board state
        logging.info("Final board state:")
        logging.info(f"\n{board}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
