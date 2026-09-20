"""schema.org structured data (JSON-LD) for the homepage.

It tells search engines that the site is the personal site of one named person, and
links it to that person's other profiles, so a search for the name can recognise the
site as theirs. Built from data/profile.yml (facts) and index.qmd (the page
description) so nothing is written twice.

Used from index.qmd:

    from site_utils import structured_data
    structured_data.show()

Only facts already public on the page belong in the data (no email, phone or address).
"""

import datetime
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "profile.yml"
INDEX = ROOT / "index.qmd"


def _page_description():
    """The homepage description, straight from index.qmd's front matter."""
    front_matter = INDEX.read_text(encoding="utf-8").split("---", 2)[1]
    return yaml.safe_load(front_matter)["description"]


def graph():
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    profile = data["profile"]
    site = profile["site_url"].rstrip("/")
    page = site + "/"
    person_id, website_id, page_id = site + "/#person", site + "/#website", site + "/#profilepage"
    description = _page_description()

    person = {
        "@type": "Person",
        "@id": person_id,
        "name": profile["name"],
        "url": page,
        "image": site + profile["image"],
        "description": description,
    }

    current = next((job for job in data["experience"] if job.get("current")), None)
    if current:
        person["jobTitle"] = current["role"]
        employer = {"@type": "Organization", "name": current["org"]}
        if current.get("org_url"):
            employer["url"] = current["org_url"]
        person["worksFor"] = employer

    person["alumniOf"] = [
        {k: v for k, v in (("@type", "CollegeOrUniversity"), ("name", e["school"]), ("url", e.get("school_url"))) if v}
        for e in data["education"]
    ]
    person["knowsAbout"] = profile["knows_about"]
    person["sameAs"] = profile["same_as"]
    person["mainEntityOfPage"] = {"@id": page_id}

    website = {
        "@type": "WebSite",
        "@id": website_id,
        "url": page,
        "name": profile["site_name"],
        "alternateName": profile["alternate_site_name"],
        "inLanguage": "en",
        "publisher": {"@id": person_id},
    }

    profile_page = {
        "@type": "ProfilePage",
        "@id": page_id,
        "url": page,
        "name": f"{profile['name']} - {current['role']}" if current else profile["name"],
        "description": description,
        "dateModified": datetime.date.today().isoformat(),
        "isPartOf": {"@id": website_id},
        "about": {"@id": person_id},
        "mainEntity": {"@id": person_id},
    }

    return {"@context": "https://schema.org", "@graph": [website, profile_page, person]}


def show():
    """Print the JSON-LD as a raw HTML block for Quarto (use in a cell with `output: asis`)."""
    payload = json.dumps(graph(), ensure_ascii=False, indent=2)
    payload = payload.replace("</", "<" + chr(92) + "/")     # never let text close the script tag
    print("```{=html}")
    print('<script type="application/ld+json">')
    print(payload)
    print("</script>")
    print("```")
