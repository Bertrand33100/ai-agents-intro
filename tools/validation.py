"""Validation déterministe des sections d'une fiche Markdown."""

import re


REQUIRED_SECTIONS = (
    "Topic",
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Practice Exercise",
    "Common Mistakes",
    "Review Comments",
    "Final Summary",
)

_HEADING_PATTERN = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
_NUMBERING_PATTERN = re.compile(r"^\d+[.)]\s*")


def validate_required_sections(markdown: str) -> dict:
    """Vérifie que chaque section requise apparaît comme titre Markdown.

    Les titres peuvent être écrits à n'importe quel niveau Markdown et précédés
    d'un numéro (par exemple, ``## 1. Topic``). La comparaison ignore la casse.
    """

    headings = set()

    for line in markdown.splitlines():
        match = _HEADING_PATTERN.match(line)
        if not match:
            continue

        heading = _NUMBERING_PATTERN.sub("", match.group(1).strip())
        headings.add(" ".join(heading.split()).casefold())

    missing_sections = [
        section
        for section in REQUIRED_SECTIONS
        if section.casefold() not in headings
    ]

    return {
        "valid": not missing_sections,
        "missing_sections": missing_sections,
    }
