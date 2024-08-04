# src/ui/menu.py
import pygame
from src.utils.log_instances import game_logger
from src.ui.window import Window


class Menu:
    def __init__(self, window: Window):
        self.window = window
        self.logger = game_logger
        self.font = pygame.font.Font(None, 36)
        self.menu_items = ["Start Game", "Instructions", "Options", "Quit"]
        self.selected_item = 0

    def draw(self):
        self.window.screen.fill((0, 0, 0))
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 255) if i == self.selected_item else (150, 150, 150)
            text = self.font.render(item, True, color)
            rect = text.get_rect(center=(self.window.width // 2, 200 + i * 50))
            self.window.screen.blit(text, rect)
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    return self.menu_items[self.selected_item].upper().replace(" ", "_")
        return None

    def run(self):
        self.logger.info("Menu started")
        while True:
            self.draw()
            action = self.handle_input()
            if action:
                self.logger.info(f"Menu action: {action}")
                return action


class Instructions:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 24)
        self.instructions = [
            "Black Box Game Instructions:",
            "1. The goal is to find hidden atoms in the black box.",
            "2. Send rays into the box and observe their behavior.",
            "3. Rays can be reflected, absorbed, or pass through.",
            "4. Use deduction to determine atom positions.",
            "5. Press SPACE to return to the main menu.",
        ]

    def draw(self):
        self.window.screen.fill((0, 0, 0))
        for i, line in enumerate(self.instructions):
            text = self.font.render(line, True, (255, 255, 255))
            rect = text.get_rect(left=50, top=50 + i * 30)
            self.window.screen.blit(text, rect)
        pygame.display.flip()

    def run(self):
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return "MAIN_MENU"


class Options:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.options = ["Difficulty: Normal", "Sound: On", "Back"]
        self.selected_option = 0

    def draw(self):
        self.window.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.window.width // 2, 200 + i * 50))
            self.window.screen.blit(text, rect)
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(
                        self.options
                    )
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(
                        self.options
                    )
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == len(self.options) - 1:
                        return "MAIN_MENU"
                    elif self.selected_option == 0:
                        self.options[0] = (
                            "Difficulty: Hard"
                            if self.options[0] == "Difficulty: Normal"
                            else "Difficulty: Normal"
                        )
                    elif self.selected_option == 1:
                        self.options[1] = (
                            "Sound: Off"
                            if self.options[1] == "Sound: On"
                            else "Sound: On"
                        )
        return None

    def run(self):
        while True:
            self.draw()
            action = self.handle_input()
            if action:
                return action


def run_menu(window):
    main_menu = Menu(window)
    instructions = Instructions(window)
    options = Options(window)

    current_screen = "MAIN_MENU"
    while True:
        if current_screen == "MAIN_MENU":
            action = main_menu.run()
        elif current_screen == "INSTRUCTIONS":
            action = instructions.run()
        elif current_screen == "OPTIONS":
            action = options.run()
        else:
            return current_screen

        if action == "QUIT":
            return "QUIT"
        elif action in ["START_GAME", "INSTRUCTIONS", "OPTIONS"]:
            current_screen = action
        elif action == "MAIN_MENU":
            current_screen = "MAIN_MENU"
