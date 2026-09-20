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
| `posts/` | Articles, one folder each (`posts/<slug>/index.qmd`). `posts/_metadata.yml` holds the defaults they all share |
| `_templates/article/` | The article template and a cheat sheet of image/chart snippets. Ignored by Quarto (leading `_`), so never published |
| `new_article.py` | Creates a new article folder from the template |
| `interviews/` | Stub pages that redirect to YouTube; they feed the homepage listing |
| `site_utils/` | Shared plotting theme and preview-image export |
| `styles-light.scss`, `styles-dark.scss` | The two themes. Each only defines colour variables, then imports the shared rules |
| `_site-components.scss` | Shared component styling (navbar, cards, buttons, chart text). Uses the theme variables, so no colours are hardcoded here |
| `assets/` | Data for the homepage chart, and `fonts/` (self-hosted Questrial + its OFL licence) |
| `images/`, `previews/` | Photos and article preview images |
| `docs/` | Rendered site (generated) |
| `_freeze/` | Cached results of executed code; commit it |

## Writing an article

Articles need no formatting work: the template is already styled for both themes.

```bash
python new_article.py "Title of the article"      # creates posts/<slug>/index.qmd
quarto preview posts/<slug>/index.qmd              # live preview while writing
```

1. Edit `posts/<slug>/index.qmd`. Fill in the front matter (`title`, `description`, `categories`; optionally `image`, `featured`), then replace the sample text. Delete any block you do not need.
2. **Publish** by deleting the `draft: true` line, then `quarto render`, commit and push.

Things to know:

- **Drafts** (`draft: true`) appear in `quarto preview` but are left out of the site's listings, search and sitemap. The built site still gets an empty page at the draft's address, and **the draft's source is public in the GitHub repo**, so keep anything confidential out of drafts.
- **LinkedIn extracts:** use the `.linkedin-post` box (in the template) and link to the original post.
- **Images and charts:** copy from `_templates/article/SNIPPETS.md`. Charts import `site_utils`, so they follow the light/dark theme and use the palette.
- **Homepage:** an article with `featured: true` also appears under "Featured Articles" (the two newest show). With no articles yet, that section hides itself and the Articles page says articles are on the way.
- **Style:** the font has one weight, so `**bold**` does nothing; use headings, lists and callouts. Do not hardcode colours.
- **Description:** about 150 characters. It appears on the article card, in Google and in link previews.

## Contact form

The homepage ends with a "Get in touch" form. GitHub Pages has no server, so the form sends its message through [Web3Forms](https://web3forms.com), which emails it to you. There is also a plain email link next to it as a fallback.

**One-time setup:**

1. Go to web3forms.com and request an access key for the inbox that should receive messages. The key is designed to be public, so it is safe to keep in the repo.
2. In `index.qmd`, replace `PASTE_YOUR_WEB3FORMS_ACCESS_KEY_HERE` in the form's `data-access-key` attribute with the key.
3. `quarto render`, commit and push. Then send yourself a test message and check your spam folder.

Until a key is set, the form stays hidden and visitors only see the email link. The address for that link is set in the script at the bottom of the contact section (`CONTACT_EMAIL`); it is assembled in JavaScript so it does not appear in the page source for scrapers. If the form service is ever down or the send fails, the page tells the visitor to email you directly.

The topic dropdown ("A job opportunity", "Requesting your CV", ...) is included in the email subject, so you can triage at a glance. The CV is no longer downloadable from the site; people ask for it here.

## Design system

- **Themes:** light is the default; a toggle in the navbar switches to dark and remembers the choice. Palette: `#1E4038` forest, `#3C7F70` teal, `#5ABFA9` mint, `#6CE5CA` seafoam, `#78FFE1` aqua. Light uses forest text with teal links; dark uses aqua links on a deep green background. To change a colour, edit the variables at the top of `styles-light.scss` / `styles-dark.scss`.
- **Contrast:** every text/background pair is meant to reach 4.5:1 (3:1 for large text and chart marks). Re-check after changing colours; several palette colours (mint, seafoam, aqua) fail as text on the light theme and are only used as fills or on the dark theme.
- **Font:** [Questrial](https://fonts.google.com/specimen/Questrial), self-hosted from `assets/fonts/` (no requests to Google). It has a single regular weight, so bold is switched off (`$font-weight-bold: 400`, `font-synthesis: none`): build hierarchy with size and colour, and avoid `**bold**` in body text.
- **Charts:** colours live in `site_utils/palette.py` and are chosen to read on both themes. `site_utils/plotly_theme.py` sets transparent backgrounds and leaves text colour unset; the page's CSS (`--chart-text` in the theme files, applied in `_site-components.scss`) colours chart text for the active theme. Do not hardcode `color="white"` or `"black"` in chart code. Preview PNGs (`site_utils/export.py`) are drawn on the light background.
- **Static matplotlib images** (e.g. `functions.py`) cannot follow the toggle, so they are drawn on a light panel using `palette.teal_cmap()`.

## Things that must survive a render

Quarto wipes `docs/`, so files that have to be present in the output live in the project root and are listed under `project: resources:` in `_quarto.yml`:

- `googlecf6de51e88026b7b.html`: Google Search Console ownership verification. Do not remove or edit.
- `robots.txt`

## Updating the footer year

The footer year range is set in `_quarto.yml` (`page-footer`).
