import pygame
from typing import List, Tuple
from src.ui.window import Window
from src.game.gameboard import GameBoard
from src.game.player import Player
from src.game.ray import Ray
from src.utils.constants import (
    COLOR_WHITE,
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    Direction,
)


class GameScreen:
    def __init__(self, window: Window, game_board: GameBoard, player: Player):
        self.window = window
        self.game_board = game_board
        self.player = player
        self.cell_size = min(window.width, window.height) // (game_board.size + 2)
        self.board_offset = (
            (window.width - self.cell_size * game_board.size) // 2,
            (window.height - self.cell_size * game_board.size) // 2,
        )
        self.font = pygame.font.Font(None, 24)

    def draw(self):
        self.window.clear()
        self.draw_grid()
        self.draw_rays()
        self.draw_guesses()
        self.draw_score()
        self.window.update()

    def draw_grid(self):
        for i in range(self.game_board.size + 1):
            start_x = self.board_offset[0] + i * self.cell_size
            start_y = self.board_offset[1] + i * self.cell_size
            end_x = start_x
            end_y = start_y + self.game_board.size * self.cell_size
            self.window.draw_line(COLOR_WHITE, (start_x, start_y), (end_x, end_y))
            self.window.draw_line(COLOR_WHITE, (start_y, start_x), (end_y, end_x))

    def draw_rays(self):
        for ray in self.player.get_fired_rays():
            self.draw_ray(ray)

    def draw_ray(self, ray: Ray):
        color = COLOR_RED if ray.outcome == "HIT" else COLOR_GREEN
        for i in range(len(ray.path) - 1):
            start = self.get_screen_position(ray.path[i])
            end = self.get_screen_position(ray.path[i + 1])
            self.window.draw_line(color, start, end, 2)

    def draw_guesses(self):
        for guess in self.player.get_guesses():
            pos = self.get_screen_position(guess)
            self.window.draw_circle(COLOR_BLUE, pos, self.cell_size // 4)

    def draw_score(self):
        score_text = f"Score: {self.player.get_score()}"
        text_surface = self.font.render(score_text, True, COLOR_WHITE)
        self.window.get_screen().blit(text_surface, (10, 10))

    def get_screen_position(self, board_pos: Tuple[int, int]) -> Tuple[int, int]:
        return (
            self.board_offset[0] + board_pos[0] * self.cell_size,
            self.board_offset[1] + board_pos[1] * self.cell_size,
        )

    def get_board_position(self, screen_pos: Tuple[int, int]) -> Tuple[int, int]:
        return (
            (screen_pos[0] - self.board_offset[0]) // self.cell_size,
            (screen_pos[1] - self.board_offset[1]) // self.cell_size,
        )

    def handle_input(self) -> str:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_left_click(event.pos)
                elif event.button == 3:  # Right click
                    self.handle_right_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MAIN_MENU"
        return "CONTINUE"

    def handle_left_click(self, pos: Tuple[int, int]):
        board_pos = self.get_board_position(pos)
        if self.game_board.is_edge(*board_pos) and self.player.can_fire_ray():
            direction = self.get_ray_direction(board_pos)
            if direction:
                self.player.fire_ray(board_pos, direction)
                ray = Ray(board_pos, direction)
                processed_ray = self.game_board.process_ray(ray)
                self.player.fired_rays.append(processed_ray)

    def handle_right_click(self, pos: Tuple[int, int]):
        board_pos = self.get_board_position(pos)
        if not self.game_board.is_edge(*board_pos):
            self.player.make_guess(board_pos)

    def get_ray_direction(self, pos: Tuple[int, int]) -> Direction:
        x, y = pos
        if x == 0:
            return Direction.RIGHT
        elif x == self.game_board.size - 1:
            return Direction.LEFT
        elif y == 0:
            return Direction.DOWN
        elif y == self.game_board.size - 1:
            return Direction.UP
        return None

    def run(self) -> str:
        while True:
            self.draw()
            action = self.handle_input()
            if action != "CONTINUE":
                return action
