import math


class Position(dict):
    def __init__(self, x: float = 0, y: float = 0):
        super().__init__()
        self.x = round(x, 2)
        self.y = round(y, 2)

    def y_distance(self, other):
        return abs(self.y - other.y)

    def x_distance(self, other):
        return abs(self.x - other.x)

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def to_code(self):
        return f"at ({self.x}, {self.y})"
