from visualizer.backend.base import TikzElement


class Document:
    def __init__(self):
        self.styles = {}
        self.latex_elements: list[TikzElement] = []

    def add_styles(self, styles):
        self.styles = styles

    def add_style(self, style_name, style: TikzElement):
        self.styles[style_name] = style

    @property
    def _styles_code(self):
        out = ""
        for style_name, style in self.styles.items():
            out += f"% style: {style_name}\n"
            out += rf"\tikzstyle{{{style_name}}}=[{style.to_code()}]" + "\n"
        return out

    def generate_header(self):
        return "\\documentclass{standalone}\n" \
               "\\usepackage{xcolor}\n" \
               "\\usepackage{tikz}\n" \
               "\\usetikzlibrary{positioning, shapes.multipart, calc, graphs, graphs.standard}\n" \
               "\\begin{document}\n" \
               "\\begin{tikzpicture}\n" \
               f"{self._styles_code}\n"

    def generate_footer(self):
        return r"\end{tikzpicture}" \
               r"\end{document}"

    def add_element(self, element: TikzElement):
        self.latex_elements.append(element)

    def add_elements(self, elements: list[TikzElement]):
        self.latex_elements.extend(elements)

    def generate_code(self):
        return \
                self.generate_header() + \
                "\n".join([element.to_code() for element in self.latex_elements]) + \
                self.generate_footer()
