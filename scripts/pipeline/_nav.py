# 발행 페이지 전체가 공유하는 전역 내비게이션 정의 (단일 소스, 생성기들이 임포트)
"""Single source of the global nav shared by every published surface.

Every generator that emits a top-of-page crumb imports NAV_ITEMS / global_nav
from here, so adding a surface is a one-line change that propagates on rebuild.
Labels are language-invariant (English) on purpose: the nav is identical in
both UI languages, like the phase pills.
"""

NAV_ITEMS = [
    ("DB", "index.html"),
    ("3D Map", "starmap.html"),
    ("Reports", "reports.html"),
    ("Phase 4", "phase4/index.html"),
    ("Tools", "tools.html"),
    ("Wiki", "wiki/index.html"),
]


def global_nav(prefix: str = "", here: str = None, sep: str = " · ") -> str:
    """Render the shared nav as crumb-style inline HTML.

    prefix: relative path from the page's directory to docs/ root (e.g. "../").
    here:   label of the current surface, rendered as plain text instead of a link.
    """
    parts = []
    for label, path in NAV_ITEMS:
        if label == here:
            parts.append(f"<span>{label}</span>")
        else:
            parts.append(f'<a href="{prefix}{path}">{label}</a>')
    return sep.join(parts)


# ── the one-line global bar ──────────────────────────────────────────────────
# Self-contained (carries its own <style>), inserted right after <body> by every
# document surface. Page-specific controls stay in each page's own header below.
# Fullscreen apps (starmap, orbit3d/interactive) keep their compact toolbars.

_BAR_CSS = """<style>
.ns-bar { display:flex; align-items:center; gap:14px; flex-wrap:wrap;
  padding:9px 22px; font:12px/1 'Geist Mono','SF Mono',Menlo,monospace;
  background:rgba(10,12,18,.62); border-bottom:1px solid rgba(255,255,255,.07);
  backdrop-filter:blur(10px) }
.ns-bar .ns-brand { color:rgba(255,255,255,.94); font-weight:700;
  font-family:'Geist','Inter',system-ui,sans-serif; font-size:13px;
  text-decoration:none; letter-spacing:.2px }
.ns-bar a { color:rgba(255,255,255,.52); text-decoration:none }
.ns-bar a:hover { color:#aac8ff; text-decoration:none }
.ns-bar span.ns-here { color:rgba(255,255,255,.90) }
.ns-bar .ns-sep { color:rgba(255,255,255,.22) }
@media (prefers-color-scheme:light) { html.ns-light-ok .ns-bar {
  background:rgba(245,246,250,.72); border-bottom:1px solid rgba(12,17,34,.12) }
  html.ns-light-ok .ns-bar .ns-brand { color:rgba(9,12,22,.92) }
  html.ns-light-ok .ns-bar a { color:rgba(9,12,22,.55) }
  html.ns-light-ok .ns-bar a:hover { color:#2f66d8 }
  html.ns-light-ok .ns-bar span.ns-here { color:rgba(9,12,22,.90) }
  html.ns-light-ok .ns-bar .ns-sep { color:rgba(9,12,22,.25) } }
@media (max-width:600px) { .ns-bar { padding:8px 14px; gap:10px } }
</style>"""


def global_bar(prefix: str = "", here: str = None) -> str:
    """The uniform one-line site bar: brand + global nav. Insert after <body>.

    prefix: relative path to docs/ root. here: current surface label (plain text).
    Pages that support a light theme opt in by putting class="ns-light-ok" on <html>.
    """
    links = []
    for label, path in NAV_ITEMS:
        if label == here:
            links.append(f'<span class="ns-here">{label}</span>')
        else:
            links.append(f'<a href="{prefix}{path}">{label}</a>')
    sep = '<span class="ns-sep">·</span>'
    return (_BAR_CSS
            + f'<div class="ns-bar"><a class="ns-brand" href="{prefix}index.html">NearStars</a>'
            + sep.join(links) + '</div>')
