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