from src.game.atom import Atom
from src.utils.log_instances import game_logger as logging


class Ray:
    def __init__(self, entry_point, direction):
        self.entry_point = entry_point
        self.direction = direction
        self.path = []
        self.result = None  # Store the result of the ray's interaction
        logging.info(f"Ray initialized at {entry_point} with direction {direction}.")

    def trace(self, gameboard):
        x, y = self.entry_point
        dx, dy = self.direction
        logging.info(
            f"Tracing ray from {self.entry_point} in direction {self.direction}."
        )
        try:
            while 0 <= x < gameboard.grid_size and 0 <= y < gameboard.grid_size:
                self.path.append((x, y))
                logging.info(f"Ray at position {(x, y)}.")
                if isinstance(gameboard.grid[x][y], Atom):
                    logging.info(f"Ray hit an atom at {(x, y)}.")
                    self.result = "Hit"
                    return self
                x, y, dx, dy = self.get_next_position(x, y, dx, dy, gameboard)
            logging.info("Ray missed all atoms.")
            self.result = "Miss"
            return self
        except Exception as e:
            logging.error(f"Error tracing ray: {e}", exc_info=True)
            raise

    def get_next_position(self, x, y, dx, dy, gameboard):
        new_x, new_y = x + dx, y + dy
        if self.is_reflection(new_x, new_y, gameboard):
            logging.info(f"Ray reflected at {(new_x, new_y)}.")
            return x, y, -dx, -dy
        return new_x, new_y, dx, dy

    def is_reflection(self, x, y, gameboard):
        if not (0 <= x < gameboard.grid_size and 0 <= y < gameboard.grid_size):
            return False
        adjacent_atoms = 0
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            adj_x, adj_y = x + dx, y + dy
            if 0 <= adj_x < gameboard.grid_size and 0 <= adj_y < gameboard.grid_size:
                if isinstance(gameboard.grid[adj_x][adj_y], Atom):
                    adjacent_atoms += 1
        return adjacent_atoms == 2
