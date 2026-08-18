# 호스트/행성 이름을 슬러그·파일명으로 정규화하는 단일 진실원
"""Canonical name normalization for the NearStars pipeline.

All builders that derive a slug or filename from a star/planet name
import from here. Keeping the definitions in one place prevents the
divergence that caused commit e0da593 ("barnards-star" vs
"barnard-s-star" producing two file-naming worlds).

Rules:
  1. lowercase
  2. strip apostrophes (so `Barnard's` → `barnards`, not `barnard-s`)
  3. non-alphanumeric runs collapse to a single separator
  4. trim leading/trailing separators

Two separator conventions:
  - URL slug uses '-' (web-friendly): `barnards-star`, `trappist-1`
  - File slug uses '_' (db/systems/*.json convention): `barnards_star`,
    `trappist_1`

Examples (canonical):
  "Barnard's star"   → url:barnards-star    file:barnards_star
  "Teegarden's Star" → url:teegardens-star  file:teegardens_star
  "TRAPPIST-1"       → url:trappist-1       file:trappist_1
  "Alpha Centauri A" → url:alpha-centauri-a file:alpha_centauri_a
  "Delta Pavonis"    → url:delta-pavonis    file:delta_pavonis
  "40 Eridani A"     → url:40-eridani-a     file:40_eridani_a
  "tau Cet"          → url:tau-cet          file:tau_cet

If you write a new builder that names files from host or planet names,
import `to_url_slug` or `to_file_slug` from this module. Do NOT
re-implement the rules — they will drift.
"""
import re


def _canonical(name: str, sep: str) -> str:
    s = name.lower()
    s = s.replace("'", "")
    s = re.sub(r"[^a-z0-9]+", sep, s)
    return s.strip(sep)


def to_url_slug(name: str) -> str:
    """Canonical web slug — separator '-'.

    Used by docs/phase2/*.html, docs/phase3/*.html, reports-manifest.json.
    """
    return _canonical(name, "-")


def to_file_slug(name: str) -> str:
    """Canonical filename slug — separator '_'.

    Used by db/systems/*.json filenames (build_systems.py wraps this with
    a '.json' suffix as to_filename).
    """
    return _canonical(name, "_")


def to_filename(name: str) -> str:
    """db/systems/<...>.json filename. Thin wrapper over to_file_slug."""
    return to_file_slug(name) + ".json"




def to_kopernicus_name(designation: str) -> str:
    """Canonical Kopernicus body `name` — the formal designation, verbatim.

    This is the identifier every cfg writer joins on, so it has to be unique across the
    whole mod and stable once shipped. Three rules, one reason each:

      1. **The formal designation, never the culture name.** `Alpha Centauri A b III`,
         not `Pandora`. The in-game label is a separate Kopernicus field
         (`Properties { displayName }`), so the internal name is free to carry the
         designation and should.
      2. **The whole designation, not its tail.** The tail alone collides:
         `Alpha Centauri A b` and `40 Eridani A b` both reduce to `A b`, and their moons
         would both be `A b I` (2026-08-18 audit). The system prefix is what makes it
         unique.
      3. **Verbatim, including case.** The satellite numeral stays upper case, per
         CONVENTIONS §5.2b (`A b I`–`A b V`) and IAU satellite practice (`Jupiter I` =
         Io). The stellar component is upper case and the planet letter lower case for
         the same reason: that is what the designation already is.

    So this is deliberately an identity function. It exists so that writers have one
    place to import rather than each inventing a transform, and so the rules above sit
    next to the thing they govern.

    Examples:
      "Alpha Centauri A b III" → "Alpha Centauri A b III"
      "40 Eridani A b"         → "40 Eridani A b"
      "Proxima Centauri c I"   → "Proxima Centauri c I"
    """
    return designation.strip()
