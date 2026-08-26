# DB 의 암석 행성을 증거 등급으로 갈라 솔버에 먹인다 — 무엇이 풀리고 무엇이 왜 안 풀리는가
"""Survey the rocky planets in `db/systems` through the interior solver.

    python3 engine/rocky_roster.py            등급별 표
    python3 engine/rocky_roster.py --md       문서용 마크다운 표

위성 로스터(`test_interior.py` 의 `ROSTER`)는 손으로 친 표다. 보드가 선언한 것을
같이 들고 다녀야 해서 그렇다. 이쪽은 다르다 — **측정된 외계행성** 이고 값이
`db/systems/*.json` 에 이미 있으므로, 손으로 옮겨 적으면 그 순간 두 번째 사본이 된다.
그래서 읽는다.

왜 등급을 가르나
----------------
역산은 질량과 반지름 **둘 다 측정됐을 때만** 조성을 말한다. 그런데 DB 의 암석 행성
대부분은 그렇지 않고, 그 사실이 필드 하나에 드러난다.

    TRAPPIST-1 b    Transit          Mass     R 1.116 ± 0.014
    Barnard b       Radial Velocity  Msini    R 0.720 ± None

**오차 없는 반지름은 측정이 아니다.** Barnard 와 Proxima 의 행성은 통과를 하지 않으므로
반지름이 관측될 수 없고, DB 에 있는 값은 어딘가의 질량-반지름 관계식이 낸 추정이다.
거기에 역산을 걸면 그 관계식이 가정한 조성을 그대로 되돌려받는다 — 순환이다. 실제로
그 서명이 보인다. Barnard 네 행성이 전부 핵질량분율 0.23~0.26 에 뭉친다.

그리고 `Msini` 는 하한이다. 궤도 경사가 미지라 참질량은 이보다 크고, 질량이 커지면
같은 반지름에서 필요한 금속이 늘어난다. 그래서 이 등급에서 나온 핵질량분율은 방향이
있는 하한이지 값이 아니다.

이 파일이 하는 일은 그 구분을 **표에 세우는 것** 이다. 셋을 한 칸에 섞으면 "17개 중
16개가 풀렸다" 같은 문장이 나오고, 그건 사실이지만 오도한다.
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from interior import (EARTH_MASS_KG, EARTH_RADIUS_M,  # noqa: E402
                      infer_composition, solve)

DB = Path(__file__).resolve().parent.parent / "db" / "systems"

# 훑을 계. 인계문의 "암석 로스터" 넷이고, 구현 후보 로스터에서 암석 행성을 가진 것들이다.
SYSTEMS = ("40_eridani", "barnards_star", "proxima_cen", "trappist_1")

# 이 위는 암석 행성이 아니다. 넘기면 솔버가 규산염으로 풀려다 상한에 걸리고, 그 거절이
# "고압 규산염이 없다" 로 읽히는데 실제로는 "이건 암석이 아니다" 다.
ROCKY_MAX_ME = 20.0

# 증거 등급. 순서가 곧 신뢰 순서다.
MEASURED = "measured"        # 통과로 반지름, 실질량
ESTIMATED = "estimated"      # 반지름이 추정 — 역산이 순환이다
MASS_ONLY = "mass-only"      # 반지름이 없다 — 순방향만


def grade(raw: dict) -> str:
    """검출 방식과 오차의 유무에서 증거 등급을 읽는다.

    **오차의 유무가 판정한다.** 검출 방식 문자열은 DB 안에서 표기가 갈린다
    ('rv' / 'Radial Velocity' / 'theoretical'). 반면 "측정된 값에는 오차가 붙는다" 는
    규칙은 표기와 무관하게 성립하므로, 그쪽을 신뢰한다."""
    if raw.get("radius_rearth") is None:
        return MASS_ONLY
    return MEASURED if raw.get("radius_err_rearth") is not None else ESTIMATED


def is_msini(raw: dict, derived: dict) -> bool:
    """질량이 하한인가. **두 블록을 다 본다** — 표기가 한쪽에만 있는 천체가 있다.

    Proxima Cen c 는 `raw.mass_type` 이 비어 있고 `derived.mass_type` 에만 'msini' 가
    있다. 한쪽만 보면 하한이라는 사실이 조용히 사라진다."""
    for src in (raw, derived):
        if str((src or {}).get("mass_type") or "").strip().lower() == "msini":
            return True
    return False


_ROWS: list[dict] | None = None


def rows() -> list[dict]:
    """DB 에서 암석 행성을 읽는다. 등급이 붙어 나온다."""
    global _ROWS
    if _ROWS is not None:
        return _ROWS
    out = []
    for path in sorted(glob.glob(str(DB / "*.json"))):
        if not any(s in Path(path).name for s in SYSTEMS):
            continue
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
        for p in doc.get("planets") or []:
            dv, raw = p.get("derived") or {}, p.get("raw") or {}
            m_kg, r_m = dv.get("mass_kg"), dv.get("radius_m")
            if not m_kg:
                continue
            m_e = m_kg / EARTH_MASS_KG
            if m_e > ROCKY_MAX_ME:
                continue
            out.append({
                "name": p["name"],
                "mass_earth": m_e,
                "radius_earth": r_m / EARTH_RADIUS_M if r_m else None,
                "grade": grade(raw),
                "msini": is_msini(raw, dv),
            })
    order = {MEASURED: 0, ESTIMATED: 1, MASS_ONLY: 2}
    out.sort(key=lambda r: (order[r["grade"]], r["name"]))
    _ROWS = out
    return out


_CACHE: dict[str, tuple] = {}


def evaluate(row: dict):
    """한 행을 솔버에 먹인다. 등급이 **어느 질문을 물을지** 를 정한다.

    추정 반지름에는 역산을 걸지 않는다. 값이 나오긴 하지만 그 값은 남의 관계식을
    되읽은 것이라, 내놓으면 도출값처럼 보이면서 도출값이 아니다."""
    # 역산 한 번이 축을 훑고 이분법까지 돌아 비싸다. 표와 검사가 같은 행을 여러 번
    # 물으므로 결과를 붙잡아 둔다 — 같은 입력이 같은 답을 내는 순수 계산이라 안전하다.
    if row["name"] in _CACHE:
        return _CACHE[row["name"]]
    m, r = row["mass_earth"], row["radius_earth"]
    if row["grade"] == MEASURED:
        out = (infer_composition(m, r, ice_allowed=True), "역산")
    elif row["grade"] == ESTIMATED:
        out = (None, "역산 불가")
    else:
        out = (solve(m), "순방향")
    _CACHE[row["name"]] = out
    return out


def _outcome(row: dict) -> tuple[str, str]:
    """(판정, 설명) 한 쌍. 표 두 종류가 같은 문장을 쓴다."""
    res, mode = evaluate(row)
    if res is None:
        return "보류", ("반지름이 추정값이다(오차 없음, 비통과). 역산하면 그 추정을 "
                        "낸 질량-반지름 관계식의 가정을 되돌려받는다")
    if not res.applicable:
        return "거절", res.reason[:150]
    if mode == "역산":
        axis = res.regime.replace("inferred_", "")
        val = res.inputs.get(axis)
        return "풀림", (f"{axis} {val:.3f} · C/MR² {res.values['nmoi']:.4f}"
                        if isinstance(val, float) else res.regime)
    note = " (Msini — 참질량은 이 이상)" if row["msini"] else ""
    return "풀림", (f"선언 조성으로 R {res.values['radius']:.3f} R⊕ · "
                    f"C/MR² {res.values['nmoi']:.4f}{note}")


LABEL = {MEASURED: "측정 (통과 + 실질량)",
         ESTIMATED: "추정 반지름 (RV, 오차 없음)",
         MASS_ONLY: "질량만 (RV, 반지름 없음)"}


def table(markdown: bool = False) -> None:
    data = rows()
    if markdown:
        print("| planet | evidence | M (M⊕) | R (R⊕) | outcome | what it says |")
        print("|---|---|---|---|---|---|")
        for row in data:
            verdict, why = _outcome(row)
            r = f"{row['radius_earth']:.3f}" if row["radius_earth"] else "–"
            print(f"| {row['name']} | {row['grade']} | {row['mass_earth']:.3f} | "
                  f"{r} | {verdict} | {why} |")
        return
    last = None
    for row in data:
        if row["grade"] != last:
            last = row["grade"]
            print(f"\n  ── {LABEL[last]}")
        verdict, why = _outcome(row)
        r = f"{row['radius_earth']:6.3f}" if row["radius_earth"] else f"{'–':>6}"
        print(f"  [{verdict}] {row['name']:18} {row['mass_earth']:7.3f} M⊕ {r} R⊕  {why}")


if __name__ == "__main__":
    table(markdown="--md" in sys.argv)
