import cmd


class Game(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

    def do_n(self, args):
        """Go north"""
        pass

    def do_s(self, args):
        """Go south"""
        pass

    def do_e(self, args):
        """Go east"""
        pass

    def do_w(self, args):
        """Go west"""
        pass

    def do_quit(self, args):
        """Leaves the game"""
        print("Thank you for playing")
        return True


if __name__ == "__main__":
    g = Game()
    g.cmdloop()
