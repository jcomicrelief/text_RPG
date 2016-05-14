""""""
from command import *
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
        if north:
            north.south = self
        self.south = south
        if south:
            south.north = self
        self.east = east
        if east:
            east.west = west
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
        self.location = Room("Hall", "The hall looks like a room.")

    def die(self, message="Game Over!"):
        print(message)
        self.health = 0
        self.dead = True
        # for later implementation of main menu
        # raw_input()


# """Commands"""
#
#
# # inventory command
# def pack(player, args):
#     if len(player.inventory) == 0:
#         print("You aren't carrying anything.")
#     else:
#         for name, item in player.inventory:
#             if item.quantity == 1:
#                 print("{0}".format(item.name))
#             else:
#                 print("{0} x{1}".format(item.name, item.quantity))
#
#
# # look command
# def look(player, args):  # maybe change "args" to the object or whatever
#     pass
#
#
# # quit command
# def escape(player, args):
#     player.die("Thanks for playing!")
#
#
# # help command
# def aid(player, args):
#     lst = []
#     for command in commands:
#         lst.append(command)
#     lst.sort()
#     lst = ", ".join(lst)
#     print(lst)
#
# # dictionary of commands
# commands = {
#     "help": aid,
#     "inventory": pack,
#     "quit": escape,
# }
#
# # dictionary of invisible commands
# # for the purpose of giving player commands as they learn
# invisible = {
#     "look": look,
# }
#
#
# # setting up commands
# def is_valid_cmd(cmd):
#     if cmd in commands:
#         return True
#     return False
#
#
# # run commands
# def run_cmd(cmd, args, player):
#     commands[cmd](player, args)


"""Basic Variables"""
player = Player("Default", 1, 1)
"""Room Variables"""
hall = Room("Hall", "The hall looks like a room.")
bedroom = Room("Bedroom", "It's the bedroom.")
kitchen = Room("Kitchen", "It's the kitchen.")
bathroom = Room("Bathroom", "It's the bathroom.")


"""Main game file"""


# defines the main menu for the player before launching into the game
def main_menu():
    # temporary usage
    print("TEXT RPG GAME")
    print("========")


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
    # print the current inventory
    print("Inventory: {0}".format(player.inventory))

# the main game call
def main():
    main_menu()
    intro()
    show_room()

    while not player.dead:
        user = Commands()
        user.menu()
        # line = raw_input(">> ")
        # user = line.split()
        # user.append("EOI")
        # if is_valid_cmd(user[0]):
        #     run_cmd(user[0], user[1:], player)
        # else:
        #     print("Not a valid command.")

main()
