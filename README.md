# Model Visualizer
_yet another attempt at a decent model visualizer_

## Installation

### Requirements

- LaTeX + TikZ + pdflatex
- Python 3.6+
- graphviz
- pygraphviz
- everything else in `requirements.txt`

## Usage

```python
from visualize import visualize

canvas_width = 120  # you have to experiment
canvas_height = 120 # with these values

visualize(model, resolution=200, canvas_width=canvas_width, canvas_height=canvas_height)
```

## Examples

Examples can be found in the `demos` folder.