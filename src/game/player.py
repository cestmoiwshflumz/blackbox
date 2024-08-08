from typing import List, Tuple
from src.game.ray import Ray


class Player:
    def __init__(self, name: str = "player1", initial_points: int = 25):
        self.name = name
        self.score = initial_points
        self.guesses: List[Tuple[int, int]] = []
        self.fired_rays: List[Ray] = []

    def fire_ray(
        self, start_position: Tuple[int, int], direction: Tuple[int, int]
    ) -> None:
        """
        Fire a ray from the given start position in the specified direction.
        Deducts points for firing a ray.
        """
        self.score -= 1  # Deduct 1 point for firing a ray
        new_ray = Ray(start_position, direction)
        self.fired_rays.append(new_ray)

    def make_guess(self, position: Tuple[int, int]) -> None:
        """
        Make a guess for an atom's position.
        """
        self.guesses.append(position)

    def correct_guess(self) -> None:
        """
        Award points for a correct guess.
        """
        self.score += 10  # Add 10 points for a correct guess

    def incorrect_guess(self) -> None:
        """
        Penalize for an incorrect guess.
        """
        self.score -= 5  # Subtract 5 points for an incorrect guess

    def can_fire_ray(self) -> bool:
        """
        Check if the player has enough points to fire a ray.
        """
        return self.score > 0

    def reset_guesses(self) -> None:
        """
        Reset the player's guesses.
        """
        self.guesses.clear()

    def get_score(self) -> int:
        """
        Get the current score of the player.
        """
        return self.score

    def get_name(self) -> str:
        """
        Get the name of the player.
        """
        return self.name

    def get_fired_rays(self) -> List[Ray]:
        """
        Get the list of rays fired by the player.
        """
        return self.fired_rays

    def get_guesses(self) -> List[Tuple[int, int]]:
        """
        Get the list of guesses made by the player.
        """
        return self.guesses

    def all_atoms_guessed(self, atom_positions: List[Tuple[int, int]]) -> bool:
        """
        Check if all atoms have been correctly guessed.
        """
        return all(atom in self.guesses for atom in atom_positions)
