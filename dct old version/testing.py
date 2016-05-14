# Prompts user for yes or no
def yes_or_no(prompt="> "):
    while 1:
        answer = raw_input(prompt)
        answer = answer.strip()
        answer = answer.lower()

        yes = ["yes", "y", "ye"]
        no = ["no", "n", "nope"]

        if answer in yes:
            return True
        elif answer in no:
            return False
        else:
            continue


# an inventory, which is initially empty
inventory = {}

# a journal, which is initially empty
journal = {}

# start the player in room 1
currentRoom = 1

notes = {
    # required: "nt desc", "title", "text"
    1: {"nt desc": "scrap of paper", "title": "test", "text": "This is just a piece of notebook paper"},
    2: {"nt desc": "crumpled ball of paper", "title": "goodbye", "text": "old paper"},
}

items = {
    # required: "it name", "it desc"
    "notebook": {
        "it name": "notebook",
        "it desc": "Good for taking notes."
    },
    "blanket": {
        "it name": "blanket",
        "it desc": "Fleece, nice, and warm."
    },
    "flashlight": {
        "it name": "flashlight",
        "it desc": "Creates light. No batteries."
    },
    "batteries": {
        "it name": "batteries",
        "it desc": "Give life to electronics."
    },
}

objects = {
    # required: "obj name", "obj desc" and []s around items
    "table": {
        "obj name": "table",
        "obj desc": "It must be made of maple. Or oak.",
        "item": [items["notebook"], items["blanket"]],
        "note": notes[2],
    },
    "lamp": {
        "obj name": "lamp",
        "obj desc": "Made in China. Why is everything made in China?",
        "note": notes[1],
    },
    "closet": {
        "obj name": "closet",
        "obj desc": "A musty closet.",
        "item": [items["blanket"]],
    },
    "desk": {
        "obj name": "desk",
        "obj desc": "A dusty desk.",
    },
    "fridge": {
        "obj name": "fridge",
        "obj desc": "An empty fridge. Well...it's got mold. Better shut it.",
    },
    "hamper": {
        "obj name": "hamper",
        "obj desc": "A hamper full of dirty clothes. That smells!",
    },
}

# JCR: testing "doors" with room 1's south doorway
# a dictionary linking a room to other room positions
rooms = {
    # required: "name", "rm desc", at least one direction, and []s around objects
    1: {
        "name": "Hall",
        "rm desc": "The hall looks like a room.",
        "east": {"status": "opened", "destination": 2, },
        "south": {"status": "opened", "destination": 3, },
        "object": [objects["table"], objects["lamp"], objects["closet"]],
    },
    2: {
        "name": "Bedroom",
        "rm desc": "It's the bedroom.",
        "west": 1,
        "south": 4,
        "object": [objects["desk"]],
    },
    3: {
        "name": "Kitchen",
        "rm desc": "It's the kitchen.",
        "north": 1,
        "object": [objects["fridge"]],
    },
    4: {
        "name": "Bathroom",
        "rm desc": "It's the bathroom",
        "north": 2,
        "object": [objects["hamper"]],
    },
}


# from random import randint #for random choices
# from info import *
# from utilities import *


def show_menu():
    # print a main menu and the commands
    print("RPG Game")
    print("========")


def show_location():
    # print the player's current location
    print("--------------------------")
    print("You are in the %s." % rooms[currentRoom]["name"])
    # print the current inventory
    print("Inventory: {0}".format(inventory.keys()))
    # print the current journal
    print(journal)
    # print an item if there is one
    # JCR: will remove, keeping for testing
    if "item" in rooms[currentRoom]:
        print("You see a %s." % ", ".join(rooms[currentRoom]["item"].keys()))

    print("--------------------------")


# converts items in rooms from list to dict
def convert_items(obj):
    it_lst = rooms[currentRoom]["object"][obj]["item"]
    if isinstance(it_lst, list):
        dct_lst = {}
        for dct in it_lst:
            dct_lst[dct["it name"]] = dct
        rooms[currentRoom]["object"][obj]["item"] = dct_lst


# converts objects in rooms from list to dict
# two occurances: beginning of game and whenever player enters a room
def convert_objects():
    print(rooms[currentRoom]["object"])
    obj_lst = rooms[currentRoom]["object"]
    if isinstance(obj_lst, list):
        dct_lst = {}
        for dct in obj_lst:
            dct_lst[dct["obj name"]] = dct
        rooms[currentRoom]["object"] = dct_lst


show_menu()
print("Your vision is blurry when you open your eyes, but you're not "
      "worried. After the nightmare of being kidnapped and brought to a "
      "strange house, you doubt that anything is out of the ordinary. "
      "Until your vision clears and you find yourself still in the house.")
# loop infinitely
while True:
    # location = rooms[currentRoom]
    # loc_obj = rooms[currentRoom]["object"]
    convert_objects()
    show_location()
    # get the player's next 'action'
    # .split() breaks it up into an list array
    # e.g. typing 'go east' would give the list:
    # ['go', 'east']
    action = raw_input("> ").lower().split()

    # if they type 'go' first
    if action[0] == "go":
        # check that they are allowed wherever they want to go
        if action[1] in rooms[currentRoom]:
            # if door is opened
            if rooms[currentRoom][action[1]]["status"] == "opened":
                # set the current room to the new room
                currentRoom = rooms[currentRoom][action[1]]
                convert_objects()
            # if door is locked
            elif rooms[currentRoom][action[1]]["status"] == "locked":
                # refuse entrance
                print("Sorry, you can't enter.")
            # if door is closed/unlocked
            else:
                print("You need to open the door.")

        # there is no door (link) to the new room
        else:
            print("You can't go that way.")

    # if they type 'take' first
    # JCR: need a better way to do this command for multiple items & notes
    elif action[0] == "take":
        # if the room contains an item and the item is the one they want
        if "item" in rooms[currentRoom] and action[1] in rooms[currentRoom]["item"]:
            # add the item to their inventory
            inventory[rooms[currentRoom]["item"][action[1]]["it name"]] = rooms[currentRoom]["item"][action[1]]
            # display a helpful message
            print("You stored the %s." % action[1])
            del rooms[currentRoom]["item"][action[1]]
            if not rooms[currentRoom]["item"]:
                #  delete the item from the room
                del rooms[currentRoom]["item"]
        # otherwise, if the item isn't there to get
        else:
            # tell them they can't get it
            action = " ".join(action[1:])
            print("There's no %s here." % action)

    # if they type 'look' first
    elif action[0] == "look":
        # if they type 'at' second
        if action[1] == "at":
            # if the room contains the object
            if "object" in rooms[currentRoom] and action[2] in rooms[currentRoom]["object"]:
                print(rooms[currentRoom]["object"][action[2]]["obj desc"])
            else:
                print("There's no %s in this room." % action[2])

        # if they type 'around' second
        elif action[1] == "around":
            # JCR: might add a better way of formatting objects and items
            print(rooms[currentRoom]["rm desc"])
            if "object" in rooms[currentRoom]:
                objects = ", ".join(rooms[currentRoom]["object"].keys())
                print("Searchable objects: %s" % objects)
            if "item" in rooms[currentRoom]:
                print("Available items: %s" % ", ".join(rooms[currentRoom]["item"]))

        # if they type anything else second
        else:
            print("Look where?")

    # if they type 'search' first
    elif action[0] == "search":
        # if the room contains the searchable object
        if "object" in rooms[currentRoom] and action[1] in rooms[currentRoom]["object"]:
            # JCR: probably a better way of writing these two options
            # if the object contains an item
            if "item" in rooms[currentRoom]["object"][action[1]]:
                convert_items(action[1])
                multyitems = rooms[currentRoom]["object"][action[1]]["item"]
                # if more than one item in object
                if len(multyitems) >= 2:
                    print("You found: %s. Take them?" % ", ".join(multyitems.keys()))
                else:
                    print("In your search, you find %s. Take it?" % ", ".join(multyitems.keys()))
                ask = yes_or_no()
                if ask:
                    # add the item to their inventory
                    for key, value in multyitems.iteritems():
                        inventory[key] = value
                    # display a helpful message
                    print("You stored: %s." % ", ".join(multyitems.keys()))
                    # delete the item from the room
                    del rooms[currentRoom]["object"][action[1]]["item"]

            # if the object has a note
            elif "note" in rooms[currentRoom]["object"][action[1]]:
                print("You see a %s. Take it?" % rooms[currentRoom]["object"][action[1]]["note"]["nt desc"])
                ask = yes_or_no()
                if ask:
                    journal[rooms[currentRoom]["object"][action[1]]["note"]["title"]] = rooms[currentRoom]["object"][action[1]]["note"]["text"]

            # if the object has both note and item
            # JCR: WIP


            # otherwise there's nothing to find
            else:
                # WIP: provide other sayings to randomly be selected
                print("Nothing of interest here.")

        # otherwise there's nothing to find
        else:
            print("There is no %s here." % action[1])

    # if they type 'drop' first
    elif action[0] == "drop":
        # JCR: How to make "drop" drop the item key and value
        # if the inventory contains the drop-able object
        if action[1] in inventory:
            print("You dropped the %s." % action[1])
            if "item" not in rooms[currentRoom]:
                rooms[currentRoom]["item"] = {}
                rooms[currentRoom]["item"][items[action[1]]["it name"]] = items[action[1]]
            del inventory[action[1]]
        else:
            print("You can't drop something you don't have.")

    # if they type 'read' first
    elif action[0] == "read":
        # if they type 'journal' second
        if action[1] == "journal":
            # check if journal is not empty
            if journal != {}:
                print("\n".join(journal.keys()).title())
            else:
                print("Your journal is empty.")
        elif action[1] in journal:
            print(journal[action[1]])
        else:
            print("Read what?")

    # if they type 'check' first
    elif action[0] == "check":
        # if they type 'inventory' second
        if action[1] == "inventory":
            # check if inventory is not empty
            if inventory != {}:
                print("In your inventory:")
                print("\n".join(inventory.keys()))
            else:
                print("There's nothing in your inventory.")
        elif action[1] in inventory:
            print(inventory[action[1]]["it desc"])
        else:
            print("Check what?")

    # if they type 'quit', they quit the game
    elif action[0] == "quit" and len(action) <= 1:
        break

    # if they type 'help', list the available commands
    # JCR: clearly WIP since it just quits
    elif action[0] == "help" and len(action) <= 1:
        print("Commands:")
        print("'go [direction]'")
        print("'take [item]'")
        print("'drop [item]'")
        print("'look around' or 'look at [object]'")
        print("'search [object]'")
        print("'read journal' or 'read [note]'")
        print("'help'")
        print("'quit'")

    else:
        # WIP: provide other sayings to randomly be selected
        # JCR: probably shouldn't be putting so much effort here...
        # converts the list of action together as a string
        action = " ".join(action)
        print("You can't %s." % action)
        continue
        # roll = randint(0,6)
        # if roll == 0:
        #    print("You don't know how to %s." % action)
        # elif roll == 1:
        #    print("Oh, so you think you can %s. How cute." % action)
        # elif roll == 2:
        #    print("Quit trying to %s. You're embarrassing yourself." % action)
        # elif roll == 3:
        #    print("You can't %s." % action)
        # elif roll == 4:
        #    print("Why would you try to %s?" % action)
        # elif roll == 5:
        #    print("Sorry, doesn't work like that.")
        # elif roll == 6:
        #    print("Wow, good job failing that.")
        # else:
        #     pass