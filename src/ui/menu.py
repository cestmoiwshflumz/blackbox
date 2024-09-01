# src/ui/menu.py
import pygame
import yaml
from typing import Optional, Union

from src.utils.log_instances import game_logger
from src.ui.window import Window


class Menu:
    """
    Represents the main menu of the game.

    This class handles the display and interaction of the main menu,
    allowing players to navigate between different game options and screens.
    """

    def __init__(self, window: Window):
        """
        Initialize the Menu class.

        Args:
            window (Window): The game window object.
        """
        self.window = window
        self.logger = game_logger
        self.font = pygame.font.Font(None, 36)
        self.menu_items = [
            "Start Game",
            "Multiplayer",
            "Instructions",
            "Options",
            "Quit",
        ]
        self.selected_item = 0

    def draw(self):
        """
        Draw the menu items on the screen.
        """
        self.window.screen.fill((0, 0, 0))
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 255) if i == self.selected_item else (150, 150, 150)
            text = self.font.render(item, True, color)
            rect = text.get_rect(center=(self.window.width // 2, 200 + i * 50))
            self.window.screen.blit(text, rect)
        pygame.display.flip()

    def handle_input(self) -> Optional[str]:
        """
        Handle user input for menu navigation and selection.

        Returns:
            Optional[str]: The selected action or None if no action was taken.
        """
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

    def run(self) -> str:
        """
        Run the main menu loop.

        Returns:
            str: The selected action to be performed.
        """
        self.logger.info("Menu started")
        while True:
            self.draw()
            action = self.handle_input()
            if action:
                self.logger.info(f"Menu action: {action}")
                return action


class Instructions:
    """
    Represents the instructions screen of the game.

    This class manages the display of game instructions, providing players
    with information on how to play the game and understand its mechanics.
    """

    def __init__(self, window: Window):
        """
        Initialize the Instructions class.

        Args:
            window (Window): The game window object.
        """
        self.window = window
        self.font = pygame.font.Font(None, 24)
        self.instructions = [
            "Black Box Game Instructions:",
            "1. The goal is to find hidden atoms in the black box.",
            "2. Send rays into the box and observe their behavior.",
            "3. Rays can be reflected, absorbed, or pass through.",
            "4. Use deduction to determine atom positions.",
            "5. Left click to fire a ray, right click to guess an atom.",
            "6. Press SPACE to return to the main menu.",
        ]

    def draw(self):
        """
        Draw the instruction text on the screen.
        """
        self.window.screen.fill((0, 0, 0))
        for i, line in enumerate(self.instructions):
            text = self.font.render(line, True, (255, 255, 255))
            rect = text.get_rect(left=50, top=50 + i * 30)
            self.window.screen.blit(text, rect)
        pygame.display.flip()

    def run(self) -> str:
        """
        Run the instructions screen loop.

        Returns:
            str: The action to be performed after exiting the instructions screen.
        """
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return "MAIN_MENU"


class Options:
    """
    Represents the options menu of the game, allowing players to adjust settings.

    This class handles loading, saving, and updating game configuration options.
    It provides methods to modify settings such as volume, difficulty, and other
    game parameters, ensuring that changes are properly saved to the config file.
    """

    def __init__(self, window: Window):
        """
        Initialize the Options class.

        Args:
            window (Window): The game window object.
        """
        self.window = window
        self.logger = game_logger
        self.font = pygame.font.Font(None, 36)
        self.config = self._load_config("config/config.yaml")
        self.options = [
            f"Difficulty: {'Hard' if self.config['options']['difficulty'] == 1 else 'Medium' if self.config['options']['difficulty'] == 0 else 'Easy'}",
            f"Sound: {'On' if self.config['options']['sound'] else 'Off'}",
            f"DEBUG: {'True' if self.config['options']['debug'] else 'False'}",
            "Save & Back To Main Menu",
        ]
        self.selected_option = 0

        if "options" not in self.config:
            self.logger.error("Missing 'options' key in configuration", exc_info=True)
            self.config["options"] = {"difficulty": 0, "sound": True, "debug": False}

        self.options = [
            f"Difficulty: {'Hard' if self.config['options']['difficulty'] == 1 else 'Medium' if self.config['options']['difficulty'] == 0 else 'Easy'}",
            f"Sound: {'On' if self.config['options']['sound'] else 'Off'}",
            f"DEBUG: {'True' if self.config['options']['debug'] else 'False'}",
            "Save & Back To Main Menu",
        ]
        self.selected_option = 0

    def _load_config(self, config_path: str) -> dict:
        """
        Load and validate the configuration from a YAML file.

        Args:
            config_path (str): The path to the configuration file.

        Returns:
            dict: The loaded configuration dictionary.
        """
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
            # Validate required config keys
            required_keys = ["options.difficulty", "options.sound", "options.debug"]
            for key in required_keys:
                if self._nested_get(config, key.split(".")) is None:
                    raise ValueError(f"Missing required config key: {key}")
            self.logger.info("Menu configuration loaded and validated")
            return config
        except Exception as e:
            self.logger.error(
                f"Failed to load or validate menu configuration: {e}", exc_info=True
            )
            # Return a default configuration
            return {"options": {"difficulty": 0, "sound": True, "debug": False}}

    def _nested_get(self, d: dict, keys: list) -> Union[dict, None]:
        """
        Get a nested value from a dictionary using a list of keys.

        Args:
            d (dict): The dictionary to search.
            keys (list): The list of keys representing the path to the desired value.

        Returns:
            Any: The value at the specified nested location, or None if not found.
        """
        for key in keys:
            d = d.get(key)
            if d is None:
                return None
        return d

    def _update_config(self, key: str, value: any) -> None:
        """
        Update a value in the nested configuration dictionary.

        Args:
            key (str): The dot-separated key path to the value.
            value (Any): The new value to set.
        """
        keys = key.split(".")
        d = self.config
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    def _save_config(self, config_path: str) -> None:
        """
        Save the current configuration to a YAML file.

        Args:
            config_path (str): The path to save the configuration file.
        """
        try:
            with open(config_path, "w") as f:
                yaml.dump(self.config, f)
            self.logger.info("Menu configuration saved")
        except Exception as e:
            self.logger.error(f"Failed to save menu configuration: {e}", exc_info=True)

    def draw(self):
        """
        Draw the options menu on the screen.
        """
        self.window.screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.window.width // 2, 200 + i * 50))
            self.window.screen.blit(text, rect)
        pygame.display.flip()

    def handle_input(self) -> Optional[str]:
        """
        Handle user input for the options menu.

        Returns:
            Optional[str]: The selected action or None if no action was taken.
        """
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
                        self._save_config("config/config.yaml")
                        return "MAIN_MENU"
                    elif self.selected_option == 0:
                        new_difficulty = (
                            1
                            if self.config["options"]["difficulty"] == 0
                            else 2 if self.config["options"]["difficulty"] == 1 else 0
                        )
                        self._update_config("options.difficulty", new_difficulty)
                        self.options[0] = (
                            f"Difficulty: {'Hard' if new_difficulty == 1 else 'Medium' if new_difficulty == 0 else 'Easy'}"
                        )
                    elif self.selected_option == 1:
                        new_sound = not self.config["options"]["sound"]
                        self._update_config("options.sound", new_sound)
                        self.options[1] = f"Sound: {'On' if new_sound else 'Off'}"
                    elif self.selected_option == 2:
                        new_debug = not self.config["options"]["debug"]
                        self._update_config("options.debug", new_debug)
                        self.options[2] = f"DEBUG: {'True' if new_debug else 'False'}"
        return None

    def run(self) -> str:
        """
        Run the options menu loop.

        Returns:
            str: The action to be performed after exiting the options menu.
        """
        while True:
            self.draw()
            action = self.handle_input()
            if action:
                return action


def run_menu(window):
    """
    Run the main menu system, including submenus.

    Args:
        window (Window): The game window object.

    Returns:
        str: The final action selected by the user.
    """
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
        elif action in ["START_GAME", "MULTIPLAYER", "INSTRUCTIONS", "OPTIONS"]:
            current_screen = action
        elif action == "MAIN_MENU":
            current_screen = "MAIN_MENU"
