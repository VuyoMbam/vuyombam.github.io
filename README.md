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
| `styles-light.scss`, `styles-dark.scss` | The two themes. Each only defines colour variables, then imports the shared rules |
| `_site-components.scss` | Shared component styling (navbar, cards, buttons, chart text). Uses the theme variables, so no colours are hardcoded here |
| `assets/` | CV PDF, data for the homepage chart, and `fonts/` (self-hosted Questrial + its OFL licence) |
| `images/`, `previews/` | Photos and article preview images |
| `docs/` | Rendered site (generated) |
| `_freeze/` | Cached results of executed code; commit it |

## Design system

- **Themes:** light is the default; a toggle in the navbar switches to dark and remembers the choice. Palette: `#1E4038` forest, `#3C7F70` teal, `#5ABFA9` mint, `#6CE5CA` seafoam, `#78FFE1` aqua. Light uses forest text with teal links; dark uses aqua links on a deep green background. To change a colour, edit the variables at the top of `styles-light.scss` / `styles-dark.scss`.
- **Contrast:** every text/background pair is meant to reach 4.5:1 (3:1 for large text and chart marks). Re-check after changing colours; several palette colours (mint, seafoam, aqua) fail as text on the light theme and are only used as fills or on the dark theme.
- **Font:** [Questrial](https://fonts.google.com/specimen/Questrial), self-hosted from `assets/fonts/` (no requests to Google). It has a single regular weight, so bold is switched off (`$font-weight-bold: 400`, `font-synthesis: none`): build hierarchy with size and colour, and avoid `**bold**` in body text.
- **Charts:** colours live in `site_utils/palette.py` and are chosen to read on both themes. `site_utils/plotly_theme.py` sets transparent backgrounds and leaves text colour unset; the page's CSS (`--chart-text` in the theme files, applied in `_site-components.scss`) colours chart text for the active theme. Do not hardcode `color="white"` or `"black"` in chart code. Preview PNGs (`site_utils/export.py`) are drawn on the light background.
- **Static matplotlib images** (e.g. `functions.py`) cannot follow the toggle, so they are drawn on a light panel using `palette.teal_cmap()`.
- `posts/sa_steel_analysis/input_output_analysis.ipynb` is an exploratory notebook: its code cells use the same palette, but its saved outputs were not regenerated.

## Things that must survive a render

Quarto wipes `docs/`, so files that have to be present in the output live in the project root and are listed under `project: resources:` in `_quarto.yml`:

- `googlecf6de51e88026b7b.html`: Google Search Console ownership verification. Do not remove or edit.
- `robots.txt`

## Updating the footer year

The footer year range is set in `_quarto.yml` (`page-footer`).
