import numpy as np

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool


def test_line_plot():
    x = [1, 3, 5, 7, 9, 11, 13]
    y = [1, 2, 3, 4, 5, 6, 7]
    title = "y = f(x)"

    plot = figure(
        title=title,
        x_axis_label="X-Axis",
        y_axis_label="Y-Axis",
        plot_width=400,
        plot_height=400,
    )
    plot.line(x, y, legend="f(x)", line_width=2)
    return components(plot)


def test_hex_plot():
    n = 500
    x = 2 + 2 * np.random.standard_normal(n)
    y = 2 + 2 * np.random.standard_normal(n)

    plot = figure(
        title="Hexbin for 500 points",
        match_aspect=True,
        tools="wheel_zoom,reset",
        background_fill_color="#440154",
    )
    plot.grid.visible = False

    r, bins = plot.hexbin(x, y, size=0.5, hover_color="pink", hover_alpha=0.8)

    plot.circle(x, y, color="white", size=1)

    plot.add_tools(
        HoverTool(
            tooltips=[("count", "@c"), ("(q,r)", "(@q, @r)")],
            mode="mouse",
            point_policy="follow_mouse",
            renderers=[r],
        )
    )
    return components(plot)
