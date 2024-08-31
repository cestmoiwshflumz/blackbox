Module src.game.gameboard
=========================

Classes
-------

`GameBoard(difficulty: str)`
:   Represents the game board for the Black Box game.
    
    This class manages the grid, atom placement, and provides methods to interact
    with the game board state.
    
    Attributes:
        size (int): The size of the grid (size x size).
        difficulty (str): The difficulty level of the game ('easy', 'medium', or 'hard').
        grid (List[List[Optional[Atom]]]): The 2D grid representing the game board.
        atoms (List[Atom]): List of atom positions on the board.
        edge_markers (List[int]): List of numbers for edge markers.
    
    Initialize the GameBoard.
    
    Args:
        size (int): The size of the grid. Defaults to 8.
        difficulty (str): The difficulty level. Defaults to 'medium'.
    
    Raises:
        ValueError: If the size is less than 4 or the difficulty is invalid.

    ### Methods

    `all_atoms_guessed(self, guessed_atoms: List[src.game.atom.Atom]) ‑> bool`
    :   Check if all atoms have been correctly guessed.
        
        Args:
            guessed_atoms (List[Tuple[int, int]]): List of guessed atom positions.
        
        Returns:
            bool: True if all atoms have been guessed correctly, False otherwise.

    `get_atom(self, x: int, y: int) ‑> Optional[src.game.atom.Atom]`
    :   Get the atom at the specified coordinates.
        
        Args:
            x (int): The x-coordinate of the atom.
            y (int): The y-coordinate of the atom.
        
        Returns:
            Optional[Atom]: The Atom object at the specified coordinates.

    `get_board_state(self) ‑> List[List[Optional[src.game.atom.Atom]]]`
    :   Get the current state of the board.
        
        Returns:
            List[List[Optional[Atom]]]: A deep copy of the current grid.

    `get_cell(self, x: int, y: int) ‑> Optional[src.game.atom.Atom]`
    :   Get the content of a cell.
        
        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        
        Returns:
            Optional[Atom]: The content of the cell (None if empty, 'A' if atom).
        
        Raises:
            ValueError: If the coordinates are out of bounds.

    `has_atom(self, x: int, y: int) ‑> bool`
    :   Check if a cell contains an atom.
        
        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        
        Returns:
            bool: True if the cell contains an atom, False otherwise.
        
        Raises:
            ValueError: If the coordinates are out of bounds.

    `is_edge(self, x: int, y: int) ‑> bool`
    :   Check if a cell is on the edge of the grid.
        
        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        
        Returns:
            bool: True if the cell is on the edge, False otherwise.
        
        Raises:
            ValueError: If the coordinates are out of bounds.

    `is_empty(self, x: int, y: int) ‑> bool`
    :   Check if a cell is empty.
        
        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        
        Returns:
            bool: True if the cell is empty, False otherwise.
        
        Raises:
            ValueError: If the coordinates are out of bounds.

    `set_cell(self, value: src.game.atom.Atom) ‑> None`
    :   Set the content of a cell.
        
        Args:
            value (Atom): The value to set in the cell (Atom).
        
        Raises:
            ValueError: If the coordinates are out of bounds or the value is invalid.