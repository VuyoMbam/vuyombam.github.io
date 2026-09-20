"""Start a new article from the template.

    python new_article.py "Title of the article"
    python new_article.py "Title of the article" --slug short-url-name

Creates posts/<slug>/index.qmd (with today's date filled in) and prints how to
preview it. Nothing else in the project is touched.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "_templates" / "article" / "index.qmd"


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "new-article"


def main():
    parser = argparse.ArgumentParser(description="Create a new article from the template.")
    parser.add_argument("title", help="Article title, in quotes")
    parser.add_argument("--slug", help="Folder / URL name (default: made from the title)")
    args = parser.parse_args()

    slug = slugify(args.slug or args.title)
    folder = ROOT / "posts" / slug
    target = folder / "index.qmd"
    if target.exists():
        sys.exit(f"{target.relative_to(ROOT)} already exists; pick another --slug.")

    title = args.title.replace("\\", "\\\\").replace('"', '\\"')
    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace("Working title of the article", title, 1)
    text = text.replace("{{date}}", date.today().isoformat(), 1)

    folder.mkdir(parents=True)
    target.write_text(text, encoding="utf-8", newline="\n")

    rel = target.relative_to(ROOT).as_posix()
    print(f"Created {rel}")
    print(f"Preview it:   quarto preview {rel}")
    print("It stays a draft (left out of the site) until you delete the `draft: true` line.")


if __name__ == "__main__":
    main()
