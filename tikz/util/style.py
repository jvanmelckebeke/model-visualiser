from tikz.base import TikzOptions


class TikzStyle(TikzOptions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_code(self):
        return str(self)

    def __str__(self):
        return f"{{{super().__str__()}}}"

    def __repr__(self):
        return str(self)


def create_node_style(color, node_distance, split_parts=10):
    return TikzStyle("rectangle split",
                     "rectangle split ignore empty parts",
                     "very thick",
                     **{
                         "rectangle split parts": split_parts,
                         "draw": f"{color}!60",
                         "fill": f"{color}!5",
                         "minimum width": "{width(\"Batch Normalisation\") + 8pt}",
                         "node distance": f"{node_distance}cm",
                         "outer sep": "0cm"
                     })
