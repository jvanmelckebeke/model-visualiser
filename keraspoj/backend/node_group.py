from keraspoj.backend.base import TikzElement
from keraspoj.backend.misc.position import Position
from keraspoj.backend.node import Node

DEBUG_OFFSET = 0

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
                                                 (self.primary_node.position.y
                                                  + self.height / 2 - self.node_after.height / 2))

    def reposition_after_node(self):
        if self.node_after is None:
            return
        if self.node_before is None:
            self.node_after.position = Position(self.primary_node.position.x + DEBUG_OFFSET,
                                                self.primary_node.position.y - self.height / 2)
        else:
            self.node_after.position = Position(self.primary_node.position.x + DEBUG_OFFSET,
                                                (self.primary_node.position.y
                                                 - self.height / 2 + self.node_before.height / 2))

    def reposition_nodes(self):
        if self.node_before is not None:
            self.reposition_before_node()
        if self.node_after is not None:
            self.reposition_after_node()

    def to_code(self):
        code = f"% node group: {self.name}\n"
        self.reposition_nodes()
        # print(self)
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
