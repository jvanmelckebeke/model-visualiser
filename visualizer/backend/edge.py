from visualizer.backend.base import TikzElement, TikzOptions
from visualizer.util.tools import latexify


class Edge(TikzElement):
    def __init__(self, from_node, to_node, label="",
                 color="black",
                 edge_style="defaultEdge", label_style="defaultLabel",
                 extra_args: TikzOptions = TikzOptions()):
        self.from_node = from_node
        self.to_node = to_node
        self.label = label
        self.edge_style = edge_style
        self.label_style = label_style
        self.extra_style = extra_args
        self.color = color
        # super().__init__(f"edge_{from_node}_{to_node}", depends_on=[from_node, to_node])
        super().__init__(f"edge_{from_node}_{to_node}", depends_on=[])

    def draw(self):
        return self.to_code()

    def to_code(self):
        from_node = latexify(self.from_node)
        to_node = latexify(self.to_node)

        out = f"% edge from {from_node} to {to_node}\n"

        self.extra_style.add_option("draw", self.color)
        if self.color == 'black':
            self.extra_style.add_option('line width', '1pt')
        else:
            self.extra_style.add_option('line width', '1.6pt')
        style_str = f"-Stealth, {self.edge_style}"
        if self.extra_style is not None:
            style_str += f", {self.extra_style.to_code()}"
        out += rf"\draw[{style_str}] ({from_node}) " \
               rf"to node [{self.label_style}] {{{self.label}}} ({to_node});"
        return out + "\n"

    def __str__(self):
        return f"edge from {self.from_node} to {self.to_node} with label {self.label}"
