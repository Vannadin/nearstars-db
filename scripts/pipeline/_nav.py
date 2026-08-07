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
