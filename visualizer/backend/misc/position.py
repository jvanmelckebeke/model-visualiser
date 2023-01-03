

class Position(dict):
    def __init__(self, x: float = 0, y: float = 0):
        super().__init__()
        self.x = x
        self.y = y

    def to_code(self):
        return f"at ({self.x}, {self.y})"

