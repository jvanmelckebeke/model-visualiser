from tikz.nodes.base_node import Node


class TrainableNode(Node):
    def __init__(self, name, layer, node_style="trainable_node", below_of=None, right_of=None, left_of=None):
        super().__init__(name, layer, node_style=node_style, below_of=below_of, right_of=right_of, left_of=left_of)
