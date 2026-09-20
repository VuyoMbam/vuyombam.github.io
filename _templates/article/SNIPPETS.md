# Article snippets

Copy these into an article's `index.qmd`. This file lives in `_templates/`, which Quarto ignores, so nothing here is ever published or executed.

## Image

Save the image in the article's folder, then:

```markdown
![Caption saying what the figure shows. Source: name of the source.](figure.png){#fig-example fig-alt="Describe the figure for screen readers"}
```

Refer to it in the text with `@fig-example`. Readers can click it to enlarge.

## Chart (Plotly)

Put the data file in the article's folder. Charts follow the light/dark theme automatically as long as they use `site_utils`. Do not set font or background colours by hand.

````markdown
```{python}
#| label: fig-chart
#| fig-cap: "Caption saying what the chart shows. Source: name of the source."
import os, sys
sys.path.insert(0, os.environ["QUARTO_PROJECT_DIR"])   # lets the article import site_utils
import pandas as pd
import plotly.express as px
from site_utils import palette, plotly_theme            # registers the site's chart theme

df = pd.read_csv("data.csv")
fig = px.bar(df, x="year", y="value", color="technology",
             color_discrete_sequence=palette.CATEGORICAL)
fig.show()
```
````

Colours to use (all readable on both themes):

| For | Use |
|-----|-----|
| Categories / series | `palette.CATEGORICAL` |
| A continuous scale (maps, heat maps) | `palette.SEQUENTIAL` |
| Fuels | `palette.FUEL_COLORS` |

Charts are fixed-width unless you leave `width` unset. Leave it unset so they fit phones.

## Social-share image made from a chart

After `fig.show()`, add:

```python
from site_utils import export
export.save_preview(fig)   # writes previews/<article-name>.png (needs kaleido)
```

Then set `image: /previews/<article-name>.png` in the article's front matter.
