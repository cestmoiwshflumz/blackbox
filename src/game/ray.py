# src/game/ray.py

from typing import List, Tuple, Optional

from src.game.gameboard import GameBoard
from src.game.atom import Atom
from src.utils.log_instances import ray_logger as logging


class Ray:
    """
    Represents a ray in the Black Box game.

    This class manages the state and movement of a ray on the game board,
    including its interactions with atoms.

    Attributes:
        start_x (int): The starting x-coordinate of the ray.
        start_y (int): The starting y-coordinate of the ray.
        direction (Tuple[int, int]): The current direction of the ray as (dx, dy).
        path (List[Tuple[int, int]]): The path of the ray through the board.
        entry_point (Tuple[int, int]): The entry point of the ray on the board.
        exit_point (Optional[Tuple[int, int]]): The exit point of the ray, if it exits.
    """

    def __init__(self, start_x: int, start_y: int, direction: Tuple[int, int]):
        """
        Initialize a Ray instance.

        Args:
            start_x (int): The starting x-coordinate of the ray.
            start_y (int): The starting y-coordinate of the ray.
            direction (Tuple[int, int]): The initial direction of the ray as (dx, dy).

        Raises:
            ValueError: If the coordinates are negative or the direction is invalid.
        """
        if start_x < -1 or start_y < -1:
            raise ValueError("Ray coordinates must be non-negative.")
        if direction not in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            raise ValueError(
                "Invalid direction. Must be one of (0, 1), (0, -1), (1, 0), (-1, 0)."
            )

        self.start_x: int = start_x
        self.start_y: int = start_y
        self.direction: Tuple[int, int] = direction
        self.path: List[Tuple[int, int]] = [(start_x, start_y)]
        self.entry_point: Tuple[int, int] = (start_x, start_y)
        self.exit_point: Optional[Tuple[int, int]] = None
        self.is_detoured: bool = False
        self.is_double_detour: bool = False

        # Initialisation de l'ensemble des positions visitées
        self.visited_positions: set = set()  # Nouvelle ligne ajoutée
        self.visited_positions.add((start_x, start_y))  # Ajout du point d'entrée

        logging.info(
            f"Ray created at ({start_x}, {start_y}) with direction {direction}"
        )

    def move(self) -> None:
        new_x = self.path[-1][0] + self.direction[0]
        new_y = self.path[-1][1] + self.direction[1]

        # Vérifiez si la position a déjà été visitée
        if (new_x, new_y) in self.visited_positions:
            logging.warning(f"Loop detected at ({new_x}, {new_y}). Stopping trace.")
            raise Exception("Infinite loop detected in ray tracing.")

        # Enregistrez la position visitée
        self.visited_positions.add((new_x, new_y))
        self.path.append((new_x, new_y))
        logging.debug(f"Ray moved to ({new_x}, {new_y})")

    def change_direction(self, new_direction: Tuple[int, int]) -> None:
        """
        Change the direction of the ray.

        Args:
            new_direction (Tuple[int, int]): The new direction as (dx, dy).

        Raises:
            ValueError: If the new direction is invalid.
        """
        if new_direction not in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            raise ValueError(
                "Invalid direction. Must be one of (0, 1), (0, -1), (1, 0), (-1, 0)."
            )

        self.direction = new_direction
        logging.info(f"Ray direction changed to {new_direction}")

    def check_hit(self, atom: Atom) -> bool:
        """
        Check if the ray hits the given atom.

        Args:
            atom (Atom): The atom to check for collision.

        Returns:
            bool: True if the ray hits the atom, False otherwise.
        """
        return atom.is_hit(self.path[-1][0], self.path[-1][1])

    def check_reflection(self, atom: Atom) -> Tuple[bool, int]:
        """
        Check if the ray is reflected by the given atom.

        Args:
            atom (Atom): The atom to check for reflection.

        Returns:
            Tuple[bool, int]: A tuple containing:
                - bool: True if the point is diagonally adjacent, False otherwise.
                - int: The corner number (1-4) if adjacent, 0 otherwise.
                    1: top-left, 2: top-right, 3: bottom-left, 4: bottom-right
        """
        return atom.is_adjacent(self.path[-1][0], self.path[-1][1])

    def check_detour(self, atom1: Atom, atom2: Atom) -> bool:
        """
        Check if the ray is detoured by two atoms.

        Args:
            atom1 (Atom): The first atom to check for detour.
            atom2 (Atom): The second atom to check for detour.

        Returns:
            bool: True if the ray is detoured by the two atoms, False otherwise.
        """
        x, y = self.path[-1]
        is_adjacent1, _ = atom1.is_adjacent(x, y)
        is_adjacent2, _ = atom2.is_adjacent(x, y)

        if is_adjacent1 and is_adjacent2:
            self.is_double_detour = True  # Marquer comme double déviation
            return True
        return False

    def trace(self, gameboard: GameBoard) -> None:
        """
        Trace the path of the ray through the game board.

        Args:
            gameboard (GameBoard): The game board to trace the ray through.
        """
        while True:
            self.move()
            x, y = self.path[-1]

            if gameboard.is_edge(x, y):
                self.exit_point = (x, y)
                logging.info(f"Ray exited at ({x}, {y})")
                break

            try:
                # Check for hit first (absorption)
                for atom in gameboard.atoms:
                    if self.check_hit(atom):
                        logging.info(f"Ray hit atom at ({atom.x}, {atom.y})")
                        return

                # Handle multiple reflections
                reflections = []
                for atom in gameboard.atoms:
                    is_adjacent, corner = self.check_reflection(atom)
                    if is_adjacent:
                        reflections.append((atom, corner))

                if len(reflections) > 1:
                    logging.info(f"Multiple reflections detected at {reflections}")
                    self._handle_multiple_reflections(reflections)
                    return  # Arrêter le suivi du rayon après avoir géré la réflexion multiple
                elif len(reflections) == 1:
                    atom, corner = reflections[0]
                    self._handle_reflection(atom, corner)
                    continue

            except Exception as e:
                logging.error(f"Error tracing ray: {e}", exc_info=True)
                return

    def _handle_multiple_reflections(self, reflections: List[Tuple[Atom, int]]) -> None:
        """
        Handle the case of multiple reflections caused by adjacent atoms.

        Args:
            reflections (List[Tuple[Atom, int]]): List of atoms and their reflection corners.
        """
        logging.info(f"Handling multiple reflections: {reflections}")

        # Dans le cas d'une double déviation, marquer comme double déviation
        self.is_double_detour = None

        # On considère que le rayon s'arrête et est absorbé dans ce cas particulier
        self.exit_point = True  # Le rayon sort
        logging.info("Ray stopped due to multiple reflections (double deviation).")

    def _handle_reflection(self, atom: Atom, corner: int) -> None:
        """
        Handle the reflection of the ray by an atom.

        Args:
            atom (Atom): The atom causing the reflection.
            corner (int): The corner number of the atom causing the reflection.
        """
        x, y = self.path[-1]
        dx, dy = self.direction

        # Define reflection rules based on incoming direction and corner
        reflection_rules = {
            (1, (1, 0)): (0, -1),  # Top-left, from left
            (1, (0, 1)): (-1, 0),  # Top-left, from top
            (2, (-1, 0)): (0, -1),  # Top-right, from right
            (2, (0, 1)): (1, 0),  # Top-right, from top
            (3, (1, 0)): (0, 1),  # Bottom-left, from left
            (3, (0, -1)): (-1, 0),  # Bottom-left, from bottom
            (4, (-1, 0)): (0, 1),  # Bottom-right, from right
            (4, (0, -1)): (1, 0),  # Bottom-right, from bottom
        }

        new_direction = reflection_rules.get((corner, self.direction))
        if new_direction:
            self.change_direction(new_direction)
        else:
            # If not in reflection rules, reverse direction
            self.change_direction((-dx, -dy))

        logging.info(f"Ray reflected by atom at ({atom.x}, {atom.y}), corner {corner}")

    def _handle_detour(self) -> None:
        """
        Handle the detour of the ray by two atoms.
        """
        if self.is_double_detour:
            logging.info("Ray experienced a double detour (color: yellow)")
            self.direction = (-self.direction[0], -self.direction[1])
            return
        self.direction = (-self.direction[0], -self.direction[1])
        self.is_detoured = True
        logging.info("Ray detoured back to entry point")

    def get_entry_point(self) -> Tuple[int, int]:
        """
        Get the entry point of the ray.

        Returns:
            Tuple[int, int]: The entry point coordinates.
        """
        return self.entry_point

    def get_exit_point(self) -> Optional[Tuple[int, int]]:
        """
        Get the exit point of the ray, if it exists.

        Returns:
            Optional[Tuple[int, int]]: The exit point coordinates, or None if the ray didn't exit.
        """
        return self.exit_point

    def get_path(self) -> List[Tuple[int, int]]:
        """
        Get the full path of the ray.

        Returns:
            List[Tuple[int, int]]: The list of coordinates representing the ray's path.
        """
        return self.path

    def __str__(self) -> str:
        """
        Return a string representation of the Ray.

        Returns:
            str: A string describing the ray's path and status.
        """
        status = "exited" if self.exit_point else "absorbed"
        return f"Ray from {self.entry_point} to {self.exit_point or self.path[-1]}, {status}"

    def __repr__(self) -> str:
        """
        Return a string representation of the Ray for debugging.

        Returns:
            str: A string representation of the Ray instance.
        """
        return f"Ray(start_x={self.start_x}, start_y={self.start_y}, direction={self.direction})"


# Example usage and testing
if __name__ == "__main__":
    try:
        # Create a sample GameBoard (you may need to adjust this based on your GameBoard implementation)
        game_board = GameBoard(size=8, difficulty="medium")

        # Create a Ray instance
        ray = Ray(0, 0, (1, 0))
        logging.info("Ray created successfully")
        logging.info(f"Initial ray state: {ray}")

        # Trace the ray through the board
        ray.trace(game_board)
        logging.info(f"Ray path: {ray.get_path()}")
        logging.info(f"Ray entry point: {ray.get_entry_point()}")
        logging.info(f"Ray exit point: {ray.get_exit_point()}")

        # Test reflection
        atom = Atom(2, 1)
        if ray.check_reflection(atom):
            ray._handle_reflection(atom)
            logging.info(f"Ray reflected. New direction: {ray.direction}")

        # Test detour
        atom1 = Atom(3, 3)
        atom2 = Atom(5, 5)
        if ray.check_detour(atom1, atom2):
            ray._handle_detour()
            logging.info("Ray detoured")

        # Test error handling
        try:
            invalid_ray = Ray(-1, 0, (1, 0))
        except ValueError as e:
            logging.error(f"Error creating ray with invalid coordinates: {e}")

        try:
            ray.change_direction((1, 1))
        except ValueError as e:
            logging.error(f"Error changing ray direction: {e}")

        # Test edge cases
        edge_ray = Ray(0, 0, (0, 1))
        edge_ray.trace(game_board)
        logging.info(f"Edge ray: {edge_ray}")

        # Test ray that hits an atom
        atom_hit_ray = Ray(1, 1, (1, 0))
        game_board.set_cell(3, 1, "A")  # Place an atom in the ray's path
        atom_hit_ray.trace(game_board)
        logging.info(f"Ray that hits an atom: {atom_hit_ray}")

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
