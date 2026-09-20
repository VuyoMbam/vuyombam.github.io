import os
from pathlib import Path

import plotly.graph_objects as go

from site_utils import palette


def _light_copy(fig):
    """Copy of `fig` with explicit light-theme colours.

    Charts on the site leave text colour to the page's CSS, which a static PNG
    cannot use, so previews (used as social-share images) are drawn on the
    light theme's background instead.
    """
    fig = go.Figure(fig)
    fig.update_layout(
        font_color=palette.LIGHT["text"],
        paper_bgcolor=palette.LIGHT["bg"],
        plot_bgcolor=palette.LIGHT["bg"],
    )
    fig.update_annotations(font_color=palette.LIGHT["muted"])
    return fig


def save_preview(fig, width = 800, height = 500):
    output_dir = Path(__file__).resolve().parent.parent / "previews"
    output_dir.mkdir(parents = True, exist_ok = True)

    # Save PNG with the article name (use stem of .qmd)
    doc_path = Path(os.environ["QUARTO_DOCUMENT_FILE"])
    article_name = doc_path.stem
    preview_path = output_dir / f"{article_name}.png"

    # Export PNG
    _light_copy(fig).write_image(preview_path, width = 800, height = 800)
