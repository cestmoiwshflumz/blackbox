# src/game/atom.py

from typing import Tuple
from src.utils.log_instances import atom_logger as logging


class Atom:
    """
    Represents an atom in the Black Box game.

    This class manages the state and position of an atom on the game board,
    and provides methods to interact with it.

    Attributes:
        x (int): The x-coordinate of the atom on the game board.
        y (int): The y-coordinate of the atom on the game board.
        is_revealed (bool): Whether the atom has been revealed or not.
    """

    def __init__(self, x: int, y: int):
        """
        Initialize an Atom instance.

        Args:
            x (int): The initial x-coordinate of the atom.
            y (int): The initial y-coordinate of the atom.

        Raises:
            ValueError: If x or y is negative.
        """
        if x < 0 or y < 0:
            raise ValueError("Atom coordinates must be non-negative.")

        self.x: int = x
        self.y: int = y
        self.is_revealed: bool = False
        logging.info(f"Atom created at position ({x}, {y})")

    def reveal(self) -> None:
        """Reveal the atom."""
        self.is_revealed = True
        logging.info(f"Atom at ({self.x}, {self.y}) revealed")

    def hide(self) -> None:
        """Hide the atom."""
        self.is_revealed = False
        logging.info(f"Atom at ({self.x}, {self.y}) hidden")

    def get_position(self) -> Tuple[int, int]:
        """
        Get the current position of the atom.

        Returns:
            Tuple[int, int]: The (x, y) coordinates of the atom.
        """
        return (self.x, self.y)

    def set_position(self, x: int, y: int) -> None:
        """
        Set a new position for the atom.

        Args:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.

        Raises:
            ValueError: If x or y is negative.
        """
        if x < 0 or y < 0:
            raise ValueError("Atom coordinates must be non-negative.")

        self.x = x
        self.y = y
        logging.info(f"Atom position updated to ({x}, {y})")

    def is_adjacent(self, x: int, y: int) -> bool:
        """
        Check if a given point is diagonally adjacent to the atom.

        Args:
            x (int): The x-coordinate of the point to check.
            y (int): The y-coordinate of the point to check.

        Returns:
            bool: True if the point is diagonally adjacent, False otherwise.

        Raises:
            ValueError: If x or y is negative.
        """
        if x < 0 or y < 0:
            raise ValueError("Coordinates must be non-negative.")

        return abs(self.x - x) == 1 and abs(self.y - y) == 1

    def is_hit(self, x: int, y: int) -> bool:
        """
        Check if a given point directly hits the atom.

        Args:
            x (int): The x-coordinate of the point to check.
            y (int): The y-coordinate of the point to check.

        Returns:
            bool: True if the point directly hits the atom, False otherwise.

        Raises:
            ValueError: If x or y is negative.
        """
        if x < 0 or y < 0:
            raise ValueError("Coordinates must be non-negative.")

        return self.x == x and self.y == y

    def __str__(self) -> str:
        """
        Return a string representation of the Atom.

        Returns:
            str: A string describing the atom's position and state.
        """
        state = "revealed" if self.is_revealed else "hidden"
        return f"Atom at ({self.x}, {self.y}), {state}"

    def __repr__(self) -> str:
        """
        Return a string representation of the Atom for debugging.

        Returns:
            str: A string representation of the Atom instance.
        """
        return f"Atom(x={self.x}, y={self.y}, is_revealed={self.is_revealed})"


# test and usecases
if __name__ == "__main__":
    try:
        # Create an Atom instance
        atom = Atom(3, 3)
        logging.info("Atom created successfully")
        logging.info(f"Atom position: {atom.get_position()}")

        # Test reveal and hide methods
        atom.reveal()
        logging.info(f"Is atom revealed? {atom.is_revealed()}")
        atom.hide()
        logging.info(f"Is atom revealed after hiding? {atom.is_revealed()}")

        # Test is_adjacent method
        logging.info(f"Is (2, 3) adjacent? {atom.is_adjacent(2, 3)}")
        logging.info(f"Is (4, 4) adjacent? {atom.is_adjacent(4, 4)}")

        # Test hit method
        logging.info(f"Does (3, 3) hit the atom? {atom.hit(3, 3)}")
        logging.info(f"Does (2, 2) hit the atom? {atom.hit(2, 2)}")

        # Test set_position method
        atom.set_position(5, 5)
        logging.info(f"New atom position: {atom.get_position()}")

        # Test error handling for negative coordinates
        try:
            Atom(-1, 2)
        except ValueError as e:
            logging.error(f"Error: {e}")

        try:
            atom.set_position(2, -1)
        except ValueError as e:
            logging.error(f"Error: {e}")

        # Test edge cases
        edge_atom = Atom(0, 0)
        logging.info(f"Edge atom position: {edge_atom.get_position()}")
        logging.info(f"Is (0, 1) adjacent to edge atom? {edge_atom.is_adjacent(0, 1)}")
        logging.info(f"Is (1, 1) adjacent to edge atom? {edge_atom.is_adjacent(1, 1)}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
