from src.game.gameboard import GameBoard
from src.game.atom import Atom
from src.utils.log_instances import gameboard_logger as logging

if __name__ == "__main__":
    try:
        board = GameBoard(size=8, difficulty="medium")
        logging.info("Game board created successfully")
        logging.info(f"Board state:\n{board}")

        # Test some methods
        logging.info(f"Is (0, 0) empty? {board.is_empty(0, 0)}")
        logging.info(f"Is (0, 0) on edge? {board.is_edge(0, 0)}")

        # Place an atom for testing
        test_atom = Atom(3, 3)
        board.set_cell(test_atom)
        logging.info(f"Placed test atom at ({test_atom.x}, {test_atom.y})")

        logging.info(
            f"Is ({test_atom.x}, {test_atom.y}) empty? {board.is_empty(test_atom.x, test_atom.y)}"
        )
        logging.info(
            f"Has atom at ({test_atom.x}, {test_atom.y})? {board.has_atom(test_atom.x, test_atom.y)}"
        )

        # Test error handling
        try:
            board.get_cell(10, 10)
        except ValueError as e:
            logging.error(f"Error: {e}", exc_info=True)

        # Test all_atoms_guessed method
        all_atoms = board.atoms + [(test_atom.x, test_atom.y)]
        logging.info(
            f"All atoms guessed correctly? {board.all_atoms_guessed(all_atoms)}"
        )

        # Display final board state
        logging.info("Final board state:")
        logging.info(f"\n{board}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
