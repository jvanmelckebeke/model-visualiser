from tikz.base import TikzElement
from tikz.edges.edge import Edge
from tikz.nodes.base_node import Node


class Diagram(TikzElement):
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def add_edges(self, edges: list[Edge]):
        self.edges.extend(edges)

    def get_elements(self) -> list[TikzElement]:
        return self.nodes + self.edges

    def generate_code(self):
        return "\n".join([element.to_code() for element in self.get_elements()])

    def to_code(self):
        return self.generate_code()