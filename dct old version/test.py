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
    "bed": {
        "obj name": "bed",
        "obj desc": "An unmade bed.",
    },
    "fridge": {
        "obj name": "fridge",
        "obj desc": "An empty fridge. Well...it's got mold. Better shut it.",
    },
    "microwave": {
        "obj name": "microwave",
        "obj desc": "A broken microwave.",
    },
    "hamper": {
        "obj name": "hamper",
        "obj desc": "A hamper full of dirty clothes. That smells!",
    },
    "toilet": {
        "obj name": "toilet",
        "obj desc": "A filthy toilet.",
    },
}

# JCR: testing "doors" with room 1's south doorway
# a dictionary linking a room to other room positions
rooms = {
    # required: "name", "rm desc", at least one direction, and []s around objects
    1: {
        "name": "Hall",
        "rm desc": "The hall looks like a room.",
        "east": {"status": "locked", "destination": 2},
        "south": {"status": "opened", "destination": 3},
        "object": [objects["table"], objects["lamp"], objects["closet"]],
    },
    2: {
        "name": "Bedroom",
        "rm desc": "It's the bedroom.",
        "west": {"status": "opened", "destination": 1},
        "south": {"status": "opened", "destination": 4},
        "object": [objects["desk"], objects["bed"]],
    },
    3: {
        "name": "Kitchen",
        "rm desc": "It's the kitchen.",
        "north": {"status": "opened", "destination": 1},
        "object": [objects["fridge"], objects["microwave"]],
    },
    4: {
        "name": "Bathroom",
        "rm desc": "It's the bathroom",
        "north": {"status": "opened", "destination": 2},
        "object": [objects["hamper"], objects["toilet"]],
    },
}


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


# def convert_objects():
#     print(rooms[currentRoom]["object"])
#     obj_lst = rooms[currentRoom]["object"]
#     if isinstance(obj_lst, list):
#         dct_lst = {}
#         for dct in obj_lst:
#             dct_lst[dct["obj name"]] = dct
#         rooms[currentRoom]["object"] = dct_lst

def convert_objects():
    print(rooms[currentRoom]["object"])
    dct_lst = {}
    for dct in rooms[currentRoom]["object"]:
        dct_lst[dct["obj name"]] = dct
    rooms[currentRoom]["object"] = dct_lst
    print("---------------------")
    print(rooms[currentRoom]["object"])
convert_objects()
# loop infinitely
while True:
    # location = rooms[currentRoom]
    # loc_obj = rooms[currentRoom]["object"]
    # convert_objects()
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
                #convert_objects()
            # if door is locked
            elif rooms[currentRoom][action[1]]["status"] == "locked":
                # refuse entrance
                print("Sorry, you can't enter.")
            # if door is closed/unlocked
            else:
                print("You need to open the door.")
