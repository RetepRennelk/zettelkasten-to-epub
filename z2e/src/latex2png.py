from matplotlib import figure
from matplotlib.mathtext import MathTextParser
import matplotlib.pyplot as plt

plt.rcParams.update({
    "text.usetex": True
})

def _math_to_image(s, filename_or_obj, prop=None, dpi=None, format=None):
    parser = MathTextParser('path')
    width, height, depth, _, _ = parser.parse(s, dpi=72, prop=prop)

    fig = figure.Figure(figsize=(width / 69.0, height / 69.0))
    fig.text(0, depth/height, s, fontproperties=prop)
    fig.savefig(filename_or_obj, dpi=dpi, format=format, transparent=True)

def latex2png(equation, target_file, dpi=150):
    _math_to_image(f'${equation}$', f'./.epub/{target_file}', dpi=dpi)