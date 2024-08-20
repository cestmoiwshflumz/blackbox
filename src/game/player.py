# src/game/player.py

from typing import List, Tuple, Optional
from src.game.ray import Ray
from src.game.atom import Atom
from src.game.gameboard import GameBoard
from src.utils.log_instances import player_logger as logging


class Player:
    """
    Represents a player in the Black Box game.

    This class manages the player's state, including their score, fired rays,
    and guessed atoms. It also provides methods for player actions and turn management.

    Attributes:
        name (str): The name of the player.
        score (int): The current score of the player.
        fired_rays (List[Ray]): A list of rays fired by the player.
        guessed_atoms (List[Atom]): A list of atoms guessed by the player.
        is_turn (bool): Indicates whether it's currently this player's turn.
    """

    def __init__(self, name: str, gameboard: GameBoard, initial_score: int = 25):
        """
        Initialize a Player instance.

        Args:
            name (str): The name of the player.
            gameboard (GameBoard): The game board instance.
            initial_score (int): The initial score for the player. Defaults to 25.

        Raises:
            ValueError: If the name is empty or the initial score is negative.
        """
        if not name.strip():
            raise ValueError("Player name cannot be empty.")
        if initial_score < 0:
            raise ValueError("Initial score cannot be negative.")

        self.gameboard = gameboard
        self.name: str = name
        self.score: int = initial_score
        self.fired_rays: List[Ray] = []
        self.guessed_atoms: List[Atom] = []
        self.is_turn: bool = False

        logging.info(f"Player '{name}' created with initial score {initial_score}")

    def update_score(self, points: int) -> None:
        """
        Update the player's score.

        Args:
            points (int): The number of points to add (or subtract if negative).

        Raises:
            ValueError: If the resulting score would be negative.
        """
        new_score = self.score + points
        if new_score < 0:
            raise ValueError("Score cannot be negative.")
        self.score = new_score
        logging.info(f"Player '{self.name}' score updated to {self.score}")

    def get_score(self) -> int:
        """
        Get the current score of the player.

        Returns:
            int: The current score.
        """
        return self.score

    def fire_ray(self, x: int, y: int, direction: Tuple[int, int]) -> Ray:
        """
        Fire a ray from the specified position and direction.

        Args:
            x (int): The x-coordinate to fire the ray from.
            y (int): The y-coordinate to fire the ray from.
            direction (Tuple[int, int]): The direction of the ray as (dx, dy).

        Returns:
            Ray: The fired ray.

        Raises:
            ValueError: If the coordinates are negative or the direction is invalid.
        """
        if x < -1 or y < -1:
            raise ValueError("Ray coordinates must be non-negative.")
        if direction not in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            raise ValueError("Invalid ray direction.")

        ray = Ray(x, y, direction)
        ray.trace(self.gameboard)
        self.fired_rays.append(ray)
        self.update_score(-1)  # Deduct 1 point for firing a ray
        logging.info(
            f"Player '{self.name}' fired a ray from ({x}, {y}) in direction {direction}"
        )
        return ray

    def guess_atom(self, atom: Atom) -> None:
        """
        Make a guess for an atom's position.

        Args:
            atom (Atom): The atom being guessed.

        Raises:
            ValueError: If the atom has already been guessed.
        """
        if atom in self.guessed_atoms:
            raise ValueError("This atom has already been guessed.")
        self.guessed_atoms.append(atom)
        logging.info(
            f"Player '{self.name}' guessed an atom at position {atom.get_position()}"
        )

    def remove_guess(self, atom: Atom) -> None:
        """
        Remove a previously guessed atom.

        Args:
            atom (Atom): The atom to remove from guesses.

        Raises:
            ValueError: If the atom was not previously guessed.
        """
        if atom not in self.guessed_atoms:
            raise ValueError("This atom was not previously guessed.")
        self.guessed_atoms.remove(atom)
        logging.info(
            f"Player '{self.name}' removed guess for atom at position {atom.get_position()}"
        )

    def get_fired_rays(self) -> List[Ray]:
        """
        Get the list of rays fired by the player.

        Returns:
            List[Ray]: The list of fired rays.
        """
        return self.fired_rays

    def get_guessed_atoms(self) -> List[Atom]:
        """
        Get the list of atoms guessed by the player.

        Returns:
            List[Atom]: The list of guessed atoms.
        """
        return self.guessed_atoms

    def start_turn(self) -> None:
        """
        Start the player's turn.
        """
        self.is_turn = True
        logging.info(f"Player '{self.name}' turn started")

    def end_turn(self) -> None:
        """
        End the player's turn.
        """
        self.is_turn = False
        logging.info(f"Player '{self.name}' turn ended")

    def __str__(self) -> str:
        """
        Return a string representation of the Player.

        Returns:
            str: A string describing the player's current state.
        """
        return f"Player '{self.name}' - Score: {self.score}, Rays fired: {len(self.fired_rays)}, Atoms guessed: {len(self.guessed_atoms)}"

    def __repr__(self) -> str:
        """
        Return a string representation of the Player for debugging.

        Returns:
            str: A string representation of the Player instance.
        """
        return f"Player(name='{self.name}', score={self.score}, fired_rays={len(self.fired_rays)}, guessed_atoms={len(self.guessed_atoms)})"


# Example usage and testing
if __name__ == "__main__":
    try:
        # Create a Player instance
        player = Player("Alice", initial_score=30)
        logging.info(f"Player created: {player}")

        # Test score updates
        player.update_score(5)
        logging.info(f"Score after update: {player.get_score()}")

        # Test firing a ray
        ray = player.fire_ray(0, 0, (1, 0))
        logging.info(f"Fired ray: {ray}")
        logging.info(f"Score after firing ray: {player.get_score()}")

        # Test guessing atoms
        atom1 = Atom(3, 3)
        atom2 = Atom(5, 5)
        player.guess_atom(atom1)
        player.guess_atom(atom2)
        logging.info(f"Guessed atoms: {player.get_guessed_atoms()}")

        # Test removing a guess
        player.remove_guess(atom1)
        logging.info(f"Guessed atoms after removal: {player.get_guessed_atoms()}")

        # Test turn management
        player.start_turn()
        logging.info(f"Is it player's turn? {player.is_turn}")
        player.end_turn()
        logging.info(f"Is it player's turn after ending? {player.is_turn}")

        # Test error handling
        try:
            Player("", initial_score=10)
        except ValueError as e:
            logging.error(f"Error creating player with empty name: {e}")

        try:
            player.update_score(-100)
        except ValueError as e:
            logging.error(f"Error updating score to negative value: {e}")

        try:
            player.update_score(-100)
        except ValueError as e:
            logging.error(f"Error updating score to negative value: {e}")

        try:
            player.fire_ray(-1, 0, (1, 0))
        except ValueError as e:
            logging.error(f"Error firing ray with negative coordinates: {e}")

        try:
            player.fire_ray(0, 0, (1, 1))
        except ValueError as e:
            logging.error(f"Error firing ray with invalid direction: {e}")

        try:
            player.guess_atom(atom1)  # Trying to guess the same atom again
        except ValueError as e:
            logging.error(f"Error guessing the same atom twice: {e}")

        try:
            player.remove_guess(Atom(7, 7))  # Trying to remove a guess that wasn't made
        except ValueError as e:
            logging.error(f"Error removing non-existent guess: {e}")

        # Test multiple ray firings
        for _ in range(5):
            player.fire_ray(0, 0, (1, 0))
        logging.info(f"Number of fired rays: {len(player.get_fired_rays())}")
        logging.info(f"Score after multiple ray firings: {player.get_score()}")

        # Test score limit
        max_score = 100
        player.update_score(max_score - player.get_score())
        logging.info(f"Score at max: {player.get_score()}")
        try:
            player.update_score(1)  # Trying to exceed max score
        except ValueError as e:
            logging.error(f"Error exceeding max score: {e}")

        # Test turn switching
        player2 = Player("Bob")
        player.end_turn()
        player2.start_turn()
        logging.info(f"Is it {player.name}'s turn? {player.is_turn}")
        logging.info(f"Is it {player2.name}'s turn? {player2.is_turn}")

        # Test string representations
        logging.info(f"str(player): {str(player)}")
        logging.info(f"repr(player): {repr(player)}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
