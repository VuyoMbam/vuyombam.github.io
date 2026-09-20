"""Builds the Experience and Education sections of the homepage from data/profile.yml.

Used from index.qmd:

    from site_utils import timeline
    timeline.show("experience")   # or "education"

All text is HTML-escaped. Styling lives in _site-components.scss.
"""

from html import escape
from pathlib import Path

import yaml

DATA = Path(__file__).resolve().parent.parent / "data" / "profile.yml"
LOGO_DIR = "/assets/logos/"


def _load():
    return yaml.safe_load(DATA.read_text(encoding="utf-8"))


def _logo(item):
    """Small logo chip; decorative (alt="") because the organisation is named in text beside it."""
    if not item.get("logo"):
        return ""
    tone = "dark" if item.get("chip") == "dark" else "light"
    src = LOGO_DIR + item["logo"]
    return f'<span class="logo-chip logo-chip--{tone}"><img src="{escape(src)}" alt="" loading="lazy"></span>'


def _dates(item):
    start, end = item.get("start"), item.get("end")
    if item.get("current"):
        return f"{escape(str(start))} - Present" if start else "Present"
    return f"{escape(str(start))} - {escape(str(end))}"


def _experience(items):
    out = ['<ol class="timeline-list">']
    for item in items:
        current = " is-current" if item.get("current") else ""
        badge = '<span class="badge-current">Current</span>' if item.get("current") else ""
        place = f" &middot; {escape(item['place'])}" if item.get("place") else ""
        points = "".join(f"<li>{escape(p)}</li>" for p in item.get("points", []))
        tags = "".join(f"<li>{escape(t)}</li>" for t in item.get("tags", []))
        out.append(
            f'<li class="timeline-item{current}">'
            '<span class="timeline-dot" aria-hidden="true"></span>'
            '<div class="timeline-card">'
            '<div class="timeline-head">'
            f"{_logo(item)}"
            '<div class="timeline-title">'
            f"<h3>{escape(item['role'])}</h3>"
            f'<p class="timeline-org">{escape(item["org"])}{place}</p>'
            "</div>"
            f'<p class="timeline-date">{_dates(item)}{badge}</p>'
            "</div>"
            f'<ul class="timeline-points">{points}</ul>'
            + (f'<ul class="chips">{tags}</ul>' if tags else "")
            + "</div></li>"
        )
    out.append("</ol>")
    return "".join(out)


def _education(items):
    cards = []
    for item in items:
        place = f" &middot; {escape(item['place'])}" if item.get("place") else ""
        grade = (
            f'<span class="badge-honours"><i class="bi bi-award" aria-hidden="true"></i> {escape(item["grade"])}</span>'
            if item.get("grade")
            else ""
        )
        highlights = "".join(
            f'<li><i class="bi bi-star-fill" aria-hidden="true"></i><span>{escape(h)}</span></li>'
            for h in item.get("highlights", [])
        )
        cards.append(
            '<div class="g-col-12 g-col-md-6">'
            '<article class="edu-card">'
            '<div class="edu-head">'
            f"{_logo(item)}"
            '<div class="edu-title">'
            f"<h3>{escape(item['degree'])}</h3>"
            f'<p class="edu-school">{escape(item["school"])}{place}</p>'
            "</div></div>"
            f'<p class="edu-meta"><span class="edu-years">{escape(str(item.get("years", "")))}</span>{grade}</p>'
            f'<ul class="edu-highlights">{highlights}</ul>'
            "</article></div>"
        )
    return '<div class="grid edu-grid">' + "".join(cards) + "</div>"


def html(section):
    data = _load()
    if section == "experience":
        return _experience(data["experience"])
    if section == "education":
        return _education(data["education"])
    raise ValueError(f"Unknown section: {section!r}")


def show(section):
    """Print the section as a raw HTML block for Quarto (use in a cell with `output: asis`)."""
    print("```{=html}")
    print(html(section))
    print("```")
