class Globals(object):
    def __init__(self):
        self.x = 50
        self.y = 50

    def left(self):
        self.x -= 1

    def right(self):
        self.x += 1

    def up(self):
        self.y -= 1

    def down(self):
        self.y += 1