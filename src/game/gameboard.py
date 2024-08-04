# src/game/gameboard.py

import random
from typing import List, Tuple, Optional
from src.game.atom import Atom
from src.game.ray import Ray
from src.utils.constants import DEFAULT_GRID_SIZE, DEFAULT_ATOM_COUNT
from src.utils.log_instances import game_logger as logging


class GameBoard:
    def __init__(
        self, size: int = DEFAULT_GRID_SIZE, atom_count: int = DEFAULT_ATOM_COUNT
    ):
        self.size = size
        self.atom_count = atom_count
        self.grid: List[List[Optional[Atom]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]
        self.atoms: List[Atom] = []
        self.initialize_board()
        logging.info(f"Game board initialized with size {size} and {atom_count} atoms.")

    def initialize_board(self) -> None:
        """Initialize the game board by placing atoms randomly."""
        self.atoms.clear()
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self._place_atoms()

    def _place_atoms(self) -> None:
        """Place atoms randomly on the board."""
        available_positions = [
            (x, y) for x in range(1, self.size - 1) for y in range(1, self.size - 1)
        ]
        for _ in range(self.atom_count):
            if not available_positions:
                break
            pos = random.choice(available_positions)
            available_positions.remove(pos)
            atom = Atom(pos[0], pos[1])
            self.atoms.append(atom)
            self.grid[pos[0]][pos[1]] = atom

    def is_atom_at(self, x: int, y: int) -> bool:
        """Check if there's an atom at the given coordinates."""
        return isinstance(self.grid[x][y], Atom)

    def is_edge(self, x: int, y: int) -> bool:
        """Check if the given coordinates are on the edge of the board."""
        return x == 0 or x == self.size - 1 or y == 0 or y == self.size - 1

    def is_corner(self, x: int, y: int) -> bool:
        """Check if the given coordinates are on a corner of the board."""
        return (x == 0 or x == self.size - 1) and (y == 0 or y == self.size - 1)

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if the given coordinates are within the board."""
        return 0 <= x < self.size and 0 <= y < self.size

    def get_atom_positions(self) -> List[Tuple[int, int]]:
        """Return a list of all atom positions."""
        return [atom.position() for atom in self.atoms]

    def place_atom(self, x: int, y: int) -> bool:
        """Place an atom at the given coordinates if possible."""
        if (
            self.is_valid_position(x, y)
            and not self.is_edge(x, y)
            and not self.is_atom_at(x, y)
        ):
            atom = Atom(x, y)
            self.atoms.append(atom)
            self.grid[x][y] = atom
            return True
        return False

    def remove_atom(self, x: int, y: int) -> bool:
        """Remove an atom from the given coordinates if present."""
        if self.is_atom_at(x, y):
            atom = self.grid[x][y]
            self.atoms.remove(atom)
            self.grid[x][y] = None
            return True
        return False

    def get_adjacent_atoms(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get positions of atoms adjacent to the given coordinates."""
        adjacent_atoms = []
        for atom in self.atoms:
            if atom.is_adjacent(x, y):
                adjacent_atoms.append(atom.position())
        return adjacent_atoms

    def reset(self) -> None:
        """Reset the game board to its initial state."""
        self.initialize_board()

    def __str__(self) -> str:
        """Return a string representation of the game board."""
        board_str = ""
        for row in self.grid:
            board_str += " ".join("A" if cell else "." for cell in row) + "\n"
        return board_str.strip()

    def can_fire_ray(self, x: int, y: int) -> bool:
        """Check if a ray can be fired from the given position (edge check)."""
        return self.is_edge(x, y) and not self.is_corner(x, y)

    def process_ray(self, ray: Ray) -> Ray:
        """Process a ray's path through the board."""
        while True:
            ray.move()
            x, y = ray.current_position

            if not self.is_valid_position(x, y):
                ray.set_exit(ray.path[-2])  # Set exit to last valid position
                break

            if self.is_atom_at(x, y):
                if ray.interact_with_atom(self.grid[x][y]):
                    break

            if ray.check_detour(self.atoms):
                continue

            if self.is_edge(x, y):
                ray.set_exit(ray.current_position)
                break

        return ray
