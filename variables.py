from character import *
from item import *
from container import *

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
"""LOCATIONS"""
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