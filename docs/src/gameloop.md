Module src.gameloop
===================

Classes
-------

`GameLoop()`
:   Manages the main game loop and game state transitions.
    
    This class is responsible for initializing the game, handling state transitions,
    and managing the overall flow of the game.
    
    Attributes:
        logger: The logger instance for logging game events.
        window (Window): The game window instance.
        game_state (str): The current state of the game.
        clock (pygame.time.Clock): The game clock for controlling frame rate.
        game_board (Optional[GameBoard]): The current game board instance.
        player (Optional[Player]): The current player instance.
        game_screen (Optional[GameScreen]): The current game screen instance.
    
    Initialize the GameLoop instance.

    ### Methods

    `check_game_over(self) ‑> bool`
    :   Check if the game is over based on the player's score and guessed atoms.
        
        Returns:
            bool: True if the game is over, False otherwise.

    `play_game(self) ‑> None`
    :   Handle the main gameplay loop, including drawing the game screen and processing input.

    `quit_game(self) ‑> None`
    :   Perform cleanup operations and quit the game.

    `run(self) ‑> None`
    :   Run the main game loop.
        
        This method handles the game state transitions and calls the appropriate
        methods based on the current game state.

    `show_game_finished(self) ‑> None`
    :   Display the game finished screen.
        
        This method shows the final score and a message indicating the end of the game.

    `show_game_over(self) ‑> None`
    :   Display the game over screen and handle input for returning to the main menu.

    `start_new_game(self) ‑> None`
    :   Start a new game by initializing the game board, player, and game screen.