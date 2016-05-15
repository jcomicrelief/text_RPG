""""""
"""Container"""


class Container(object):
    def __init__(self, name):
        self.name = name
        self.inside = {}

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


"""Item"""


class Item(object):
    def __init__(self, name, value, quantity=1):
        self.name = name
        self.raw = name.strip().lower()
        self.quantity = quantity

        self.value = value
        self.net_value = quantity * value

    # Recalculate value of items
    def recalculate(self):
        self.net_value = self.quantity * self.value


"""Interactive Objects"""


class Object(Container):
    def __init__(self, name, description, *items):
        Container.__init__(self, name)
        self.description = description
        self.inside = {}


"""Rooms"""


class Room(Container):
    def __init__(self, name, description, *objects):
        Container.__init__(self, name)
        self.description = description
        self.inside = {}

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
"""Room Variables"""
hall = Room("Hall", "The hall looks like a room.")
bedroom = Room("Bedroom", "It's the bedroom.")
kitchen = Room("Kitchen", "It's the kitchen.")
bathroom = Room("Bathroom", "It's the bathroom.")
"""Connect Rooms"""


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
    # [line 17, in __contains__return item.raw in self.inside])
    elif args[1] in player.inventory:
        print("Items not implemented yet")
    else:
        print("Check what?")


# quit command
def escape(player, args):
    player.die("Thanks for playing!")


# look command (around and at)
def look(player, args):
    # if second word is 'around'
    if args[1] == "around":
        print(player.location.description)
    # if second word is 'at'
    # objects in rooms not implemented yet
    elif args[1] == "at":
        print("Objects in rooms not implemented yet")
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
def aid(player, args):
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
    print("You are in the {0}. To the east is the {1}. To the south is the {2}.".format(player.location.name, player.location.east, player.location.south))
    # print the player's location's directions
    print("North: {0}".format(player.location.north))
    print("South: {0}".format(player.location.south))
    print("East: {0}".format(player.location.east))
    print("West: {0}".format(player.location.west))
    # print the current inventory
    print("Inventory: {0}".format(player.inventory))


# the main game call
def main():
    main_menu()
    set_location()
    connect_rooms()
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

main()
