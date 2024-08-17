from src.utils.log_instances import ray_logger as logging
from src.game.gameboard import GameBoard
from src.game.ray import Ray
from src.game.atom import Atom

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
