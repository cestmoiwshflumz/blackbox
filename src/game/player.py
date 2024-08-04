from src.utils.log_instances import player_logger as logging


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.guesses = set()  # Change from list to set for easier toggling
        self.guesses_finalized = False
        logging.info(f"Player {self.name} initialized with score {self.score}.")

    def make_guess(self, x, y):
        if self.guesses_finalized:
            logging.warning(
                f"{self.name} attempted to make a guess after guesses were finalized."
            )
            return None
        guess = (x, y)
        if guess in self.guesses:
            self.guesses.remove(guess)
            logging.info(f"{self.name} unmarked guess: {guess}.")
        else:
            self.guesses.add(guess)
            logging.info(f"{self.name} marked guess: {guess}.")
        return guess

    def update_score(self, points):
        self.score += points
        logging.info(
            f"{self.name} updated score by {points} points. New score: {self.score}."
        )

    def get_score(self):
        logging.info(f"{self.name} current score: {self.score}.")
        return self.score

    def get_guesses(self):
        logging.info(f"{self.name} guesses: {self.guesses}.")
        return self.guesses

    def fire_ray(self):
        try:
            # Deduct points for firing a ray
            self.update_score(-1)
            logging.info(
                f"{self.name} fired a ray. Score deducted by 1 point. New score: {self.score}."
            )
        except Exception as e:
            logging.error(f"Error in fire_ray: {e}", exc_info=True)
            raise

    def correct_guess(self):
        try:
            # Add points for a correct guess
            self.update_score(10)
            logging.info(
                f"{self.name} made a correct guess. Score increased by 10 points. New score: {self.score}."
            )
        except Exception as e:
            logging.error(f"Error in correct_guess: {e}", exc_info=True)
            raise

    def incorrect_guess(self):
        try:
            # Deduct points for an incorrect guess
            self.update_score(-5)
            logging.info(
                f"{self.name} made an incorrect guess. Score deducted by 5 points. New score: {self.score}."
            )
        except Exception as e:
            logging.error(f"Error in incorrect_guess: {e}", exc_info=True)
            raise

    def finalize_guesses(self):
        try:
            self.guesses_finalized = True
            logging.info(f"{self.name} has finalized their guesses: {self.guesses}.")
        except Exception as e:
            logging.error(f"Error in finalize_guesses: {e}", exc_info=True)
            raise

    def __repr__(self):
        return f"Player(name={self.name}, score={self.score}, guesses={self.guesses})"
