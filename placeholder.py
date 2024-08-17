from typing import List, Optional, Tuple
import random
from src.game.atom import Atom

DEFAULT_GRID_SIZE = 8


class GameBoard:
    def __init__(self, size: int = DEFAULT_GRID_SIZE, difficulty: str = "medium"):
        if size < 4:
            raise ValueError("Grid size must be at least 4x4")

        if difficulty not in ["easy", "medium", "hard"]:
            raise ValueError(
                "Invalid difficulty level. Choose 'easy', 'medium', or 'hard'"
            )

        self.size = size
        self.difficulty = difficulty
        self.grid: List[List[Optional[Atom]]] = [
            [None for _ in range(size)] for _ in range(size)
        ]
        self.atoms: List[Atom] = []
        self.edge_markers: List[int] = list(range(1, 4 * size + 1))

        self._place_atoms()

    def _place_atoms(self) -> None:
        num_atoms = {
            "easy": random.randint(3, 4),
            "medium": random.randint(4, 5),
            "hard": random.randint(5, 6),
        }[self.difficulty]

        while len(self.atoms) < num_atoms:
            x = random.randint(1, self.size - 2)
            y = random.randint(1, self.size - 2)
            if self.grid[y][x] is None:
                atom = Atom(x, y)
                self.atoms.append(atom)
                self.grid[y][x] = atom

    def is_empty(self, x: int, y: int) -> bool:
        self._validate_coordinates(x, y)
        return self.grid[y][x] is None

    def has_atom(self, x: int, y: int) -> bool:
        self._validate_coordinates(x, y)
        return isinstance(self.grid[y][x], Atom)

    def is_edge(self, x: int, y: int) -> bool:
        self._validate_coordinates(x, y)
        return x == 0 or x == self.size - 1 or y == 0 or y == self.size - 1

    def get_cell(self, x: int, y: int) -> Optional[Atom]:
        self._validate_coordinates(x, y)
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: Optional[Atom]) -> None:
        self._validate_coordinates(x, y)
        if value is not None and not isinstance(value, Atom):
            raise ValueError(
                "Invalid cell value. Use None for empty or an Atom instance."
            )
        self.grid[y][x] = value

    def all_atoms_guessed(self, guessed_atoms: List[Tuple[int, int]]) -> bool:
        return set((atom.x, atom.y) for atom in self.atoms) == set(guessed_atoms)

    def get_board_state(self) -> List[List[Optional[Atom]]]:
        return [row[:] for row in self.grid]

    def _validate_coordinates(self, x: int, y: int) -> None:
        if not (0 <= x < self.size and 0 <= y < self.size):
            raise ValueError(
                f"Coordinates ({x}, {y}) are out of bounds for a {self.size}x{self.size} grid."
            )

    def __str__(self) -> str:
        board_str = "  " + " ".join(f"{i:2}" for i in range(self.size)) + "\n"
        for y in range(self.size):
            board_str += (
                f"{y:2} "
                + " ".join(
                    "A" if isinstance(cell, Atom) else "·" for cell in self.grid[y]
                )
                + "\n"
            )
        return board_str
