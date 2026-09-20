# vuyombam.github.io

Personal and portfolio website of Vuyo Mbam, built with [Quarto](https://quarto.org) and published with GitHub Pages at <https://vuyombam.github.io>.

## How publishing works

GitHub Pages serves the `docs/` folder on `main`. `docs/` is the **rendered output**, so it is committed, but it is never edited by hand. It is emptied and regenerated on every full render.

```bash
quarto render        # rebuild the whole site into docs/
quarto preview       # live preview while editing
git add -A && git commit -m "..." && git push
```

## Setup

1. Install Quarto (1.8 or newer).
2. Create a Python environment and `pip install -r requirements.txt`.
3. Render from the project root. Posts import `site_utils`, so paths are resolved relative to the project.

## Layout

| Path | What it is |
|---|---|
| `_quarto.yml` | Site config: navbar, footer, metadata, `resources` |
| `index.qmd`, `articles.qmd`, `404.qmd` | Top-level pages |
| `posts/` | Articles (each with its data and code) |
| `interviews/` | Stub pages that redirect to YouTube; they feed the homepage listing |
| `site_utils/` | Shared plotting theme and preview-image export |
| `styles.scss` | Site theme (loaded through `theme:` in `_quarto.yml`) |
| `assets/` | CV PDF and data used by the homepage chart |
| `images/`, `previews/` | Photos and article preview images |
| `docs/` | Rendered site (generated) |
| `_freeze/` | Cached results of executed code; commit it |

## Things that must survive a render

Quarto wipes `docs/`, so files that have to be present in the output live in the project root and are listed under `project: resources:` in `_quarto.yml`:

- `googlecf6de51e88026b7b.html`: Google Search Console ownership verification. Do not remove or edit.
- `robots.txt`

## Updating the footer year

The footer year range is set in `_quarto.yml` (`page-footer`).
