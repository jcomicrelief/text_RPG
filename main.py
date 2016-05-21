"""TEXT RPG GAME - JCOMICRELIEF"""
from command import *
from variables import *


# help command (usage: help)
def aid():
    lst = []
    for command in commands:
        lst.append(command)
    lst.sort()
    lst = ", ".join(lst)
    print(lst)

# dictionary of commands
commands = {
    "help": aid,
    "check": check,
    "quit": escape,
    "look": look,
    "read": read,
    "go": go,
    "search": search,
    "take": take,
}

# dictionary of invisible commands
# for the purpose of giving player commands as they learn
invisible = {
    "temp": look,
}


# setting up commands
def is_valid_cmd(cmd):
    if cmd in commands:
        return True
    return False


# run commands
def run_cmd(cmd, args, player):
    commands[cmd](player, args)


"""MAIN GAME FILE"""


# defines the main menu for the player before launching into the game
def main_menu():
    # temporary usage
    print("TEXT RPG GAME")
    print("========")


# Sets the player's beginning location
def set_location():
    # begins in the hall for now
    player.location = hall


# Connect the rooms
def connect_rooms():
    hall.connect(east=bedroom)
    bedroom.connect(west=hall, south=bathroom)
    kitchen.connect(north=hall)
    bathroom.connect(north=bedroom)


# Setting doors
def set_doors():
    hall.sdoor = "closed"


# Add objects into rooms
def add_objects():
    # hall objects
    hall.add(table)
    hall.add(lamp)
    hall.add(closet)
    # bedroom objects
    bedroom.add(bed)
    bedroom.add(desk)
    # kitchen objects
    kitchen.add(fridge)
    kitchen.add(microwave)
    # bathroom objects
    bathroom.add(hamper)
    bathroom.add(toilet)


# Add items to objects
def add_items():
    # hall items
    hall.add(notebook)
    table.add(flashlight)
    closet.add(blanket)
    # bedroom items
    desk.add(batteries)
    # kitchen items

    # bathroom items


# Performs an intro for the player
def intro():
    print("Your vision is blurry when you open your eyes, but you're not "
          "worried. After the nightmare of being kidnapped and brought to a "
          "strange house, you doubt that anything is out of the ordinary. "
          "Until your vision clears and you find yourself still in the house.")


# for testing purposes
def show_room():
    # print the player's current location
    print("-------------------------")
    print("You are in the {0}.".format(player.location.name))
    print("Interactive objects: {0}".format(", ".join(player.location.inside.keys())))
    # print the current inventory
    print("Inventory: {0}".format(player.inventory.inside.keys()))


# the main game call
def main():
    main_menu()
    set_location()
    connect_rooms()
    set_doors()
    add_objects()
    add_items()
    intro()

    while not player.dead:
        # testing (START)
        show_room()
        # testing (END)
        line = raw_input(">> ")
        user = line.split()
        user.append("EOI")
        if is_valid_cmd(user[0]):
            run_cmd(user[0], user, player)
        else:
            print("Not a valid command.")

main()
