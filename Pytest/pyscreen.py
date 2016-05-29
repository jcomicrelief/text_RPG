import pygame
import sys
from pygame.locals import *
import random

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
    DIRT: pygame.image.load("dirt.png"),
    GRASS: pygame.image.load("grass.png"),
    WATER: pygame.image.load("water.png"),
    COAL: pygame.image.load("coal.png")
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

# player's inventory
inventory = {
    DIRT: 0,
    GRASS: 0,
    WATER: 0,
    COAL: 0
}

# a list of resources
resources = [DIRT, GRASS, WATER, COAL]

# initialise the pygame module
pygame.init()
# create a new drawing surface
setDisplay = pygame.display.set_mode((display_width, display_height + 50))
# give the window a caption
pygame.display.set_caption("MY FIRST GAME")
# create a green square (display, color, (x, y, width, height))
# pygame.draw.rect(setDisplay, GREEN, (100, 50, 20, 20))

# the player image
PLAYER = pygame.image.load("player.png").convert_alpha()
# the position of the player [x, y]
playerPos = [0, 0]

# this decides what tile is chosen to display
# loop through each row
for rw in range(map_height):
    # loop through each column in that row
    for cl in range(map_width):
        # pick a random number in that row
        randomNumber = random.randint(0, 25)
        # if a zero, then the tile is coal
        if randomNumber == 0:
            tile = COAL
        # water if the random number is a 1 or a 2
        elif randomNumber == 1 or randomNumber == 2:
            tile = WATER
        elif 3 <= randomNumber <= 7:
            tile = GRASS
        else:
            tile = DIRT
        # set the position in the tilemap to the randomNumber
        tilemap[rw][cl] = tile

# font for textboxes
font = pygame.font.SysFont(None, 25)
# add a font for our inventory
INVFONT = pygame.font.Font(None, 18)

# loop (repeat) forever
while True:
    # get all the user events
    for event in pygame.event.get():
        # if the user wants to quit
        if event.type == QUIT:
            # end the game and close the window
            pygame.quit()
            sys.exit()
        # if a key is pressed
        elif event.type == KEYDOWN:
            # if the right arrow is pressed
            if (event.key == K_RIGHT) and playerPos[0] < map_width - 1:
                # change the player's x position
                playerPos[0] += 1
            # if the left arrow is pressed
            if (event.key == K_LEFT) and playerPos[0] > 0:
                # change the player's x position
                playerPos[0] -= 1
            # if the down arrow is pressed
            if (event.key == K_DOWN) and playerPos[1] < map_height - 1:
                # change the player's y position
                playerPos[1] += 1
            # if the up arrow is pressed
            if (event.key == K_UP) and playerPos[1] > 0:
                # change the player's y position
                playerPos[1] -= 1
            if event.key == K_SPACE:
                # what resource is the player standing on
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                # player now has 1 more of this resource
                inventory[currentTile] += 1
                # the player is now standing on dirt
                tilemap[playerPos[1]][playerPos[0]] = DIRT
            # placing dirt
            if event.key == K_1:
                # get the tile to swap with the dirt
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                # if we have dirt in our inventory
                if inventory[DIRT] > 0:
                    # remove one dirt and place it
                    inventory[DIRT] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = DIRT
                    # swap the item that was there before
                    inventory[currentTile] += 1
                    # placing dirt
            if event.key == K_2:
                # get the tile to swap with the dirt
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                # if we have dirt in our inventory
                if inventory[GRASS] > 0:
                    # remove one dirt and place it
                    inventory[GRASS] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = GRASS
                    # swap the item that was there before
                    inventory[currentTile] += 1
                    # placing dirt
            if event.key == K_3:
                # get the tile to swap with the dirt
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                # if we have dirt in our inventory
                if inventory[WATER] > 0:
                    # remove one dirt and place it
                    inventory[WATER] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = WATER
                    # swap the item that was there before
                    inventory[currentTile] += 1
                    # placing dirt
            if event.key == K_4:
                # get the tile to swap with the dirt
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                # if we have dirt in our inventory
                if inventory[COAL] > 0:
                    # remove one dirt and place it
                    inventory[COAL] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = COAL
                    # swap the item that was there before
                    inventory[currentTile] += 1

    # loop through each row
    for row in range(map_height):
        # loop through each column in the row
        for column in range(map_width):
            # draw the resource at that position in the tilemap
            setDisplay.blit(textures[tilemap[row][column]], (column * tile_size, row * tile_size))

    # set the player
    setDisplay.blit(PLAYER, (playerPos[0] * tile_size, playerPos[1] * tile_size))

    # display the inventory, starting 10 pixels in
    placePosition = 10
    for item in resources:
        # add the image
        setDisplay.blit(textures[item], (placePosition, map_height * tile_size + 20))
        placePosition += 30
        # add the text showing the amount in the inventory
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        setDisplay.blit(textObj, (placePosition, map_height * tile_size + 20))
        placePosition += 50

    # update the display
    pygame.display.update()
