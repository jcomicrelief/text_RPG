import pygame
import sys
from pygame.locals import *

# Variables for height and width of game display (multiples of 32)
display_width = 640
display_height = 480
tile_size = 32
map_width = display_width / tile_size
map_height = display_height / tile_size

# Setting colors, set by RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (153, 76, 0)

# constants representing the different resources
DIRT = 0
GRASS = 1
WATER = 2
COAL = 3

# a dictionary linking resources to colors
# PROBABLY NEED TO CREATE IMAGES
textures = {
    DIRT: BROWN,
    GRASS: GREEN,
    WATER: BLUE,
    COAL: BLACK
}

# a list representing our tilemap
# tilemap = [
#     [GRASS, COAL, DIRT],
#     [WATER, WATER, GRASS],
#     [COAL, GRASS, WATER],
#     [DIRT, GRASS, COAL],
#     [GRASS, WATER, DIRT]
# ]
tilemap = [[DIRT for w in range(map_width)] for h in range(map_height)]

# initialise the pygame module
pygame.init()
# create a new drawing surface
setDisplay = pygame.display.set_mode((display_width, display_height))
# give the window a caption
pygame.display.set_caption("MY FIRST GAME")
# create a green square (display, color, (x, y, width, height))
# pygame.draw.rect(setDisplay, GREEN, (100, 50, 20, 20))

# font for textboxes
font = pygame.font.SysFont(None, 25)

# loop (repeat) forever
while True:
    # get all the user events
    for event in pygame.event.get():
        # if the user wants to quit
        if event.type == QUIT:
            # end the game and close the window
            pygame.quit()
            sys.exit()

    # loop through each row
    for row in range(map_height):
        # loop through each column in the row
        for column in range(map_width):
            # draw the resource at that position in the tilemap
            setDisplay.blit(textures[tilemap[row][column]], (column * tile_size, row * tile_size))

    # update the display
    pygame.display.update()
