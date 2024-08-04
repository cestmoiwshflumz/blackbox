# src/game/ray.py

from typing import Tuple, List, Optional
from src.game.atom import Atom
from src.utils.constants import Direction, RayOutcome


class Ray:
    def __init__(self, start_position: Tuple[int, int], direction: Direction):
        self.start_position = start_position
        self.direction = direction
        self.current_position = start_position
        self.path: List[Tuple[int, int]] = [start_position]
        self.outcome: Optional[RayOutcome] = None
        self.exit_position: Optional[Tuple[int, int]] = None

    def move(self) -> None:
        """Move the ray one step in its current direction."""
        x, y = self.current_position
        if self.direction == Direction.UP:
            self.current_position = (x, y - 1)
        elif self.direction == Direction.RIGHT:
            self.current_position = (x + 1, y)
        elif self.direction == Direction.DOWN:
            self.current_position = (x, y + 1)
        elif self.direction == Direction.LEFT:
            self.current_position = (x - 1, y)
        self.path.append(self.current_position)

    def reflect(self, new_direction: Direction) -> None:
        """Change the direction of the ray when it reflects."""
        self.direction = new_direction

    def interact_with_atom(self, atom: Atom) -> bool:
        """
        Handle the interaction between the ray and an atom.
        Returns True if the ray should stop, False otherwise.
        """
        atom_pos = atom.position
        if self.current_position == atom_pos:
            self.outcome = RayOutcome.HIT
            return True

        # Check for reflection (diagonally adjacent)
        dx = atom_pos[0] - self.current_position[0]
        dy = atom_pos[1] - self.current_position[1]

        if abs(dx) == 1 and abs(dy) == 1:
            if self.direction in (Direction.UP, Direction.DOWN):
                self.reflect(Direction.LEFT if dx > 0 else Direction.RIGHT)
            else:
                self.reflect(Direction.UP if dy > 0 else Direction.DOWN)
            self.outcome = RayOutcome.REFLECTION
            return False

        return False

    def check_detour(self, atoms: List[Atom]) -> bool:
        """
        Check if the ray is passing between two diagonally adjacent atoms (detour).
        Returns True if a detour is detected, False otherwise.
        """
        x, y = self.current_position
        if self.direction in (Direction.UP, Direction.DOWN):
            adjacent_positions = [(x - 1, y), (x + 1, y)]
        else:
            adjacent_positions = [(x, y - 1), (x, y + 1)]

        adjacent_atoms = [atom for atom in atoms if atom.position in adjacent_positions]

        if len(adjacent_atoms) == 2:
            self.reflect(Direction.opposite(self.direction))
            self.outcome = RayOutcome.REFLECTION  # Detour is considered a reflection
            return True
        return False

    def set_exit(self, position: Tuple[int, int]) -> None:
        """Set the exit position of the ray."""
        self.exit_position = position
        if self.outcome is None:
            self.outcome = RayOutcome.MISS

    def get_entry_exit(self) -> Tuple[Tuple[int, int], Optional[Tuple[int, int]]]:
        """Return the entry and exit positions of the ray."""
        return self.start_position, self.exit_position

    def __str__(self) -> str:
        return f"Ray(start={self.start_position}, direction={self.direction}, outcome={self.outcome})"
