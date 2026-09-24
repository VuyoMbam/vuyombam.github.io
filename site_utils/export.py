import os
from pathlib import Path

import plotly.graph_objects as go

from site_utils import palette


def _light_copy(fig, title=None):
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
    if title:
        fig.update_layout(title_text=title, title_font_size=28)
    return fig


def save_preview(fig, width = 1200, height = 630, title = None):
    """Save `fig` as previews/<article>.png (the default size suits link previews and cards).

    The file is named after the article's folder (posts/<article>/index.qmd), or after the
    .qmd file itself for a page that is not called index.qmd. Point the article's `image:`
    front matter at /previews/<article>.png. `title` adds a heading inside the picture, which
    is useful because a shared preview appears without the page's caption.
    """
    output_dir = Path(__file__).resolve().parent.parent / "previews"
    output_dir.mkdir(parents = True, exist_ok = True)

    # Quarto gives the file name (QUARTO_DOCUMENT_FILE) and its folder (QUARTO_DOCUMENT_PATH) separately
    doc_file = Path(os.environ["QUARTO_DOCUMENT_FILE"])
    doc_folder = Path(os.environ.get("QUARTO_DOCUMENT_PATH", ".")).resolve()
    article_name = doc_folder.name if doc_file.stem == "index" else doc_file.stem
    preview_path = output_dir / f"{article_name}.png"

    _light_copy(fig, title).write_image(preview_path, width = width, height = height)
