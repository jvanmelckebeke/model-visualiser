from visualizer.backend.base import TikzElement
from visualizer.backend.edge import Edge
from visualizer.backend.node import Node
from visualizer.util.const import COLOR_MAP


class Diagram(TikzElement):
    def __init__(self):
        self.nodes = []
        self.edges = []
        super().__init__("diagram", depends_on=None)

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def add_edges(self, edges: list[Edge]):
        self.edges.extend(edges)

    @property
    def elements(self) -> list[TikzElement]:
        return self.nodes + self.edges

    @property
    def element_map(self):
        return {element.internal_name: element for element in self.elements}

    def get_drawing_order(self):

        stack_in = self.elements
        stack_out = []
        waiting_line = []

        old_len_stack_out = -1
        old_len_waiting_line = -1

        while len(stack_in) > 0 or len(waiting_line) > 0:
            if len(stack_in) > 0:
                # print(f"there are currently {len(stack_in)} elements in the stack")
                element = stack_in.pop(0)
                if len(element.depends_on) == 0:
                    # print(f"putting element {element.internal_name} on the stack")
                    stack_out.append(element.internal_name)
                else:
                    dependencies_satisfied = True
                    for dependency in element.depends_on:
                        if dependency not in stack_out:
                            dependencies_satisfied = False
                            break
                    if dependencies_satisfied:
                        stack_out.append(element.internal_name)
                    else:
                        # print(
                        # f"putting element {element.internal_name} on the waiting line, because it depends on {element.depends_on}")
                        waiting_line.append(element)

            for waiting_element in waiting_line:
                dependencies_satisfied = True
                for dependency in waiting_element.depends_on:
                    if dependency not in stack_out:
                        dependencies_satisfied = False

                        break
                if dependencies_satisfied:
                    stack_out.append(waiting_element.internal_name)
                    waiting_line.remove(waiting_element)
            # print(f"there are currently {len(waiting_line)} elements left in the waiting line")

            if old_len_stack_out == len(stack_out) and old_len_waiting_line == len(waiting_line):
                print("no progress was made on the waiting line, aborting")
                break
            old_len_stack_out = len(stack_out)
            old_len_waiting_line = len(waiting_line)
        return stack_out

    def register_color_map(self):
        code = ""

        for i, (r, g, b) in enumerate(COLOR_MAP):
            code += rf"\definecolor{{COLOR{i}}}{{RGB}}{{{r},{g},{b}}}" + "\n"
        return code

    def generate_code(self):
        drawing_order = self.get_drawing_order()
        code = self.register_color_map()

        for element_name in drawing_order:
            code += self.element_map[element_name].to_code() + "\n"

        return code

    def to_code(self):
        return self.generate_code()
