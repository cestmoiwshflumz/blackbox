class Atom:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def __repr__(self):
        return f"Atom({self.x}, {self.y})"
