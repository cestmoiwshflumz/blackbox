from src.game.player import Player
from src.game.atom import Atom
from src.utils.log_instances import player_logger as logging


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
