"""Default Plotly template for the site ("site").

Importing this module registers the template and makes it the default.

Backgrounds are transparent so charts sit on whichever theme (light or dark) the
visitor has chosen, and text colour is left unset: the page's CSS supplies it
via `--chart-text` (see _site-components.scss). Mark colours come from
`site_utils.palette` and are chosen to read on both themes.
"""

import plotly.io as pio

from site_utils import palette

_axis = dict(
    showgrid=True,
    gridcolor=palette.GRID,
    zeroline=False,
    showline=True,
    linecolor=palette.NEUTRAL,
    tickfont=dict(size=12),
)

pio.templates["site"] = dict(
    layout=dict(
        font=dict(
            family=palette.FONT_FAMILY,
            size=14,
        ),
        title=dict(
            font=dict(size=18),
            x=0,
            xanchor="left",
        ),
        hoverlabel=dict(font=dict(family=palette.FONT_FAMILY)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=palette.CATEGORICAL,
        colorscale=dict(
            sequential=[
                [i / (len(palette.SEQUENTIAL) - 1), c]
                for i, c in enumerate(palette.SEQUENTIAL)
            ],
        ),
        xaxis=_axis,
        yaxis=_axis,
        margin=dict(l=40, r=30, t=60, b=40),
        legend=dict(
            orientation="h",
            y=-0.25,
            x=0,
            title=None,
        ),
    ),
    # Sankey traces take their tooltip font from the trace, not the layout
    data=dict(sankey=[dict(hoverlabel=dict(font=dict(family=palette.FONT_FAMILY)))]),
)

pio.templates.default = "site"
