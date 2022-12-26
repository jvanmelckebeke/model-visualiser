from layer_tools import str_shape
from tikz.base import TikzArg, TikzOptions, TikzElement


class Node(TikzElement):
    def __init__(self, name, layer, node_style="default_node",
                 below_of=None, right_of=None, left_of=None):
        self.name = name
        self.layer = layer

        self.below_of = below_of
        self.right_of = right_of
        self.left_of = left_of
        self.node_style = node_style

    def set_position(self, below_of=None, right_of=None, left_of=None):
        self.below_of = below_of
        self.right_of = right_of
        self.left_of = left_of

    def draw(self):
        return self.__str__()

    def generate_position_code(self):

        position_args = TikzOptions(*self._position_args)

        return rf"[{position_args}]"

    @property
    def _position_args(self):
        position_args = []
        if self.below_of:
            position_args.append(TikzArg("below", f"of {self.below_of}"))
        if self.right_of:
            position_args.append(TikzArg("right", f"of {self.right_of}"))
        if self.left_of:
            position_args.append(TikzArg("left", f"of {self.left_of}"))
        return position_args

    @property
    def _layer_type(self):
        return self.layer.__class__.__name__

    @property
    def _layer_shape(self):
        return str_shape(self.layer.output_shape)

    def generate_description_code(self):
        return fr"{self._layer_type}\nodepart{{two}}output shape: {self._layer_shape}"

    def __str__(self):

        position_args = self.generate_position_code()

        layer_description = self.generate_description_code()

        return rf"\node[{self.node_style}] {position_args} ({self.name}) {{{layer_description}}};" + "\n"

    def to_code(self):
        return str(self)
