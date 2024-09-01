from src.game.atom import Atom
from src.utils.log_instances import atom_logger as logging


if __name__ == "__main__":
    try:
        # Create an Atom instance
        atom = Atom(3, 3)
        logging.info("Atom created successfully")
        logging.info(f"Atom position: {atom.get_position()}")

        # Test reveal and hide methods
        atom.reveal()
        logging.info(f"Is atom revealed? {atom.is_revealed}")
        atom.hide()
        logging.info(f"Is atom revealed after hiding? {atom.is_revealed}")

        # Test is_adjacent method
        logging.info(f"Is (2, 3) adjacent? {atom.is_adjacent(2, 3)}")
        logging.info(f"Is (4, 4) adjacent? {atom.is_adjacent(4, 4)}")
        logging.info(f"Is (2, 4) adjacent? {atom.is_adjacent(2, 4)}")
        logging.info(f"Is (4, 2) adjacent? {atom.is_adjacent(4, 2)}")
        logging.info(f"Is (2, 2) adjacent? {atom.is_adjacent(2, 2)}")

        # Test set_position method
        atom.set_position(5, 5)
        logging.info(f"New atom position: {atom.get_position()}")

        # Test error handling for negative coordinates
        try:
            Atom(-1, 2)
        except ValueError as e:
            logging.error(f"Error: {e}")

        try:
            atom.set_position(2, -1)
        except ValueError as e:
            logging.error(f"Error: {e}")

        # Test edge cases
        edge_atom = Atom(0, 0)
        logging.info(f"Edge atom position: {edge_atom.get_position()}")
        logging.info(f"Is (0, 1) adjacent to edge atom? {edge_atom.is_adjacent(0, 1)}")
        logging.info(f"Is (1, 1) adjacent to edge atom? {edge_atom.is_adjacent(1, 1)}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
