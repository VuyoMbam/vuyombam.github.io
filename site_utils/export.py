import os
from pathlib import Path

def save_preview(fig, width = 800, height = 500):
    output_dir = Path(r"C:\Users\vuyom\OneDrive\Desktop\random-website\previews")
    output_dir.mkdir(parents = True, exist_ok = True)

    # Save PNG with the article name (use stem of .qmd)
    doc_path = Path(os.environ["QUARTO_DOCUMENT_FILE"])
    article_name = doc_path.stem
    preview_path = output_dir / f"{article_name}.png"

    # Export PNG
    fig.write_image(preview_path, width = 800, height = 800)