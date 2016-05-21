"""COMMANDS"""
# note to self: use 'args' as the player's raw_input
from com_func import *
# temporarily
from variables import *


# go command (usage: go [direction])
def go(player, args):
    if args[0] == "go":
        # need to add doors now (unlocked/closed, opened, locked)
        # also need to add directions up and down
        # needs to be a better way to write this to make it neater
        direction = args[1]
        # if player types "go east"
        if direction == "east" and player.location.east is not None:
            door_check(player.location.edoor, player.location.east)
        # if player types "go west"
        elif direction == "west" and player.location.west is not None:
            door_check(player.location.wdoor, player.location.west)
        # if player types "go north"
        elif direction == "north" and player.location.north is not None:
            door_check(player.location.ndoor, player.location.north)
        # if player types "go south"
        elif direction == "south" and player.location.south is not None:
            door_check(player.location.sdoor, player.location.south)
        # if there's no room in given direction or anything undefined follows "go"
        else:
            print("Can't go that way.")


# check command (usage: check inventory/check [item])
def check(player, args):
    # if second word is 'inventory'
    if args[1] == "inventory":
        # if player has nothing in their inventory
        if len(player.inventory) == 0:
            print("You aren't carrying anything.")
            # testing purposes (START)
            player.inventory.add(batteries)
            player.inventory.add(blanket)
            # testing purposes (END)
        # if player has items
        else:
            for name, item in player.inventory:
                # if item quantity is only one
                if item.quantity == 1:
                    print("{0}".format(item.name))
                # shows item quantity
                else:
                    print("{0} x{1}".format(item.name, item.quantity))
    # if the second word is an item name
    else:
        # next line breaks when multiple words
        # DELETE: item = eval(" ".join(args[1:-1]))
        item = input_converter(args[1:-1])
        if item in player.inventory:
            print(item.description)
        else:
            print("Check what?")


# look command (usage: look around/look at [object])
def look(player, args):
    # if second word is 'around'
    if args[1] == "around":
        print(player.location.description)
    # if second word is 'at'
    # objects in room having same issue as items in inventory
    elif args[1] == "at":
        try:
            # next line breaks when multiple words
            object = input_converter(args[2:-1])
        except NameError:
            print("This object isn't in the room.")
        except SyntaxError:
            print("Look where?")
        else:
            if object in player.location:
                print(object.description)
            else:
                print("There's no {0} here.".format(object.name))
    else:
        print("Look where?")


# search command (usage: search [object])
def search(player, args):
    try:
        obj = input_converter(args[1:-1])
    except NameError:
        print("This object doesn't exist.")
    except SyntaxError:
        print("This object doesn't exist.")
    else:
        if obj in player.location:
            if len(obj) == 0:
                print("Nothing of interest here.")
            else:
                print("You find: \n{0}".format(", ".join(obj.inside.keys())))
        else:
            print("There's no {0} to search.".format(obj.name))


# take command (take [item] from [object])
def take(player, args):
    if args[0] == "take":
        try:
            item = eval(args[1])
        except NameError:
            # DELETE: item = args[1]
            print("This item doesn't exist.")
        else:
            if 2 <= len(args) <= 3:
                if item in player.location:
                    if hasattr(item, "quantity"):
                        player.inventory.add(item)
                        player.location.remove(item)
                    else:
                        print("You can't pick that up.")
                else:
                    print("That item doesn't exist.")
            elif len(args) >= 4:
                try:
                    obj = eval(args[3])
                except NameError:
                    # DELETE: obj = args[3]
                    print("This object doesn't exist.")
                else:
                    if args[2] == "from":
                        if obj in player.location and item in obj:
                            if len(obj) == 0:
                                print("There's nothing to take.")
                            else:
                                player.inventory.add(item)
                                obj.remove(item)
            else:
                print("What are you taking from?")


# read command (usage: read journal/read [title])
def read(player, args):
    # if second word is 'journal'
    if args[1] == "journal":
        # if journal not empty
        if player.journal != {}:
            print("\n".join(player.journal.keys()).title())
        # if journal is empty
        else:
            print("Your journal is empty.")
    # if second word is a title name
    # notes not implemented yet
    elif args[1] in player.journal.keys():
        print(player.journal[args[1]])
    else:
        print("Read what?")


# quit command (usage: quit)
def escape(player, args):
    player.die("Thanks for playing!")
