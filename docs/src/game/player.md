Module src.game.player
======================

Classes
-------

`Player(name: str, gameboard: src.game.gameboard.GameBoard, initial_score: int = 35)`
:   Represents a player in the Black Box game.
    
    This class manages the player's state, including their score, fired rays,
    and guessed atoms. It also provides methods for player actions and turn management.
    
    Attributes:
        name (str): The name of the player.
        score (int): The current score of the player.
        fired_rays (List[Ray]): A list of rays fired by the player.
        active_turn_rays (List[Ray]): A list of rays fired during the current turn.
        guessed_atoms (List[Atom]): A list of atoms guessed by the player.
        guesses (List[Tuple[int, int]]): A list of guesses made by the player.
        is_turn (bool): Indicates whether it's currently this player's turn.
    
    Initialize a Player instance.
    
    Args:
        name (str): The name of the player.
        gameboard (GameBoard): The game board instance.
        initial_score (int): The initial score for the player. Defaults to 25.
    
    Raises:
        ValueError: If the name is empty or the initial score is negative.

    ### Methods

    `check_guess(self, x: int, y: int, gameboard: src.game.gameboard.GameBoard) ‑> bool`
    :   Check if a guess is correct based on the game board.
        
        Args:
            x (int): The x-coordinate of the guessed atom.
            y (int): The y-coordinate of the guessed atom.
            gameboard (GameBoard): The game board instance.
        
        Returns:
            bool: True if the guess was correct, False otherwise.
        
        Raises:
            ValueError: If the coordinates are out of bounds.

    `end_turn(self) ‑> None`
    :   End the player's turn.

    `fire_ray(self, x: int, y: int, direction: Tuple[int, int]) ‑> src.game.ray.Ray`
    :   Fire a ray from the specified position and direction.
        
        Args:
            x (int): The x-coordinate to fire the ray from.
            y (int): The y-coordinate to fire the ray from.
            direction (Tuple[int, int]): The direction of the ray as (dx, dy).
        
        Returns:
            Ray: The fired ray.
        
        Raises:
            ValueError: If the coordinates are negative or the direction is invalid.

    `get_active_turn_guesses(self) ‑> List[Tuple[int, int]]`
    :   Get the list of guesses made during the current turn.
        
        Returns:
            List[Tuple[int, int]]: The list of active turn guesses.

    `get_active_turn_rays(self) ‑> List[src.game.ray.Ray]`
    :   Get the list of rays fired during the current turn.
        
        Returns:
            List[Ray]: The list of active turn rays.

    `get_fired_rays(self) ‑> List[src.game.ray.Ray]`
    :   Get the list of rays fired by the player.
        
        Returns:
            List[Ray]: The list of fired rays.

    `get_guessed_atoms(self) ‑> List[src.game.atom.Atom]`
    :   Get the list of atoms guessed by the player.
        
        Returns:
            List[Atom]: The list of guessed atoms.

    `get_guesses(self) ‑> List[Tuple[int, int]]`
    :   Get the list of guesses made by the player.
        
        Returns:
            List[Tuple[int, int]]: The list of guesses as (x, y) coordinates.

    `get_score(self) ‑> int`
    :   Get the current score of the player.
        
        Returns:
            int: The current score.

    `guess_atom(self, atom: src.game.atom.Atom) ‑> None`
    :   Make a guess for an atom's position.
        
        Args:
            atom (Atom): The atom being guessed.
        
        Raises:
            ValueError: If the atom has already been guessed.

    `guess_atom_position(self, x: int, y: int) ‑> None`
    :   Make a guess for an atom's position based on coordinates.
        
        Args:
            x (int): The x-coordinate of the guessed atom.
            y (int): The y-coordinate of the guessed atom.

    `refresh_turn(self) ‑> None`
    :   Refresh the player's turn.

    `remove_guess(self, atom: src.game.atom.Atom) ‑> None`
    :   Remove a previously guessed atom.
        
        Args:
            atom (Atom): The atom to remove from guesses.
        
        Raises:
            ValueError: If the atom was not previously guessed.

    `start_turn(self) ‑> None`
    :   Start the player's turn.

    `update_score(self, points: int) ‑> None`
    :   Update the player's score.
        
        Args:
            points (int): The number of points to add (or subtract if negative).
        
        Raises:
            ValueError: If the resulting score would be negative.