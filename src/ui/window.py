# src/ui/window.py
import pygame
import yaml
from src.utils.log_instances import game_logger
from src.utils.constants import COLOR_BLACK


class Window:
    def __init__(self):
        self.logger = game_logger
        self.logger.info("Initializing Window")

        self.load_config()
        self.initialize_pygame()
        self.create_window()

    def load_config(self):
        try:
            with open("config/config.yaml", "r") as config_file:
                config = yaml.safe_load(config_file)
                self.width = config["window"]["width"]
                self.height = config["window"]["height"]
                self.title = config["window"]["title"]
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            # Set default values if config loading fails
            self.width = 800
            self.height = 600
            self.title = "Black Box Game"

    def initialize_pygame(self):
        pygame.init()
        self.logger.info("Pygame initialized")

    def create_window(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.logger.info(f"Window created: {self.width}x{self.height}")

    def clear(self):
        self.screen.fill(COLOR_BLACK)

    def update(self):
        pygame.display.flip()

    def draw_rect(self, color, rect):
        pygame.draw.rect(self.screen, color, rect)

    def draw_circle(self, color, center, radius):
        pygame.draw.circle(self.screen, color, center, radius)

    def draw_line(self, color, start_pos, end_pos, width=1):
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)

    def draw_text(self, text, font, color, position):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def get_screen(self):
        return self.screen

    def quit(self):
        pygame.quit()
        self.logger.info("Pygame quit")
