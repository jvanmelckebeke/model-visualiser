from visualizer.backend.base import TikzElement
from visualizer.util.tools import generate_uuid


class Grid(TikzElement):
    def __init__(self, to_x, to_y, from_x=0, from_y=0, grid_style_name="grid"):
        super().__init__("grid_" + generate_uuid())
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.grid_style_name = grid_style_name

    def draw(self):
        return self.to_code()

    def to_code(self):
        # \draw[step=20pt, black, very thin] (0,0) grid (60,60);
        return rf"\draw[{self.grid_style_name}] ({self.from_x}, {self.from_y}) grid ({self.to_x}, {self.to_y});" + "\n"
