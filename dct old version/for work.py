# STATUS: WORKING (kinda)
# moving around in an Text RPG
# WIP: need to input errors? [DONE]
# WIP: add an opening before the while loop [DONE]
# WIP: add a journal that updates with "read" note info, delete note after [DONE]
# WIP: add searchable objects to rooms [DONE]
# WIP: add items, notes to rooms [DONE]
# Note: fixed item in room being overwritten with yes-no prompt; HOWEVER, still need to fix it in case player "drops" items. [DONE]


# WORKING ON DROPPING THE ITEM SO THAT THE WHOLE DICTIONARY IS DROPPED FROM THE INVENTORY, NOT JUST THE VALUE!!! THE KEY GETS LOST WHEN PLACED IN THE ROOM WILL ALSO NEED TO FIGURE OUT HOW TO MAKE SURE THE WHOLE KEY-VALUE PAIR GETS BACK INTO INVENTORY WHEN TAKEN

# WIP: rewrite inventory related to make inventory a dictionary instead
# WIP: maybe add a section for you to pick your name
# WIP: add ability to move objects (push/shove, pull, pick up/hold, place)
# WIP: add rooms/doors (status: locked, closed, opened)
# WIP: include objects and items dictionaries
# WIP: add ability to jump (up, down, left, right, back, forward)combine items
# WIP: add new directions to move and look(eg. "up")
# WIP: add other things to rooms (eg. enemies)
# WIP: add interactive commands ("drop", "use", "fight", "hide", "open", "close")
# WIP: add game logic (eg. you die if you enter a room containing an enemy without a sword)
# WIP: add variables (eg. "health", "strength", "money")
# WIP: off variables, add player status, add status to objects (level, elevated, cover)
# WIP: add battles (eg. roll dice to decide your fate - no, maybe for chance related but battles should be based on attributes/variables)
# Known Limitations: one item per object, one item per room [1:WIP, 2:DONE]


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
inventory = []

# a journal, which is initially empty
journal = {}

# start the player in room 1
currentRoom = 1

notes = {
    1: {"nt desc": "scrap of paper", "title": "test", "text": "This is just a piece of notebook paper"},
    2: {"nt desc": "crumpled ball of paper", "title": "goodbye", "text": "old paper"},
    }

items = {
    "notebook": {"it name": "notebook", "it desc": "Good for taking notes."},
    "blanket": {"it name": "blanket", "it desc": "Fleece, nice, and warm."},
    "flashlight": {"it name": "flashlight", "it desc": "Creates light. No batteries."},
    "batteries": {"it name": "batteries", "it desc": "Give life to electronics."},
    }


# a dictionary linking a room to other room positions
rooms = {
    1: {
        "name": "Hall",
        "rm desc": "The hall looks like a room.",
        "east": 2,
        "south": 3,
        "object": {
            "table": {
                "obj desc": "It must be made of maple. Or oak.",
                "item": items["notebook"],
                "note": notes[2],
                },
            "lamp": {
                "obj desc": "Made in China. Why is everything made in China? There's a note attached to it.",
                "note": notes[1],
                },
            "closet": {
                "obj desc": "A musty closet.",
                "item": items["blanket"],
                },
            },
        },
    2: {
        "name": "Bedroom",
        "rm desc": "It's the bedroom.",
        "west": 1,
        "south": 4,
        "object": "desk",
        "item": "sword",
    },
    3: {
        "name": "Kitchen",
        "rm desc": "It's the kitchen.",
        "north": 1,
        "object": "fridge",
    },
    4: {
        "name": "Bathroom",
        "rm desc": "It's the bathroom",
        "north": 2,
        "object": "closet",
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
    print("You are in the %s." % location["name"])
    # print the current inventory
    print("Inventory: {0}".format(inventory))
    # print the current journal
    print(journal)
    # print an item if there is one
    # JCR: will remove, keeping for testing
    if "item" in location:
        print("You see a %s." % location["item"])
    print("--------------------------")


show_menu()
print("Your vision is blurry when you open your eyes, but you're not "
      "worried. After the nightmare of being kidnapped and brought to a "
      "strange house, you doubt that anything is out of the ordinary. "
      "Until your vision clears and you find yourself still in the house.")
# loop infinitely
while True:
    location = rooms[currentRoom]
    loc_obj = location["object"]
    show_location()
    # get the player's next 'action'
    # .split() breaks it up into an list array
    # e.g. typing 'go east' would give the list:
    # ['go', 'east']
    action = raw_input("> ").lower().split()

    # if they type 'go' first
    if action[0] == "go":
        # check that they are allowed wherever they want to go
        if action[1] in location:
            # set the current room to the new room
            currentRoom = location[action[1]]
        # there is no door (link) to the new room
        else:
            print("You can't go that way.")

    # if they type 'take' first
    # JCR: need a better way to do this command for multiple items & notes
    elif action[0] == "take":
        # if the room contains an item and the item is the one they want
        if "item" in location and action[1] in location["item"]:
            # add the item to their inventory
            inventory[location["item"]] = location["item"][action[1]]
            # display a helpful message
            print("You stored the %s." % action[1])
            if not location["item"]:
                #  delete the item from the room
                del location["item"]
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
            if "object" in location and action[2] in loc_obj:
                print(loc_obj[action[2]]["obj desc"])
            else:
                print("There's no %s in this room." % action[2])

        # if they type 'around' second
        elif action[1] == "around":
            # JCR: might add a better way of formatting objects and items
            print(location["rm desc"])
            if "object" in location:
                objects = ", ".join(location["object"].keys())
                print("Searchable objects: %s" % objects)
            if "item" in location:
                print("Available items: %s" % ", ".join(location["item"]))

        # if they type anything else second
        else:
            print("Look where?")

    # if they type 'search' first
    elif action[0] == "search":
        # if the room contains the searchable object
        if "object" in location and action[1] in loc_obj:
            # JCR: probably a better way of writing these two options
            # if the object contains an item
            if "item" in loc_obj[action[1]]:
                print("In your search, you find %s. Take it?" % loc_obj[action[1]]["item"]["it name"])
                ask = yes_or_no()
                if ask:
                    # add the item to their inventory
                    inventory[loc_obj[action[1]]["item"]["it name"]] = loc_obj[action[1]]["item"]
                    # display a helpful message
                    print("You stored: %s." % loc_obj[action[1]]["item"]["it name"])
                    # delete the item from the room
                    del loc_obj[action[1]]["item"]
            # if the object has a note
            elif "note" in loc_obj[action[1]]:
                print("You see a %s. Take it?" % loc_obj[action[1]]["note"]["nt desc"])
                ask = yes_or_no()
                if ask:
                    journal[loc_obj[action[1]]["note"]["title"]] = loc_obj[action[1]]["note"]["text"]
            # if the object has both note and item
            # JCR: WIP

            # otherwise there's nothing to find
            else:
                # WIP: provide other sayings to randomly be selected
                print("Nothing of interest here.")

        else:
            print("There is no %s here." % action[1])

    # if they type 'drop' first
    elif action[0] == "drop":
        # JCR: How to make "drop" drop the item key and value
        # if the inventory contains the drop-able object
        if action[1] in inventory:
            print("You dropped the %s." % action[1])
            location["item"] = inventory[action[1]]
            del inventory[action[1]]
        else:
            print("You can't drop something you don't have.")

    # if they type 'read' first
    elif action[0] == "read":
        # if they type 'journal' second
        if action[1] == "journal":
            print("\n".join(journal.keys()).title())
        elif action[1] in journal:
            print(journal[action[1]])
        else:
            print("Read what?")

    # if they type 'quit', they quit the game
    elif action[0] == "quit" and len(action) <= 1:
        break

    # if they type 'help', list the available commands
    # JCR: clearly WIP since it just quits
    elif action[0] == "help" and len(action) <= 1:
        print "Commands:"
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
