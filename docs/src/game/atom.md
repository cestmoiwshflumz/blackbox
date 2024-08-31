Module src.game.atom
====================

Classes
-------

`Atom(x: int, y: int)`
:   Represents an atom in the Black Box game.
    
    This class manages the state and position of an atom on the game board,
    and provides methods to interact with it.
    
    Attributes:
        x (int): The x-coordinate of the atom on the game board.
        y (int): The y-coordinate of the atom on the game board.
        is_revealed (bool): Whether the atom has been revealed or not.
    
    Initialize an Atom instance.
    
    Args:
        x (int): The initial x-coordinate of the atom.
        y (int): The initial y-coordinate of the atom.
    
    Raises:
        ValueError: If x or y is negative.

    ### Methods

    `get_position(self) ‑> Tuple[int, int]`
    :   Get the current position of the atom.
        
        Returns:
            Tuple[int, int]: The (x, y) coordinates of the atom.

    `hide(self) ‑> None`
    :   Hide the atom.

    `is_adjacent(self, x: int, y: int) ‑> Tuple[bool, int]`
    :   Check if a given point is diagonally adjacent to the atom and return the corner number.
        
        Args:
            x (int): The x-coordinate of the point to check.
            y (int): The y-coordinate of the point to check.
        
        Returns:
            Tuple[bool, int]: A tuple containing:
                - bool: True if the point is diagonally adjacent, False otherwise.
                - int: The corner number (1-4) if adjacent, 0 otherwise.
                    1: top-left, 2: top-right, 3: bottom-left, 4: bottom-right
        
        Raises:
            ValueError: If x or y is negative.

    `is_hit(self, x: int, y: int) ‑> bool`
    :   Check if a given point directly hits the atom.
        
        Args:
            x (int): The x-coordinate of the point to check.
            y (int): The y-coordinate of the point to check.
        
        Returns:
            bool: True if the point directly hits the atom, False otherwise.
        
        Raises:
            ValueError: If x or y is negative.

    `reveal(self) ‑> None`
    :   Reveal the atom.

    `set_position(self, x: int, y: int) ‑> None`
    :   Set a new position for the atom.
        
        Args:
            x (int): The new x-coordinate.
            y (int): The new y-coordinate.
        
        Raises:
            ValueError: If x or y is negative.