# Import the necessary library
import pygame

# Initialize pygame
pygame.init()

# Define color constants for the game interface
BACKGROUND = (171, 158, 145)
PIECES_BACKGROUND = (205, 193, 181)
TITLE_BACKGROUND = (222, 213, 197)

FONT_COLOR = (114, 115, 113)
COLOR_FOR_BLOCKS_FONT = (255, 255, 255)

BLACK_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the color for each block value
BLOCKS_COLOR = {
    0: PIECES_BACKGROUND,
    2: (238, 228, 218),
    4: (236, 224, 202),
    8: (244, 177, 122),
    16: (245, 149, 117),
    32: (245, 124, 95),
    64: (246, 93, 59),
    128: (237, 206, 113),
    256: (237, 204, 99),
    512: (237, 198, 81),
    1028: (238, 199, 68),
    2048: (236, 194, 48),
    4096: (254, 61, 61),
    8192: (255, 32, 32)
}

# Define the size of the game board and tiles
BLOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + 110

# Define the title rectangle at the top of the screen
TITLE = pygame.Rect(0, 0, WIDTH, 110)

# Initialize the game score
score = 0

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define fonts for the game interface
font_main = pygame.font.SysFont('stxingkai', 70)
font_score = pygame.font.SysFont('simsun', 48)
font_title = pygame.font.SysFont('stxingkai', 45)

# Set the game window caption
pygame.display.set_caption('2048')


def load_highscore():
    # Load the highest score from a file or create a new file with a default value
    try:
        with open('highscore.py', 'r') as f:
            return int(f.readline())
    except FileNotFoundError:
        with open('highscore.py', "w") as f:
            f.write("0")
        with open('highscore.py', "r") as f:
            return int(f.readline().strip())


# Load the highest score
HIGHSCORE = load_highscore()
