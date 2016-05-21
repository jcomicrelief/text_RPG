from variables import *


# door check: used by 'go' command
def door_check(door, direction):
    room_message = "You stepped into the {0}."
    # if door is opened
    if door == "opened":
        player.location = direction
        print(room_message.format(player.location.name))
    # if door is closed
    elif door == "closed":
        print("The door is closed.")
    # if door is locked
    else:
        print("The door is locked. Find a way to open it.")


# converts player input from strings
# usage: search, look, and take commands
def input_converter(input):
    return eval(" ".join(input))
