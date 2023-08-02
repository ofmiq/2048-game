from logic import *


# The main function is the entry point of the game
def main():
    # Create an instance of GameBoard, GameLogic, and UserInterface
    game_board = GameBoard()
    game_logic = GameLogic(game_board)
    user_interface = UserInterface(game_board)

    # Draw the home screen with game instructions and wait for ENTER key press
    user_interface.draw_home_screen()

    # Draw the initial game interface
    user_interface.draw_interface()

    # The game loop that continues until the game is over
    while not game_board.is_game_over():

        # Process events from the user (e.g., keyboard inputs)
        for event in pygame.event.get():

            # If the user clicks the close button, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the user presses a key
            elif event.type == pygame.KEYDOWN:
                # Handle the input (move) based on the key pressed
                game_logic.handle_input(event)

                # Update the grid and add a new tile
                game_logic.update_grid()

                # Draw the updated game interface
                user_interface.draw_interface()

        # Update the display to reflect the changes
        pygame.display.update()

    # The game is over, display the end screen with the final score and options to restart or exit
    user_interface.draw_end_screen(main)


if __name__ == '__main__':
    main()
