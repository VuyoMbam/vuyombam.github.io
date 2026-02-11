# import plotly.graph_objects as go
import plotly.io as pio

pio.templates["site"] = dict(
    layout = dict(
        font = dict(
            family = "Arial, Consolas, sans-serif",
            color = "#1a1a1a",
            size = 14
        ),
        title = dict(
            font = dict(size = 18),
            x = 0,
            xanchor = "left"
        ),
        paper_bgcolor = "#000000",
        plot_bgcolor = "#000000",
        # colorway = ["#2a4f7c"],
        colorway=[
            "#2a4f7c",
            "#6b8fb4",
            "#9fbad5",
            "#c9d9ea"
        ],
        xaxis = dict(
            showgrid = True,
            gridcolor = "#e6e6e6",
            zeroline = False,
            showline = True,
            linecolor = "#cccccc",
            tickfont = dict(size=12)
        ),
        margin = dict(l=40, r=30, t=60, b=40),
        legend = dict(
            orientation = "h",
            y = -0.25,
            x = 0,
            title = None
        )
    )
)

pio.templates.default = "site"
print("PLOTLY THEME LOADED")