"""CONTAINER CLASS - contains Container, Interactive Objects, and Rooms"""


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
