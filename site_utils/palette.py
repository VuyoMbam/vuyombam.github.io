"""Single source of truth for chart colours.

The site has a light and a dark theme (see styles-light.scss / styles-dark.scss).
Charts are drawn once and shown on both, so:

* Marks (bars, links, nodes, fills) use mid-tone colours that keep >= 3:1
  contrast against BOTH page backgrounds.
* Text cannot satisfy 4.5:1 on both, so charts leave text colour to the page's
  CSS (`--chart-text`, set per theme). Static exports (preview PNGs) use the
  explicit LIGHT values below instead.

Brand palette: https://color.adobe.com/ (5ABFA9, 3C7F70, 78FFE1, 1E4038, 6CE5CA)
"""

FOREST = "#1E4038"
TEAL = "#3C7F70"
MINT = "#5ABFA9"
SEAFOAM = "#6CE5CA"
AQUA = "#78FFE1"

FONT_FAMILY = "Questrial, 'Segoe UI', Helvetica, Arial, sans-serif"

# Explicit colours for places CSS cannot reach (e.g. PNG previews via kaleido).
LIGHT = dict(bg="#F7FCFA", text=FOREST, muted="#4F6B64")
DARK = dict(bg="#0B1512", text="#E6F5F1", muted="#9DB8B0")

# Neutral used for gridlines and axis lines: readable on both backgrounds.
NEUTRAL = "#7D8A86"
GRID = "rgba(125, 138, 134, 0.35)"

# Light-to-dark teal ramp for continuous data (maps, treemaps, heat maps).
SEQUENTIAL = ["#E6FBF6", SEAFOAM, MINT, TEAL, FOREST]

# Ordered categories in green, for things that go low -> medium -> high (scenarios, tiers).
# Runs from a light leaf green to a deep teal, so it echoes the site's greens. The band of
# greens that keeps >= 3:1 on BOTH themes is narrow (the brand's mint/aqua vanish on light,
# and forest vanishes on dark), so the hue drifts toward teal as it darkens to keep the steps
# clearly distinct (colour difference >= 24 between neighbours).
GREENS = ["#439D4B", "#3A8861", "#31726D"]

# Categorical series. Each is >= 3:1 on both LIGHT["bg"] and DARK["bg"].
CATEGORICAL = [TEAL, "#3F6FE0", "#C4801A", "#D4503C", NEUTRAL, "#8E5BD0"]

# Fuel colours for energy balance charts. Fuel-specific hues (grey coal,
# blue electricity, ...) are kept so readers can decode them at a glance;
# each was adjusted to pass 3:1 on both themes.
FUEL_COLORS = {
    "Coal": "#7D8A86",
    "Crude oil": "#A0522D",
    "Oil products": "#D97A1E",
    "Natural gas": "#5C87B3",
    "Nuclear": "#9A32CD",
    "Hydro": "#1B8DC4",
    "Geo-therm., Solar etc.": "#228B22",
    "Biofuels and Waste": "#AD8504",
    "Electricity": "#3F6FE0",
    "Heat": "#DE5A42",
}

# Node colours for the three stages of an energy-balance Sankey.
NODE_PRIMARY = NEUTRAL
NODE_TRANSFORMATION = TEAL
NODE_FINAL = "#B87A3D"


def hex_to_rgba(hex_color, alpha=0.6):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def teal_cmap():
    """Matplotlib colormap matching SEQUENTIAL (import is deferred so plotly-only pages stay light)."""
    from matplotlib.colors import LinearSegmentedColormap

    return LinearSegmentedColormap.from_list("site_teal", SEQUENTIAL)
