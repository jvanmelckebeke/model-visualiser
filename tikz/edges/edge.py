from tikz.base import TikzElement


class Edge(TikzElement):
    def __init__(self, from_node, to_node, label="", edge_style="default_edge", label_style="default_label"):
        self.from_node = from_node
        self.to_node = to_node
        self.label = label
        self.edge_style = edge_style
        self.label_style = label_style

    def draw(self):
        return self.__str__()

    def to_code(self):
        return str(self)
    def __str__(self):
        return rf"\draw[->, {self.edge_style}] ({self.from_node}) " \
               rf"to node [{self.label_style}] {{{self.label}}} ({self.to_node});" + "\n "
