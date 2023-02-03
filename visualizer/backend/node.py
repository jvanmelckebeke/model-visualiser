import inflect
from visualizer.backend.base import TikzElement
from visualizer.backend.misc.position import Position
from visualizer.util.const import FONT_SIZE, INNER_SEP, SCALE_Y

from visualizer.util.tools import INDENT_STR, latexify

DEBUG_OFFSET = 0


class Node(TikzElement):
    inflector = inflect.engine()

    def __init__(self, name, *args, node_style_name="default_node",
                 position: Position = None, depends_on=None):
        self.name = name
        self.description_parts = args

        self.position = Position() if position is None else position
        self.node_style_name = node_style_name

        super().__init__(name, depends_on=depends_on)

        if depends_on is None:
            self.depends_on = []

    @property
    def latex_name(self):
        return latexify(self.name)

    @property
    def height(self):
        return ((float(INNER_SEP + FONT_SIZE) * (len(self.description_parts))) - INNER_SEP * 2) / SCALE_Y

    def draw(self):
        return self.to_code()

    def generate_description_code(self):
        text = ""
        description_parts = [str(part) for part in self.description_parts]
        # description_parts.append(self.internal_name)
        for i, part in enumerate(description_parts):
            part = part.replace("_", r"\_")
            part_number = self.inflector.number_to_words(i + 1)
            text += "\n" + INDENT_STR
            text += fr"\nodepart{{{part_number}}}{{{part}}}"
        return text

    def to_code(self):
        layer_description = self.generate_description_code()
        node_code_comment = f"% node: {self.name}\n"

        code = f""

        node_code = rf"\node[{self.node_style_name}] ({self.latex_name}) {self.position.to_code()}" + \
                    f"\n{INDENT_STR}{{{layer_description}}};"
        node_code += "\n"
        code += node_code_comment + node_code

        return code

    def __str__(self):
        return f"Node: {self.name} at {self.position} with style {self.node_style_name}"
