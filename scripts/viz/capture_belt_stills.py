# 벨트 뷰어를 UI 없이 캡처해 Phase 4 결정 행에 붙일 자기권 단면 이미지를 만든다.
"""Capture the belt viewer's cross-section as still figures, two per NearStars body.

The Phase 4 boards want the magnetosphere *inside* the magnetism row, not an
interactive viewer several screens below it. The viewer already knows how to draw
every body, so the still is a screenshot of that same canvas with the interactive
chrome switched off (`?still=1` — hides the pickers, the hover readout, the 2D/3D
switch and the slider panel), rather than a second renderer to keep in sync.

Two framings, because they answer different questions:

  close-up  the preset's own view half-width — the belts and the body, read as structure.
  shape     the whole magnetopause. Framed on the *boundary's* own length rather than on
            the body: the nose sits a few radii sunward and the tail runs tens of radii
            the other way, so a body-centred frame spends half its width on empty space
            and still shrinks the tail. Centre x is put at the midpoint of nose..tail and
            the half-width widened until any orbit ring still fits. The frame stays
            square — the figures sit side by side in a decision row and a cropped band
            would not match the close-up beside it.

Both site palettes are captured, since the boards serve figures through <picture>.

Writes docs/img/belts/nearstars/<body_key>{,_shape}.png (+ _light.png).
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


# Read the boundary's own extent out of the live viewer rather than reimplementing the
# Shue closure here: pauseNoseTail() is the same function that draws the curve.
SHAPE_FRAME = """() => {
  const v = state.view, P = state.pause;
  // the Kerbalism pause itself (the cyan boundary the game uses), not the Shue overlay:
  // a pinned Shue tail runs to hundreds of radii and would render the body as a dot.
  const nt = pauseNoseTail(P);
  const nose = nt.nose || v.R, tail = nt.tail || nose;
  const cx = (nose - tail) / 2;
  // moon rings must stay inside the frame; the parent-orbit arc passes through the body
  // at any zoom, so it needs no allowance
  let ring = 1;
  (state.moons.list || []).forEach(m => { if (m[1] > 0) ring = Math.max(ring, m[1]); });
  const R = Math.max((nose + tail) / 2, ring + Math.abs(cx)) * 1.04;
  return {R, cx};
}"""


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
                base = f"{VIEWER.as_uri()}?body={quote(label)}&variant=phys&still=1"
                page.goto(base)
                page.wait_for_timeout(900)          # first raster + resize settle
                frame = page.evaluate(SHAPE_FRAME)
                suffix = "" if theme == "dark" else "_light"
                page.query_selector(".grid .card").screenshot(
                    path=str(OUT / f"{key}{suffix}.png"))
                page.goto(f"{base}&R={frame['R']:.3f}&cx={frame['cx']:.3f}")
                page.wait_for_timeout(900)
                page.query_selector(".grid .card").screenshot(
                    path=str(OUT / f"{key}_shape{suffix}.png"))
                ctx.close()
            print(f"  ✓ {label} → {key}[_shape][_light].png"
                  f"  (shape R={frame['R']:.1f}, cx={frame['cx']:+.1f})")
        browser.close()
    print(f"→ wrote {len(bodies) * 2} stills to {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
