Module src.game.ray
===================

Classes
-------

`Ray(start_x: int, start_y: int, direction: Tuple[int, int])`
:   Represents a ray in the Black Box game.
    
    This class manages the state and movement of a ray on the game board,
    including its interactions with atoms.
    
    Attributes:
        start_x (int): The starting x-coordinate of the ray.
        start_y (int): The starting y-coordinate of the ray.
        direction (Tuple[int, int]): The current direction of the ray as (dx, dy).
        path (List[Tuple[int, int]]): The path of the ray through the board.
        entry_point (Tuple[int, int]): The entry point of the ray on the board.
        exit_point (Optional[Tuple[int, int]]): The exit point of the ray, if it exits.
    
    Initialize a Ray instance.
    
    Args:
        start_x (int): The starting x-coordinate of the ray.
        start_y (int): The starting y-coordinate of the ray.
        direction (Tuple[int, int]): The initial direction of the ray as (dx, dy).
    
    Raises:
        ValueError: If the coordinates are negative or the direction is invalid.

    ### Methods

    `change_direction(self, new_direction: Tuple[int, int]) ‑> None`
    :   Change the direction of the ray.
        
        Args:
            new_direction (Tuple[int, int]): The new direction as (dx, dy).
        
        Raises:
            ValueError: If the new direction is invalid.

    `check_detour(self, atom1: src.game.atom.Atom, atom2: src.game.atom.Atom) ‑> bool`
    :   Check if the ray is detoured by two atoms.
        
        Args:
            atom1 (Atom): The first atom to check for detour.
            atom2 (Atom): The second atom to check for detour.
        
        Returns:
            bool: True if the ray is detoured by the two atoms, False otherwise.

    `check_hit(self, atom: src.game.atom.Atom) ‑> bool`
    :   Check if the ray hits the given atom.
        
        Args:
            atom (Atom): The atom to check for collision.
        
        Returns:
            bool: True if the ray hits the atom, False otherwise.

    `check_reflection(self, atom: src.game.atom.Atom) ‑> Tuple[bool, int]`
    :   Check if the ray is reflected by the given atom.
        
        Args:
            atom (Atom): The atom to check for reflection.
        
        Returns:
            Tuple[bool, int]: A tuple containing:
                - bool: True if the point is diagonally adjacent, False otherwise.
                - int: The corner number (1-4) if adjacent, 0 otherwise.
                    1: top-left, 2: top-right, 3: bottom-left, 4: bottom-right

    `get_entry_point(self) ‑> Tuple[int, int]`
    :   Get the entry point of the ray.
        
        Returns:
            Tuple[int, int]: The entry point coordinates.

    `get_exit_point(self) ‑> Optional[Tuple[int, int]]`
    :   Get the exit point of the ray, if it exists.
        
        Returns:
            Optional[Tuple[int, int]]: The exit point coordinates, or None if the ray didn't exit.

    `get_path(self) ‑> List[Tuple[int, int]]`
    :   Get the full path of the ray.
        
        Returns:
            List[Tuple[int, int]]: The list of coordinates representing the ray's path.

    `move(self) ‑> None`
    :   Move the ray one step in its current direction.

    `trace(self, gameboard: src.game.gameboard.GameBoard) ‑> None`
    :   Trace the path of the ray through the game board.
        
        Args:
            gameboard (GameBoard): The game board to trace the ray through.