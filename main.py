"""TEXT ADVENTURE RPG GAME - JCOMICRELIEF"""
"""CONTAINER CLASS"""


class Container(object):
    OPEN = "opened"
    CLOSED = "closed"
    LOCKED = "locked"
    def __init__(self, name):
        self.name = name
        self.inside = {}
        # testing Container's ability to open and close
        self.status = self.OPEN

    def __iter__(self):
        return iter(self.inside.items())

    def __len__(self):
        return len(self.inside)

    def __contains__(self, item):
        return item.raw in self.inside

    def __getitem__(self, item):
        return self.inside[item.raw]

    def __setitem__(self, item, value):
        self.inside[item.raw] = value
        return self[item]

    def add(self, item, quantity=1):
        if quantity < 0:
            raise ValueError("Negative quantity. Use remove() instead")

        if item in self:
            self[item].quantity += quantity
            self[item].recalculate()
        else:
            self[item] = item

    def remove(self, item, quantity=1):
        if item not in self:
            raise KeyError("You don't have that in your inventory.")
        if quantity < 0:
            raise ValueError("Negative quantity. Use add() instead")
        if self[item].quantity <= quantity:
            del self.inside[item.raw]
        else:
            self[item].quantity -= quantity
            self[item].recalculate()

    def open(self):
        if self.status == "closed":
            self.status = "opened"

    def close(self):
        if self.status == "opened":
            self.status = "closed"

    def lock(self):
        if self.status == "closed":
            self.status = "locked"

    def unlock(self):
        if self.status == "locked":
            self.status = "closed"


"""ITEM CLASS"""


class Item(object):
    def __init__(self, name, description, value=0, quantity=1):
        self.name = name
        self.raw = name.strip().lower()
        self.description = description
        self.quantity = quantity

        self.value = value
        self.net_value = quantity * value

    # Recalculate value of items
    def recalculate(self):
        self.net_value = self.quantity * self.value


"""INTERACTIVE OBJECTS CLASS"""


class Object(Container):
    def __init__(self, name, description, status="opened"):
        Container.__init__(self, name)
        self.description = description
        self.raw = name.strip().lower()
        self.inside = {}
        self.status = status


"""ROOMS CLASS"""


class Room(Container):
    def __init__(self, name, description):
        Container.__init__(self, name)
        self.description = description
        
        self.edoor = self.OPEN
        self.wdoor = self.OPEN
        self.ndoor = self.OPEN
        self.sdoor = self.OPEN

        self.north = None
        self.south= None
        self.east = None
        self.west = None
        self.up = None
        self.down = None

    def connect(self, north=None, south=None, east=None, west=None, up=None, down=None):
        self.north = north
        if north is not None:
            north.south = self
        self.south = south
        if south:
            south.north = self
        self.east = east
        if east is not None:
            east.west = self
        self.west = west
        if west:
            west.east = west
        self.down = down
        if down:
            down.up = down
        self.up = up
        if up:
            up.down = up
            

"""CHARACTER CLASSES"""


# Character class that parents Enemy and Player
class Character(object):
    def __init__(self, name, health, strength):
        self.name = name
        self.health = health
        self.strength = strength
        self.dead = False

    def attack(self, other):
        pass

    def update(self):
        if self.health <= 0:
            self.dead = True
            self.health = 0


# Player class, child of Character class
class Player(Character):
    def __init__(self, name, health, strength):
        Character.__init__(self, name, health, strength)
        self.inventory = Container("Inventory")
        self.journal = {}
        self.location = None

    def die(self, message="Game Over!"):
        print(message)
        self.health = 0
        self.dead = True
        # for later implementation of main menu
        # raw_input()


"""BASIC VARIABLES"""
player = Player("Default", 1, 1)
"""ITEMS IN OBJECTS"""
notebook = Item("notebook", "Good for taking notes.")
blanket = Item("blanket", "Fleece, nice, and warm.")
flashlight = Item("flashlight", "Creates light. No batteries.")
batteries = Item("batteries", "Give life to electronics.")
"""OBJECTS IN ROOMS"""
table = Object("table", "It must be made of maple. Or oak.", "opened")
lamp = Object("lamp", "Made in China. Why is everything made in China?")
closet = Object("closet", "A musty closet.", "closed")
desk = Object("desk", "A dusty desk.", "opened")
bed = Object("bed", "An unmade bed.")
fridge = Object("fridge", "An empty fridge. Well...it's got mold. Better shut it.", "opened")
microwave = Object("microwave", "A broken microwave.")
hamper = Object("hamper", "A hamper full of dirty clothes. That smells!")
toilet = Object("toilet", "A filthy toilet.")
"""ROOM VARIABLES"""
hall = Room("Hall", "The hall looks like a room.")
bedroom = Room("Bedroom", "It's the bedroom.")
kitchen = Room("Kitchen", "It's the kitchen.")
bathroom = Room("Bathroom", "It's the bathroom.")
"""NOTES DICTIONARY"""
notes = {
    # required: "nt desc", "title", "text"
    1: {"nt desc": "scrap of paper", "title": "test", "text": "This is just a piece of notebook paper"},
    2: {"nt desc": "crumpled ball of paper", "title": "goodbye", "text": "old paper"},
}


"""METHODS FOR COMMANDS"""


# converts player input from strings
# usage: 
def input_converter(input):
    return eval(" ".join(input))
    
    
# door check: used by 'go' command
def door_check(dirdoor, direction):
    room_message = "You stepped into the {0}."
    # if door is opened
    if dirdoor == "opened":
        player.location = direction
        print(room_message.format(player.location.name))
    # if door is closed
    elif dirdoor == "closed":
        print("The door is closed.")
    # if door is locked
    else:
        print("The door is locked. Find a way to open it.")

"""COMMANDS"""
# note to self: use 'args' as the player's raw_input


# go command (usag: go [direction])
def go(player, args):
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
        # next line breaks with multiple words
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
    elif args[1] == "at":
        # next line breaks with multiple words
        object = input_converter(args[2:-1])
        if object in player.location:
            print(object.description)
        else:
            print("There's no {0} here.".format(object.name))
    else:
        print("Look where?")


# search command (usage: search [object])
def search(player, args):
    obj = input_converter(args[1:-1])
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
        item = eval(args[1])
        if 2<= len(args) <= 3:
            if item in player.location:
                if hasattr(item, "quantity"):
                    player.inventory.add(item)
                    player.location.remove(item)
                else:
                    print("You can't pick that up.")
        elif len(args) >= 4:
            obj = eval(args[3])
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
    hall.edoor = "closed"

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
#def add_items():
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


# DELETE: should be able to delete safely
# testing objects vs items in room
def objvsit():
    inv = player.location.inside
    objs = []
    its = []
    for key in inv.iteritems():
        if issubclass(key, Container):
            objs.append(key)
        if issubclass(key, Item):
            its.append(key)
    print("Interactive objects: {0}".format(", ".join(objs)))
    print("Items in room: {0}".format(", ".join(its)))


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
    intro()
    #show_room()

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
