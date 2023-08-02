# Import necessary libraries
import sys
from random import randint, shuffle, choice
import pygame
from constants import *
from typing import List, Tuple, Callable


# GameBoard class represents the game board and handles game state
class GameBoard:

    def __init__(self) -> None:
        # Initialize the 4x4 grid and the score
        self.grid = self.create_grid()
        self.score = 0

    def create_grid(self) -> List[List[int]]:
        # Create a new 4x4 grid with two randomly placed 2 or 4 tiles
        arr = [4 * [0] for _ in range(4)]
        cord1 = [randint(0, 3), randint(0, 3)]
        cord2 = [randint(0, 3), randint(0, 3)]
        self.insert_2_or_4(arr, cord1)
        self.insert_2_or_4(arr, cord2)
        return arr

    def simple_print(self, arr: List[List[int]]) -> None:
        # Print the 4x4 grid in a simple format
        print('-' * 23)
        for row in arr:
            print(' '.join([str(number).rjust(4) for number in row]))
        print('-' * 23)

    def insert_2_or_4(self, arr: List[List[int]], cord: Tuple[int, int]) -> List[List[int]]:
        # Insert a randomly chosen 2 or 4 at the specified coordinates in the grid
        arr[cord[0]][cord[1]] = choice([2, 4])
        return arr

    def compress_and_merge_line(self, line: List[int]) -> Tuple[List[int], int]:
        # Compress and merge a single row/column
        # Returns the new compressed and merged line and the score delta from merging
        non_zeros = [cell for cell in line if cell != 0]
        merged = []
        delta = 0
        i = 0
        while i < len(non_zeros):
            if i + 1 < len(non_zeros) and non_zeros[i] == non_zeros[i + 1]:
                # Merge adjacent cells of the same value
                merged.append(non_zeros[i] * 2)
                delta += non_zeros[i] * 2
                i += 2
            else:
                merged.append(non_zeros[i])
                i += 1
        return merged + [0] * (len(line) - len(merged)), delta

    def move_left(self) -> None:
        # Move all tiles left and merge adjacent ones with the same value
        for row in self.grid:
            compressed, delta = self.compress_and_merge_line(row)
            row[:] = compressed
            self.score += delta

    def move_right(self) -> None:
        # Move all tiles right and merge adjacent ones with the same value
        for row in self.grid:
            row.reverse()
            compressed, delta = self.compress_and_merge_line(row)
            row[:] = compressed
            self.score += delta
            row.reverse()

    def move_up(self) -> None:
        # Move all tiles up and merge adjacent ones with the same value
        for j in range(4):
            column = [self.grid[i][j] for i in range(4)]
            merged_column, delta = self.compress_and_merge_line(column)
            self.score += delta
            for i in range(4):
                self.grid[i][j] = merged_column[i]

    def move_down(self) -> None:
        # Move all tiles down and merge adjacent ones with the same value
        for j in range(4):
            column = [self.grid[i][j] for i in range(4)]
            column.reverse()
            compressed, delta = self.compress_and_merge_line(column)
            compressed.reverse()
            for i in range(4):
                self.grid[i][j] = compressed[i]
            self.score += delta

    def available_space(self) -> List[Tuple[int, int]]:
        # Return a list of coordinates of empty cells on the grid
        return [(i, j) for i in range(len(self.grid)) for j in range(len(self.grid[0])) if self.grid[i][j] == 0]

    def is_game_over(self):
        # Check if the game is over (no valid moves or 2048 tile is achieved)
        for row in self.grid:
            if self.compress_and_merge_line(row)[1] != 0 or len(self.available_space()) > 0:
                return False
        return True


# GameLogic class handles user input, game flow, and updates the grid
class GameLogic:

    def __init__(self, game_board: GameBoard) -> None:
        self.game_board = game_board
        self.previous_grid = [[0] * 4 for _ in range(4)]

    def handle_input(self, event: pygame.event) -> None:
        # Handle user keyboard input and move the tiles accordingly
        if event.key == pygame.K_LEFT:
            self.game_board.move_left()
        elif event.key == pygame.K_RIGHT:
            self.game_board.move_right()
        elif event.key == pygame.K_UP:
            self.game_board.move_up()
        elif event.key == pygame.K_DOWN:
            self.game_board.move_down()

    def draw(self) -> None:
        # Draw the current state of the grid on the screen
        screen.fill(BACKGROUND)
        for row in range(4):
            for column in range(4):
                value = self.game_board.grid[row][column]
                color = BLOCKS_COLOR[value]
                pygame.draw.rect(screen, color, (column * SIZE_BLOCK, row * SIZE_BLOCK, SIZE_BLOCK, SIZE_BLOCK))

    def run(self) -> None:
        # Start the game loop and handle user input until the game is over
        while not self.game_board.is_game_over():
            self.handle_input()
            self.draw()
            self.game_board.merge()
            pygame.time.wait(100)

    def update_grid(self) -> None:
        # Update the grid with a new random tile if there is a change and check for high score
        if self.game_board.grid != self.previous_grid:
            empty = self.game_board.available_space()
            shuffle(empty)
            random_num = empty.pop()
            self.game_board.insert_2_or_4(self.game_board.grid, random_num)
            self.previous_grid = [row[:] for row in self.game_board.grid]
            if self.game_board.score > HIGHSCORE:
                with open('highscore.py', 'w') as f:
                    f.write(str(self.game_board.score))


# UserInterface class handles drawing the game interface and screens
class UserInterface:

    def __init__(self, game_board: GameBoard) -> None:
        self.game_board = game_board

    def draw_interface(self) -> None:
        # Draw the game interface, including the grid, score, and tiles
        screen.fill(BACKGROUND)
        pygame.draw.rect(screen, TITLE_BACKGROUND, TITLE)
        self.game_board.simple_print(self.game_board.grid)

        for row in range(BLOCKS):
            for column in range(BLOCKS):
                value = self.game_board.grid[row][column]
                # Draw the tile with the appropriate value and color
                if value <= 4:
                    text = font_main.render(f'{value}', True, FONT_COLOR)
                else:
                    text = font_main.render(f'{value}', True, COLOR_FOR_BLOCKS_FONT)

                text_score = font_score.render(f'Score: ', True, BLACK_COLOR)
                screen.blit(text_score, (20, 30))

                text_score_value = font_score.render(f'{self.game_board.score}', True, BLACK_COLOR)
                screen.blit(text_score_value, (175, 30))

                w = column * SIZE_BLOCK + (column + 1) * MARGIN
                h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK

                pygame.draw.rect(screen, BLOCKS_COLOR[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))

                if value != 0:
                    font_w, font_h = text.get_size()
                    text_x = w + (SIZE_BLOCK - font_w) / 2
                    text_y = h + (SIZE_BLOCK - font_h) / 2
                    screen.blit(text, (text_x, text_y))

    def draw_home_screen(self):
        # Draw the home screen with the game logo and instructions
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            screen.fill(BACKGROUND)

            # Draw the title and logo
            logo_image = pygame.image.load('logo.png')
            logo_rect = logo_image.get_rect()
            logo_rect.center = (WIDTH // 2, HEIGHT // 3)

            # Draw the start button
            start_button_text = font_title.render('Press ENTER to start', True, WHITE)
            start_button_rect = start_button_text.get_rect()
            start_button_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)

            # Draw instructions
            instructions_text1 = font_title.render('Use arrow keys to move tiles.', True, WHITE)
            instructions_text1_rect = instructions_text1.get_rect()
            instructions_text1_rect.center = (WIDTH // 2, HEIGHT // 2 + 170)

            # Blit all elements to the screen
            screen.blit(logo_image, logo_rect)
            screen.blit(start_button_text, start_button_rect)
            screen.blit(instructions_text1, instructions_text1_rect)

            pygame.display.update()

    def draw_end_screen(self, func: Callable) -> None:
        # Draw the game over screen with the final score and high score
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button_rect.collidepoint(mouse_pos):
                        # Restart the game
                        func()
                    elif exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

            screen.fill(BACKGROUND)

            text_game_over = font_main.render('Game over!', True, WHITE)
            text_score = font_main.render(f'Score: {str(self.game_board.score)}', True, WHITE)
            text_highscore = font_main.render(f'Your highscore: {load_highscore()}', True, WHITE)

            text_game_over_rect = text_game_over.get_rect()
            text_game_over_rect.center = (WIDTH // 2, 80)

            text_score_rect = text_score.get_rect()
            text_score_rect.center = (WIDTH // 2, 140)

            text_highscore_rect = text_highscore.get_rect()
            text_highscore_rect.center = (WIDTH // 2, HEIGHT // 2)

            restart_button_text = font_main.render('Restart', True, WHITE)
            restart_button_rect = restart_button_text.get_rect()
            restart_button_rect.center = (WIDTH // 3, HEIGHT - 50)

            exit_button_text = font_main.render('Exit', True, WHITE)
            exit_button_rect = exit_button_text.get_rect()
            exit_button_rect.center = (2 * WIDTH // 3 + 20, HEIGHT - 50)

            screen.blit(text_game_over, text_game_over_rect)
            screen.blit(text_score, text_score_rect)
            screen.blit(text_highscore, text_highscore_rect)

            screen.blit(restart_button_text, restart_button_rect)
            screen.blit(exit_button_text, exit_button_rect)

            pygame.display.update()
