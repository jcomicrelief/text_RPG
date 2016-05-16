""""""
"""Container"""


class Container(object):
    def __init__(self, name):
        self.name = name
        self.inside = {}
        # testing Container's ability to open and close
        self.status = "opened"

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


"""Item"""


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


"""Interactive Objects"""


class Object(Container, Item):
    def __init__(self, name, description, status="opened"):
        Container.__init__(self, name)
        Item.__init__(self, name, description, value=0, quantity=1)
        self.description = description
        self.inside = {}
        self.status = status


"""Rooms"""


class Room(Container):
    def __init__(self, name, description):
        Container.__init__(self, name)
        self.description = description

        self.north = None
        self.south = None
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

    # def door(self, north="opened", south="opened", east="opened", west="opened"):


"""Character"""


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


"""Basic Variables"""
player = Player("Default", 1, 1)
"""Items in Objects"""
notebook = Item("notebook", "Good for taking notes.")
blanket = Item("blanket", "Fleece, nice, and warm.")
flashlight = Item("flashlight", "Creates light. No batteries.")
batteries = Item("batteries", "Give life to electronics.")
"""Objects in Rooms"""
table = Object("table", "It must be made of maple. Or oak.", "opened")
lamp = Object("lamp", "Made in China. Why is everything made in China?")
closet = Object("closet", "A musty closet.", "closed")
desk = Object("desk", "A dusty desk.", "opened")
bed = Object("bed", "An unmade bed.")
fridge = Object("fridge", "An empty fridge. Well...it's got mold. Better shut it.", "opened")
microwave = Object("microwave", "A broken microwave.")
hamper = Object("hamper", "A hamper full of dirty clothes. That smells!")
toilet = Object("toilet", "A filthy toilet.")
"""Room Variables"""
hall = Room("Hall", "The hall looks like a room.")
bedroom = Room("Bedroom", "It's the bedroom.")
kitchen = Room("Kitchen", "It's the kitchen.")
bathroom = Room("Bathroom", "It's the bathroom.")
"""Notes Dictionary"""
notes = {
    # required: "nt desc", "title", "text"
    1: {"nt desc": "scrap of paper", "title": "test", "text": "This is just a piece of notebook paper"},
    2: {"nt desc": "crumpled ball of paper", "title": "goodbye", "text": "old paper"},
}

"""Commands"""
# note to self: use 'args' as the player's raw_input


# go command (player location)
def go(player, args):
    # need to add doors now (unlocked/closed, opened, locked)
    direction = args[1]
    room_message = "You stepped into the {0}."
    if direction == "east" and player.location.east is not None:
        player.location = player.location.east
        print(room_message.format(player.location.name))
    elif direction == "west" and player.location.west is not None:
        player.location = player.location.west
        print(room_message.format(player.location.name))
    elif direction == "north" and player.location.north is not None:
        player.location = player.location.north
        print(room_message.format(player.location.name))
    elif direction == "south" and player.location.south is not None:
        player.location = player.location.south
        print(room_message.format(player.location.name))
    else:
        print("You can't go that way.")


# check command (inventory and items)
def check(player, args):
    # if second word is 'inventory'
    if args[1] == "inventory":
        # if player has nothing in their inventory
        if len(player.inventory) == 0:
            print("You aren't carrying anything.")
            # testing purposes (START)
            potion = Item("Potion", 5, 2)
            lizard = Item("Magical Lizard", 9000, 1)
            player.inventory.add(potion)
            player.inventory.add(lizard)
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
    # items not implemented yet (breaks game right now
    # [AttributeError: 'str' object has no attribute 'raw']
    # [line 19, in __contains__return item.raw in self.inside]
    elif args[1] in player.inventory:
        print("Items not implemented yet")
    else:
        print("Check what?")


# quit command
def escape(player):
    player.die("Thanks for playing!")


# look command (around and at)
def look(player, args):
    # if second word is 'around'
    if args[1] == "around":
        print(player.location.description)
    # if second word is 'at'
    # objects in room having same issue as items in inventory
    # [AttributeError: 'str' object has no attribute 'raw']
    # [line 19, in __contains__ return item.raw in self.inside])
    elif args[1] == "at":
        if args[2] in player.location:
            print("Object is here.")
        else:
            print("Object not working")
    else:
        print("Look where?")


# read command (journal and titles)
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


# help command
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


"""Main game file"""


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


# Add objects into rooms
def add_objects():
    # hall objects
    hall.add(table)
    hall.add(lamp)
    hall.add(closet)


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
    add_objects()
    intro()
    show_room()

    while not player.dead:
        line = raw_input(">> ")
        user = line.split()
        user.append("EOI")
        if is_valid_cmd(user[0]):
            run_cmd(user[0], user, player)
        else:
            print("Not a valid command.")
        show_room()

main()
