# src/game/atom.py


class Atom:
    def __init__(self, x: int, y: int):
        """
        Initialize an Atom object.

        Args:
            x (int): The x-coordinate of the atom on the game board.
            y (int): The y-coordinate of the atom on the game board.
        """
        self.x = x
        self.y = y
        self.is_revealed = False

    def position(self) -> tuple[int, int]:
        """
        Get the position of the atom.

        Returns:
            tuple[int, int]: A tuple containing the x and y coordinates of the atom.
        """
        return (self.x, self.y)

    def reveal(self) -> None:
        """
        Reveal the atom, typically when it's correctly guessed by a player.
        """
        self.is_revealed = True

    def is_adjacent(self, x: int, y: int) -> bool:
        """
        Check if the given coordinates are adjacent to the atom.

        Args:
            x (int): The x-coordinate to check.
            y (int): The y-coordinate to check.

        Returns:
            bool: True if the coordinates are adjacent (including diagonally), False otherwise.
        """
        return (abs(self.x - x) <= 1) and (abs(self.y - y) <= 1)

    def is_directly_adjacent(self, x: int, y: int) -> bool:
        """
        Check if the given coordinates are directly adjacent (not diagonally) to the atom.

        Args:
            x (int): The x-coordinate to check.
            y (int): The y-coordinate to check.

        Returns:
            bool: True if the coordinates are directly adjacent, False otherwise.
        """
        return (abs(self.x - x) + abs(self.y - y)) == 1

    def __eq__(self, other: object) -> bool:
        """
        Check if this atom is equal to another atom (same position).

        Args:
            other (object): The other atom to compare with.

        Returns:
            bool: True if the atoms have the same position, False otherwise.
        """
        if not isinstance(other, Atom):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        """
        Return a string representation of the Atom.

        Returns:
            str: A string representing the Atom object.
        """
        return f"Atom(x={self.x}, y={self.y}, revealed={self.is_revealed})"
