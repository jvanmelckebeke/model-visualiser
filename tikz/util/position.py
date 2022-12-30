from typing import Optional

from tikz.base import TikzArg


class Position(dict):
    def __init__(self,
                 left_of: Optional[str] = None,
                 right_of: Optional[str] = None,
                 below_of: Optional[str] = None,
                 below_right_of: Optional[str] = None,
                 below_left_of: Optional[str] = None,
                 xshift: Optional[str] = None,
                 yshift: Optional[str] = None):
        super().__init__()
        self.left_of = left_of
        self.right_of = right_of
        self.below_of = below_of
        self.below_left_of = below_left_of
        self.below_right_of = below_right_of
        self.xshift = xshift
        self.yshift = yshift

        self.update(left_of=left_of, right_of=right_of, below_of=below_of,
                    below_left_of=below_left_of, below_right_of=below_right_of,
                    xshift=xshift, yshift=yshift)

    def get_position_args(self):
        position_args = []
        if self.below_of:
            position_args.append(TikzArg("below", f"of {self.below_of}"))
        if self.right_of:
            position_args.append(TikzArg("right", f"of {self.right_of}"))
        if self.left_of:
            position_args.append(TikzArg("left", f"of {self.left_of}"))
        if self.xshift:
            position_args.append(TikzArg("xshift", f"({self.xshift})"))
        if self.yshift:
            position_args.append(TikzArg("yshift", f"({self.yshift})"))

        if self.below_left_of:
            position_args.append(TikzArg("below left", f"of {self.below_left_of}"))

        if self.below_right_of:
            position_args.append(TikzArg("below right", f"of {self.below_right_of}"))

        return position_args

    def __str__(self):
        return f"Position(left_of={self.left_of}, right_of={self.right_of}, " \
               f"below_of={self.below_of}, xshift={self.xshift}, yshift={self.yshift})"
