from tikz.base import TikzOptions, TikzElement
from tikz.util.position import Position

import inflect

from tools import INDENT_STR

p = inflect.engine()


class Node(TikzElement):
    def __init__(self, name, *args, node_style_name="default_node",
                 position: Position = None, depends_on=None):
        self.name = name
        self.description_parts = args

        self.position = Position() if position is None else position
        self.node_style_name = node_style_name
        super().__init__(name, depends_on=depends_on)

        if depends_on is None:
            self.depends_on = []

    def draw(self):
        return self.to_code()

    def generate_position_code(self):
        position_args = TikzOptions(*self.position.get_position_args())

        return rf"[{position_args}]"

    def generate_description_code(self):
        text = ""
        self.description_parts = [str(part) for part in self.description_parts]
        self.description_parts.append(self.internal_name)
        for i, part in enumerate(self.description_parts):
            part = part.replace("_", r"\_")
            text += "\n" + INDENT_STR
            text += fr"\nodepart{{{p.number_to_words(i + 1)}}}{{{part}}}"
        return text

    def to_code(self):
        position_args = self.generate_position_code()

        layer_description = self.generate_description_code()
        pre_code_comment = f"% node: {self.name}\n"
        code = rf"\node[{self.node_style_name}] {position_args} ({self.name}) " + \
               f"\n{INDENT_STR}{{{layer_description}}};"
        code += "\n"
        return pre_code_comment + code

    def __str__(self):
        return f"Node: {self.name} at {self.position} with style {self.node_style_name}"
