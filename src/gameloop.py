# src/gameloop.py

import pygame
from src.ui.window import Window
from src.ui.menu import run_menu
from src.ui.gamescreen import GameScreen
from src.game.gameboard import GameBoard
from src.game.player import Player
from src.utils.log_instances import game_logger
from src.utils.constants import DEFAULT_GRID_SIZE, DEFAULT_ATOM_COUNT


class GameLoop:
    def __init__(self):
        self.logger = game_logger
        self.window = Window()
        self.game_state = "MAIN_MENU"
        self.clock = pygame.time.Clock()
        self.logger.info("GameLoop initialized")

    def run(self):
        self.logger.info("Starting game loop")
        while True:
            if self.game_state == "MAIN_MENU":
                self.game_state = run_menu(self.window)
            elif self.game_state == "START_GAME":
                self.start_new_game()
            elif self.game_state == "PLAYING":
                self.play_game()
            elif self.game_state == "GAME_OVER":
                self.show_game_over()
            elif self.game_state == "QUIT":
                self.quit_game()
                break
            else:
                self.logger.error(f"Unknown game state: {self.game_state}")
                self.game_state = "MAIN_MENU"

            self.clock.tick(60)  # Limit the frame rate to 60 FPS

    def start_new_game(self):
        self.logger.info("Starting new game")
        self.game_board = GameBoard(DEFAULT_GRID_SIZE, DEFAULT_ATOM_COUNT)
        self.player = Player()
        self.game_screen = GameScreen(self.window, self.game_board, self.player)
        self.game_state = "PLAYING"

    def play_game(self):
        self.game_screen.draw()
        action = self.game_screen.handle_input()

        if action == "QUIT":
            self.game_state = "QUIT"
        elif action == "MAIN_MENU":
            self.game_state = "MAIN_MENU"
        elif self.check_game_over():
            self.game_state = "GAME_OVER"

    def check_game_over(self):
        if self.player.get_score() <= 0:
            self.logger.info("Game over: Player ran out of points")
            return True
        if self.player.all_atoms_guessed(self.game_board.atoms):
            self.logger.info("Game Wins: All atoms guessed correctly")
            return True
        return False

    def show_game_over(self):
        self.logger.info("Showing game over screen")
        # TODO: Implement a proper game over screen
        font = pygame.font.Font(None, 36)
        text = font.render(
            "Game Over! Press SPACE to return to menu", True, (255, 255, 255)
        )
        text_rect = text.get_rect(
            center=(self.window.width // 2, self.window.height // 2)
        )
        self.window.get_screen().blit(text, text_rect)
        self.window.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = "QUIT"
                    waiting = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_state = "MAIN_MENU"
                    waiting = False

    def quit_game(self):
        self.logger.info("Quitting game")
        self.window.quit()


if __name__ == "__main__":
    game = GameLoop()
    game.run()
