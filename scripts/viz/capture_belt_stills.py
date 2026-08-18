# 벨트 뷰어를 UI 없이 캡처해 Phase 4 결정 행에 붙일 자기권 단면 이미지를 만든다.
"""Capture the belt viewer's cross-section as a still figure, one per NearStars body.

The Phase 4 boards want the magnetosphere *inside* the magnetism row, not an
interactive viewer several screens below it. The viewer already knows how to draw
every body, so the still is a screenshot of that same canvas with the interactive
chrome switched off (`?still=1` — hides the pickers, the hover readout, the 2D/3D
switch and the slider panel), rather than a second renderer to keep in sync.

Both site palettes are captured, since the boards serve figures through <picture>.

Writes docs/img/belts/nearstars/<body_key>.png (+ _light.png).
Usage: python3 scripts/viz/capture_belt_stills.py [--bodies "Proxima Cen b" ...]
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parents[2]
VIEWER = REPO / "docs" / "belt-viewer.html"
OUT = REPO / "docs" / "img" / "belts" / "nearstars"
_PRESET_RE = re.compile(r"const PRESETS\s*=\s*(\{.*?\});", re.S)


def nearstars_bodies():
    """(label, body_key) for every non-Solar-System preset the viewer carries."""
    m = _PRESET_RE.search(VIEWER.read_text(encoding="utf-8"))
    if not m:
        sys.exit("belt-viewer.html: PRESETS not found — build it first")
    out = {}
    for p in json.loads(m.group(1)).values():
        if p.get("sys") in (None, "sol", "demo") or not p.get("label"):
            continue
        out[p["label"]] = p.get("body_key") or p["label"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bodies", nargs="*", help="subset of board body names")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright   # optional dep, capture-only

    bodies = nearstars_bodies()
    if args.bodies:
        bodies = {k: v for k, v in bodies.items() if k in args.bodies}
    OUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for label, key in bodies.items():
            for theme in ("dark", "light"):
                ctx = browser.new_context(viewport={"width": 900, "height": 760},
                                          color_scheme=theme, device_scale_factor=2)
                page = ctx.new_page()
                page.goto(f"{VIEWER.as_uri()}?body={quote(label)}&variant=phys&still=1")
                page.wait_for_timeout(900)          # first raymarch + resize settle
                card = page.query_selector(".grid .card")
                name = f"{key}.png" if theme == "dark" else f"{key}_light.png"
                card.screenshot(path=str(OUT / name))
                ctx.close()
            print(f"  ✓ {label} → {key}.png + _light.png")
        browser.close()
    print(f"→ wrote {len(bodies) * 2} stills to {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
