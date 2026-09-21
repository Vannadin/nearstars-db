# 핵 경계량을 읽는 모듈이 정확히 어느 것인가 — 층 항목의 음성 대조 (사전등록 3be84248 §3 ㉣)
"""Which modules reach for the core boundary, and which must not.

    python3 engine/test_boundary_reach.py

The layered-Mars item predicts that three nodes do not move, because they do not read the
boundary at all: `dynamo_rocky`, whose edge `interior_layers → dynamo_rocky (via core_radius)` is
drawn in `chain.yaml` but whose module never reads it, and `body_figure` and `cassini_state`,
which have no module. Nothing bound that prediction, so a boundary quantity could reach one of
them and no run would notice — and the census the item rests on would be wrong with no signal.

This is that binding, and it is the only new device the item introduces. It solves nothing: it
reads the source text, collects which boundary names each recipe module mentions, and compares
the result against the table frozen below.

A red line here means one of two things, and the message says which:
  - a module gained or lost a boundary name — the reach changed, so the census is stale;
  - `body_figure.py` or `cassini_state.py` now exists — a node that had no code has some.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent

#: The boundary quantities. `core_plus_layer_radius_km` is the declared apparent radius — the iron
#: core plus the molten silicate layer — and `core_radius_km` is what the solve produced.
BOUNDARY_NAMES = (
    "core_radius", "core_radius_earth", "core_radius_km", "core_radius_fraction",
    "core_plus_layer_radius_km", "r_cmb", "cmb_pressure", "p_cmb", "cmb_temperature", "t_cmb",
)

#: Modules that are not recipes: entry points and report writers. They print what recipes
#: produced, so their mentions say nothing about which node reaches for the boundary.
NOT_RECIPES = ("run.py", "build_graph_page.py", "dynamo_table.py", "rocky_roster.py")

#: Frozen 2026-09-21 against tree 16110413, and re-read at every landing that touches these names.
#: ⚠ `dynamo_rocky.py` is deliberately absent: `chain.yaml` draws the edge and the module never
#:   reads it (`chain.yaml@«no code consumer (ladder() has no core_radius argument; hook never
#:   fired on Earth or Pandora although interior_layers emits it, calibrated)»`). Its absence from
#:   this table IS the negative control.
REACH = {
    "cmb_flux.py": {"cmb_pressure", "cmb_temperature", "core_radius", "core_radius_earth",
                    "p_cmb", "r_cmb"},
    "core_energy.py": {"cmb_pressure", "cmb_temperature", "core_radius", "core_radius_earth",
                       "p_cmb", "r_cmb"},
    "core_entropy.py": {"cmb_pressure", "core_radius", "core_radius_earth", "p_cmb", "r_cmb"},
    "core_history.py": {"cmb_pressure", "cmb_temperature", "core_radius", "core_radius_earth",
                        "p_cmb", "r_cmb"},
    "core_state.py": {"cmb_pressure", "cmb_temperature", "p_cmb", "t_cmb"},
    # ⚠ 선언 사슬이 `core_plus_layer_radius_km` 로 갈라진 뒤 `interior.py` 는 `core_radius_km` 을
    #   더는 안 든다 — 그 이름은 이제 **풀이 출력** 쪽에만 산다 (앵커 `fixings`, `test_mars_sulphur`).
    "interior.py": {"cmb_pressure", "cmb_temperature", "core_radius", "core_radius_fraction",
                    "core_plus_layer_radius_km", "p_cmb", "t_cmb"},
    "tidal_response.py": {"core_radius", "r_cmb"},
}

#: Nodes that `chain.yaml` names with a `via` on a boundary quantity and that have no module.
#: A file appearing here is not a failure of this item — it is a signal that the census is stale.
NO_MODULE = ("body_figure.py", "cassini_state.py")


def measured() -> dict[str, set[str]]:
    """Every recipe module, and which boundary names its source text mentions."""
    pattern = re.compile(r"\b(" + "|".join(BOUNDARY_NAMES) + r")\b")
    out: dict[str, set[str]] = {}
    for path in sorted(ENGINE.glob("*.py")):
        if path.name.startswith("test_") or path.name in NOT_RECIPES:
            continue
        found = set(pattern.findall(path.read_text(encoding="utf-8")))
        if found:
            out[path.name] = found
    return out


def main() -> int:
    fails: list[str] = []
    got = measured()

    # ⚠ dynamo_rocky 는 아래 ②가 이름을 대고 잡는다 — 여기서도 잡으면 한 원인이 [FAIL] 두 줄이
    #   되고, 게이트는 [FAIL] 을 **줄 수로** 센다.
    for name in sorted((set(got) | set(REACH)) - {"dynamo_rocky.py"}):
        want = REACH.get(name)
        have = got.get(name)
        if want is None:
            fails.append(f"1: {name} reaches for the boundary and is not in the frozen table "
                         f"({sorted(have)}) — the census is stale")
            continue
        if have is None:
            fails.append(f"1: {name} is in the frozen table and now mentions no boundary name — "
                         "the reach shrank")
            continue
        if have != want:
            gained = sorted(have - want)
            lost = sorted(want - have)
            fails.append(f"1: {name} changed — gained {gained}, lost {lost}")

    # ⚠ 이 한 줄이 음성 대조의 전부다: 이름이 하나라도 들어오면 위 고리가 «표에 없다» 로 잡는다.
    if "dynamo_rocky.py" in got:
        fails.append("2: dynamo_rocky.py now reaches for the boundary "
                     f"({sorted(got['dynamo_rocky.py'])}) — prediction ㉣ says it must not")

    for name in NO_MODULE:
        if (ENGINE / name).exists():
            fails.append(f"3: {name} now exists — that node had no module when the census was "
                         "taken, so its row must be re-read")

    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails:
        print(f"  [PASS] 핵 경계 도달 — 레시피 {len(REACH)} 종만 읽는다 · "
              f"dynamo_rocky 안 읽음 · 모듈 없는 노드 {len(NO_MODULE)} 그대로")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
