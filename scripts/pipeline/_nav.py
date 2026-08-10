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

# ── the one segmented-control spec (language toggles + filter segments) ──────
# Shipped inside the bar's <style>, which is injected after <body> and therefore
# wins over page-local rules. Fullscreen apps without the bar (starmap, orbit3d)
# carry a verbatim copy — keep the two in sync.
SEG_CSS = """
/* .seg.seg = 특이도 상향: 본문 내 <style> 를 가진 페이지에서도 정본이 이긴다 */
.seg.seg { display:inline-flex; padding:2px; gap:2px; flex-shrink:0;
  background:rgba(255,255,255,.022); border:1px solid rgba(255,255,255,.09);
  border-radius:8px }
.seg.seg button { background:transparent; border:none; cursor:pointer;
  padding:5px 10px; border-radius:6px; white-space:nowrap;
  color:rgba(255,255,255,.56);
  font:500 12px/1 'Geist','Inter',system-ui,sans-serif }
.seg.seg button:hover { color:rgba(255,255,255,.80) }
.seg.seg button.on { background:rgba(255,255,255,.07); color:rgba(255,255,255,.94) }
@media (prefers-color-scheme:light) { html.ns-light-ok .seg.seg {
  background:rgba(12,17,34,.03); border-color:rgba(12,17,34,.12) }
  html.ns-light-ok .seg.seg button { color:rgba(9,12,22,.62) }
  html.ns-light-ok .seg.seg button:hover { color:rgba(9,12,22,.80) }
  html.ns-light-ok .seg.seg button.on { background:rgba(12,17,34,.08);
    color:rgba(9,12,22,.92) } }
/* 모바일: 세그먼트 버튼이 24px 였다 → 44px 터치 타깃 */
@media (max-width:700px) {
  .seg.seg button { min-height:40px; min-width:44px; justify-content:center;
    display:inline-flex; align-items:center; font-size:13px; padding:0 12px }
}"""

# ── site-wide accessibility floor ────────────────────────────────────────────
# Keyboard focus was invisible everywhere before 2026-08-10 (no :focus rule on
# 269/272 pages), and only one page honoured prefers-reduced-motion. Both are
# global concerns, so they ride with the bar like SEG_CSS does.
A11Y_CSS = """
:focus-visible { outline:2px solid #7aa8ff; outline-offset:2px; border-radius:4px }
@media (prefers-color-scheme:light) {
  html.ns-light-ok :focus-visible { outline-color:#114edd } }
@media (prefers-reduced-motion:reduce) {
  *, *::before, *::after { animation-duration:.01ms !important;
    animation-iteration-count:1 !important; transition-duration:.01ms !important;
    scroll-behavior:auto !important } }"""

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
  html.ns-light-ok .ns-bar a { color:rgba(9,12,22,.62) }
  html.ns-light-ok .ns-bar a:hover { color:#114edd }
  html.ns-light-ok .ns-bar span.ns-here { color:rgba(9,12,22,.90) }
  html.ns-light-ok .ns-bar .ns-sep { color:rgba(9,12,22,.25) } }
/* 모바일: 두 줄로 접히고 링크가 13px 높이였다 → 한 줄 가로 스크롤 + 44px 터치 타깃.
   구분점은 폭만 먹으므로 감추고, 브랜드는 왼쪽에 고정해 되돌아갈 곳을 남긴다. */
@media (max-width:700px) {
  .ns-bar { gap:0; padding:0 0 0 12px; flex-wrap:nowrap; overflow-x:auto;
    overscroll-behavior-x:contain; -webkit-overflow-scrolling:touch;
    scrollbar-width:none; align-items:stretch }
  .ns-bar::-webkit-scrollbar { display:none }
  .ns-bar > * { flex-shrink:0 }
  .ns-bar .ns-sep { display:none }
  .ns-bar .ns-brand { position:sticky; left:0; z-index:1; display:flex; align-items:center;
    padding-right:12px; background:linear-gradient(90deg,rgba(10,12,18,.92) 70%,transparent) }
  .ns-bar a:not(.ns-brand), .ns-bar span.ns-here {
    display:flex; align-items:center; min-height:44px; padding:0 11px }
  .ns-bar span.ns-here { box-shadow:inset 0 -2px 0 #7aa8ff }
}
@media (max-width:700px) and (prefers-color-scheme:light) {
  html.ns-light-ok .ns-bar .ns-brand {
    background:linear-gradient(90deg,rgba(245,246,250,.94) 70%,transparent) }
  html.ns-light-ok .ns-bar span.ns-here { box-shadow:inset 0 -2px 0 #114edd }
}
""" + SEG_CSS + A11Y_CSS + """
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
