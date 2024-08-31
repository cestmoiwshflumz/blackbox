Module src.ui.gamescreen_solo
=============================

Classes
-------

`GameScreen(window: src.ui.window.Window, game_board: src.game.gameboard.GameBoard, player: src.game.player.Player)`
:   Represents the game screen for the Black Box game.
    
    This class is responsible for rendering the game board, handling user input,
    and managing the visual representation of the game state.
    
    Attributes:
        window (Window): The game window.
        game_board (GameBoard): The game board.
        player (Player): The current player.
        cell_size (int): The size of each cell on the game board.
        board_offset (Tuple[int, int]): The offset of the board from the window edges.
        font (pygame.font.Font): The font used for rendering text.
    
    Initialize the GameScreen.
    
    Args:
        window (Window): The game window.
        game_board (GameBoard): The game board.
        player (Player): The current player.
    
    Raises:
        ValueError: If the window, game_board, or player is None.

    ### Methods

    `check_ray_detoured(self, ray: src.game.ray.Ray) ‑> bool`
    :   Check if a ray has been detoured by atoms.
        
        Args:
            ray (Ray): The ray to check.
        
        Returns:
            bool: True if the ray has been detoured, False otherwise.

    `draw(self) ‑> None`
    :   Draw the entire game screen.
        
        This method clears the screen, draws the grid, rays, guesses, and score,
        then updates the display.

    `draw_Active_rays_debug(self) ‑> None`
    :   Draw fired rays of the current turn on the game screen.
        
        This method iterates through all fired rays of the current turn and draws them on the screen.

    `draw_active_rays_normal(self) ‑> None`
    :   Draw fired rays of the current turn on the game screen.
        
        This method iterates through all fired rays of the current turn and draws them on the screen.

    `draw_all_guesses(self) ‑> None`
    :   Draw all guessed atom positions on the game screen.
        
        This method iterates through all guessed atoms and draws them on the screen.

    `draw_all_rays_debug(self) ‑> None`
    :   Draw all rays fired on the game screen.
        
        This method iterates through all fired rays and draws them on the screen.

    `draw_all_rays_normal(self) ‑> None`
    :   Draw all rays fired on the game screen.
        
        This method iterates through all fired rays and draws them on the screen.

    `draw_atoms(self, atoms: List[src.game.atom.Atom]) ‑> None`
    :   Draw atoms on the game screen.
        
        Args:
            atoms (List[Atom]): The list of atoms to draw.

    `draw_button(self, text: str, pos: Tuple[int, int], size: Tuple[int, int], color: Tuple[int, int, int]) ‑> None`
    :   Draw a button on the game screen.
        
        Args:
            text (str): The text to display on the button.
            pos (Tuple[int, int]): The position of the button on the screen.
            size (Tuple[int, int]): The size of the button.
            color (Tuple[int, int, int]): The color of the button.

    `draw_buttons(self) ‑> None`
    :   Draw all buttons on the game screen.

    `draw_current_guess(self) ‑> None`
    :   Draw the current guessed atom position on the game screen.

    `draw_debug(self) ‑> None`
    :   Draw the entire game screen with debug option enabled which allow user to see all the rays and atoms.
        
        This method clears the screen, draws the grid, rays, guesses, and score,
        then updates the display.

    `draw_grid(self) ‑> None`
    :   Draw the game grid on the screen.
        
        This method draws both vertical and horizontal lines to create the game grid.

    `draw_guesses(self) ‑> None`
    :   Draw all guessed atom positions on the game screen.
        
        This method iterates through all guessed atoms and draws them on the screen.

    `draw_normal(self) ‑> None`
    :   Draw the entire game screen.
        
        This method clears the screen, draws the grid, rays, guesses, and score,
        then updates the display.

    `draw_ray_debug(self, ray: src.game.ray.Ray) ‑> None`
    :   Draw a single ray on the game screen.
        
        Args:
            ray (Ray): The ray to be drawn.

    `draw_ray_normal(self, ray: src.game.ray.Ray) ‑> None`
    :   Only draw the entry and the exit points of the ray.
        
        Args:
            ray (Ray): The ray to be drawn.

    `draw_score(self) ‑> None`
    :   Draw the current player's score on the game screen.

    `get_board_position(self, screen_pos: Tuple[int, int]) ‑> Tuple[int, int]`
    :   Convert screen coordinates to a board position.
        
        Args:
            screen_pos (Tuple[int, int]): The position on the screen.
        
        Returns:
            Tuple[int, int]: The corresponding position on the game board.

    `get_detour_positions(self, screen_pos: Tuple[int, int]) ‑> Tuple[int, int]`
    :   Convert screen coordinates to a board position.
        
        Args:
            screen_pos (Tuple[int, int]): The position on the screen.
        
        Returns:
            Tuple[int, int]: The corresponding position on the game board.

    `get_ray_direction(self, pos: Tuple[int, int]) ‑> Optional[Tuple[int, int]]`
    :   Get the direction of a ray based on its starting position.
        
        Args:
            pos (Tuple[int, int]): The starting position of the ray.
        
        Returns:
            Optional[Tuple[int, int]]: The direction of the ray as (dx, dy), or None if invalid.

    `get_screen_position(self, board_pos: Tuple[int, int]) ‑> Tuple[int, int]`
    :   Convert a board position to screen coordinates.
        
        Args:
            board_pos (Tuple[int, int]): The position on the game board.
        
        Returns:
            Tuple[int, int]: The corresponding position on the screen.

    `handle_draw_detour(self, ray: src.game.ray.Ray) ‑> None`
    :   Handle the drawing of a detoured ray.
        
        Args:
            ray (Ray): The detoured ray to draw.

    `handle_input(self) ‑> str`
    :   Handle user input events.
        
        Returns:
            str: A string indicating the action to be taken ('QUIT', 'MAIN_MENU', or 'CONTINUE').

    `handle_left_click(self, pos: Tuple[int, int]) ‑> Optional[str]`
    :   Handle left mouse click events.
        
        This method is responsible for firing rays when the player clicks on the edge of the board.
        
        Args:
            pos (Tuple[int, int]): The position of the mouse click on the screen.

    `handle_right_click(self, pos: Tuple[int, int]) ‑> None`
    :   Handle right mouse click events.
        
        This method is responsible for placing or removing atom guesses when the player right-clicks on the board.
        
        Args:
            pos (Tuple[int, int]): The position of the mouse click on the screen.

    `highlight_cell(self, pos: Tuple[int, int], color: Tuple[int, int, int]) ‑> None`
    :   Highlight a cell on the game board.
        
        Args:
            pos (Tuple[int, int]): The position of the cell to highlight.
            color (Tuple[int, int, int]): The color to use for highlighting.

    `is_valid_guess_position(self, pos: Tuple[int, int]) ‑> bool`
    :   Check if the given position is a valid position for guessing an atom.
        
        Args:
            pos (Tuple[int, int]): The position to check.
        
        Returns:
            bool: True if the position is within the board and not on the edge, False otherwise.

    `is_valid_ray_start(self, pos: Tuple[int, int]) ‑> bool`
    :   Check if the given position is a valid starting point for a ray.
        
        Args:
            pos (Tuple[int, int]): The position to check.
        
        Returns:
            bool: True if the position is on the edge of the board, False otherwise.

    `show_game_finished(self) ‑> None`
    :   Display the game finished screen.
        
        This method shows the final score and a message indicating the end of the game.

    `show_game_over(self) ‑> None`
    :   Display the game over screen.
        
        This method shows the final score and a message indicating the end of the game.

    `update(self) ‑> None`
    :   Update the game state and redraw the screen.
        
        This method should be called once per frame to keep the game display current.