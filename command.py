class Commands(object):
    def __init__(self):
        self.cmds = {
            "help": aid,
            "inventory": pack,
            "quit": escape,
        }

    def menu(self):
        strcmd = input(">> ")
        if strcmd in self.cmds:
            self.cmds[strcmd]()
        else:
            print("Unknown command")

    # inventory command
    def pack(self, player, args):
        if len(player.inventory) == 0:
            print("You aren't carrying anything.")
        else:
            for name, item in player.inventory:
                if item.quantity == 1:
                    print("{0}".format(item.name))
                else:
                    print("{0} x{1}".format(item.name, item.quantity))

    # look command
    def look(self, player, args):  # maybe change "args" to the object or whatever
        pass

    # quit command
    def escape(self, player, args):
        player.die("Thanks for playing!")

    # help command
    def aid(self, player, args):
        lst = []
        for command in commands:
            lst.append(command)
        lst.sort()
        lst = ", ".join(lst)
        print(lst)