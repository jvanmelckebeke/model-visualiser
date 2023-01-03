import inflect
from visualizer.backend.base import TikzElement
from visualizer.backend.misc.position import Position
from visualizer.util.const import FONT_SIZE, INNER_SEP, SCALE_Y

from visualizer.util.tools import INDENT_STR

p = inflect.engine()

DEBUG_OFFSET = 0


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

    @property
    def height(self):
        return (((INNER_SEP + FONT_SIZE) * (len(self.description_parts) + 1)) + INNER_SEP * 1.75) / SCALE_Y

    def draw(self):
        return self.to_code()

    def generate_description_code(self):
        text = ""
        description_parts = [str(part) for part in self.description_parts]
        description_parts.append(self.internal_name)
        for i, part in enumerate(description_parts):
            part = part.replace("_", r"\_")
            text += "\n" + INDENT_STR
            text += fr"\nodepart{{{p.number_to_words(i + 1)}}}{{{part}}}"
        return text

    def to_code(self):
        layer_description = self.generate_description_code()
        node_code_comment = f"% node: {self.name}\n"

        code = f""

        node_code = rf"\node[{self.node_style_name}] ({self.name}) {self.position.to_code()}" + \
                    f"\n{INDENT_STR}{{{layer_description}}};"
        node_code += "\n"
        code += node_code_comment + node_code

        return code

    def __str__(self):
        return f"Node: {self.name} at {self.position} with style {self.node_style_name}"


class NodeGroup(TikzElement):
    def __init__(self, primary_node: Node, node_before: Node = None, node_after: Node = None, name=None):
        if name is None:
            name = primary_node.name + "_group"
        self.name = name
        self.primary_node = primary_node
        self.node_before = node_before
        self.node_after = node_after

        super().__init__(name)

    @property
    def height(self):
        total_height = self.primary_node.height
        if self.node_before is not None:
            total_height += self.node_before.height
        if self.node_after is not None:
            total_height += self.node_after.height
        return total_height

    def draw(self):
        return self.to_code()

    def reposition_before_node(self):
        if self.node_before is None:
            return
        if self.node_after is None:
            self.node_before.position = Position(self.primary_node.position.x - DEBUG_OFFSET,
                                                 self.primary_node.position.y + self.height / 2)
        else:
            self.node_before.position = Position(self.primary_node.position.x - DEBUG_OFFSET,
                                                 (
                                                             self.primary_node.position.y + self.height / 2 - self.node_after.height / 2))

    def reposition_after_node(self):
        if self.node_after is None:
            return
        if self.node_before is None:
            self.node_after.position = Position(self.primary_node.position.x + DEBUG_OFFSET,
                                                self.primary_node.position.y - self.height / 2)
        else:
            self.node_after.position = Position(self.primary_node.position.x + DEBUG_OFFSET,
                                                (
                                                            self.primary_node.position.y - self.height / 2 + self.node_before.height / 2))

    def reposition_nodes(self):
        if self.node_before is not None:
            self.reposition_before_node()
        if self.node_after is not None:
            self.reposition_after_node()

    def to_code(self):
        code = f"% node group: {self.name}\n"
        self.reposition_nodes()
        print(self)
        if self.node_before is not None:
            code += self.node_before.draw()

        if self.node_after is not None:
            code += self.node_after.draw()

        code += self.primary_node.draw()

        code += f"% end of node group: {self.name}\n"
        return code

    def __repr__(self):
        return str(self)

    def __str__(self):
        text = f"NodeGroup: {self.name} with primary node {self.primary_node.name}"
        if self.node_before is not None:
            text += f" and node before {self.node_before.name}"
        if self.node_after is not None:
            text += f" and node after {self.node_after.name}"
        return text
