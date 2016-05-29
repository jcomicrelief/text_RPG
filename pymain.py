import pygame
import sys
from pygame.locals import *

# Set width and height of display screen
display_width = 640
display_height = 480

# Setting colors, set by RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (153, 76, 0)

# initialize the pygame module
pygame.init()
# create a new drawing surface
DISPLAY = pygame.display.set_mode((display_width, display_height))
# window caption: game title
pygame.display.set_caption("ADVENTURE")
# setting player's character
PLAYER = pygame.image.load("player.png").convert_alpha()
# setting textbox and menu font
FONT = pygame.font.Font(None, 25)

def escape():
    pygame.quit()
    sys.exit()

# loop (repeat) forever
while True:
    # get all the user events
    for event in pygame.event.get():
        # if the user wants to quit
        if event.type == QUIT:
            # end the game and close the window
            escape()
        # if a key is pressed
        if event.type == KEYDOWN:
            # if the right arrow is pressed
            if event.key == K_RIGHT:
                pass
            if event.key == K_LEFT:
                pass
            if event.key == K_DOWN:
                pass
            if event.key == K_UP:
                pass
            if event.key == K_ESCAPE:
                # end the game and close the window
                escape()
