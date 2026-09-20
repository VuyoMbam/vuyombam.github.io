"""Show Plotly charts without any third-party requests.

Quarto's default Plotly output loads plotly.js, requirejs and MathJax from public CDNs
(and the MathJax scripts carry no integrity check). Use `show(fig)` instead of
`fig.show()`: it loads plotly.js from this site (assets/vendor/), once per page, and
leaves out MathJax, which the charts do not use.

    from site_utils import charts
    charts.show(fig)                                   # or charts.show(fig, config={"displayModeBar": False})

Refresh the vendored plotly.js after upgrading the plotly package:

    python -c "from site_utils import charts; print(charts.vendor_plotlyjs())"
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR_DIR = ROOT / "assets" / "vendor"
_loader_emitted = False


def _plotlyjs_filename():
    from plotly.offline import get_plotlyjs_version

    return f"plotly-{get_plotlyjs_version()}.min.js"


def vendor_plotlyjs():
    """Write the plotly.js bundled with the installed plotly package to assets/vendor/."""
    from plotly.offline import get_plotlyjs

    VENDOR_DIR.mkdir(parents=True, exist_ok=True)
    target = VENDOR_DIR / _plotlyjs_filename()
    target.write_text(get_plotlyjs(), encoding="utf-8")
    return target


def show(fig, config=None):
    """Display `fig` as an interactive chart (use in a Quarto Python cell)."""
    global _loader_emitted
    from IPython.display import Markdown, display

    name = _plotlyjs_filename()
    if not (VENDOR_DIR / name).exists():
        raise FileNotFoundError(
            f"{name} is missing from assets/vendor/. Run: "
            'python -c "from site_utils import charts; print(charts.vendor_plotlyjs())"'
        )

    chart = fig.to_html(
        full_html=False,
        include_plotlyjs=False,
        include_mathjax=False,
        default_width="100%",
        config=config,
    )
    loader = ""
    if not _loader_emitted:
        loader = f'<script src="/assets/vendor/{name}" charset="utf-8"></script>'
        _loader_emitted = True
    # Emitted as a raw HTML block inside markdown output. (Plain text/html output makes Quarto
    # add requirejs and jQuery to the page, which the chart does not need.)
    display(Markdown("```{=html}\n" + loader + chart + "\n```"))
