from tikz.base import TikzArg
from tikz.nodes.base_node import Node


class UtilityNode(Node):
    def __init__(self, name, layer, node_style="utility_node", below_of=None, right_of=None, left_of=None):
        super().__init__(name, layer, node_style=node_style, below_of=below_of, right_of=right_of, left_of=left_of)

    def generate_description_code(self):
        return f"{self._layer_type}"

    @property
    def _position_args(self):
        return super()._position_args + [TikzArg("yshift", "2cm")]
