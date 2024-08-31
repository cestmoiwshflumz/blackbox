Module src.ui.menu
==================

Functions
---------

`run_menu(window)`
:   Run the main menu system, including submenus.
    
    Args:
        window (Window): The game window object.
    
    Returns:
        str: The final action selected by the user.

Classes
-------

`Instructions(window: src.ui.window.Window)`
:   Represents the instructions screen of the game.
    
    This class manages the display of game instructions, providing players
    with information on how to play the game and understand its mechanics.
    
    Initialize the Instructions class.
    
    Args:
        window (Window): The game window object.

    ### Methods

    `draw(self)`
    :   Draw the instruction text on the screen.

    `run(self) ‑> str`
    :   Run the instructions screen loop.
        
        Returns:
            str: The action to be performed after exiting the instructions screen.

`Menu(window: src.ui.window.Window)`
:   Represents the main menu of the game.
    
    This class handles the display and interaction of the main menu,
    allowing players to navigate between different game options and screens.
    
    Initialize the Menu class.
    
    Args:
        window (Window): The game window object.

    ### Methods

    `draw(self)`
    :   Draw the menu items on the screen.

    `handle_input(self) ‑> Optional[str]`
    :   Handle user input for menu navigation and selection.
        
        Returns:
            Optional[str]: The selected action or None if no action was taken.

    `run(self) ‑> str`
    :   Run the main menu loop.
        
        Returns:
            str: The selected action to be performed.

`Options(window: src.ui.window.Window)`
:   Represents the options menu of the game, allowing players to adjust settings.
    
    This class handles loading, saving, and updating game configuration options.
    It provides methods to modify settings such as volume, difficulty, and other
    game parameters, ensuring that changes are properly saved to the config file.
    
    Initialize the Options class.
    
    Args:
        window (Window): The game window object.

    ### Methods

    `draw(self)`
    :   Draw the options menu on the screen.

    `handle_input(self) ‑> Optional[str]`
    :   Handle user input for the options menu.
        
        Returns:
            Optional[str]: The selected action or None if no action was taken.

    `run(self) ‑> str`
    :   Run the options menu loop.
        
        Returns:
            str: The action to be performed after exiting the options menu.