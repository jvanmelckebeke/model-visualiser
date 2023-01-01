

class Position(dict):
    def __init__(self, x: float = 0, y: float = 0):
        super().__init__()
        self.x = x
        self.y = y

    def to_code(self):
        return f"at ({self.x}, {self.y})"

    def __str__(self):
        return f"Position(left_of={self.left_of}, right_of={self.right_of}, " \
               f"below_of={self.below_of}, xshift={self.xshift}, yshift={self.yshift})"
