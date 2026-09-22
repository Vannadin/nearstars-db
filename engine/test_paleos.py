# PALEOS 표를 우리 상자 밖의 **둘째 의견**으로만 읽는다는 것을 세는 시험 (ㄱ, 사전등록 a610ae6d)
"""PALEOS as a named second extrapolation — counted, never shipped.

    python3 engine/test_paleos.py

⚠ **This test is the only consumer of `paleos.py`.** The owner's ruling ⑨ is *«PALEOS stays a
validation line»*, so the module is not wired into any solve path: the second opinion is printed
here, next to ours, and never travels into a shipped cell. Acceptance ① is therefore structural —
there is no consumer to move a digit — and this file proves that by grep rather than by assertion.

⚠ **This file IS in the gate** — `scripts/check.sh` runs it as `step "test_paleos"`. The sentence
that stood here said the opposite, and ⚠ **it was true when it was written**: the docstring landed
in `26e44e36` (2026-09-14 23:18:50) and the gate step in `5a7687dd` (2026-09-15 01:57:43), **two
hours and thirty-nine minutes later**. Nobody went back. **A sentence about wiring does not have to
be wrong to become wrong — it only has to stop being told.** That is worse than a lie, because
nothing looks suspicious at the moment it rots. Corrected 2026-09-22, and the claim it replaced is
named here rather than deleted, because the next reader is owed the reason the line moved.

The six acceptance lines of §7, each counted in this run:

| # | counted how |
|---|---|
| ① | no engine file imports `paleos`; a set of engine values is bit-identical before and after the import |
| ② | the fire count per probe family — roster expected **0**, anchors fire |
| ③ | every answer carries its grade; a value without a grade is a failure, not a cell |
| ④ | the iron phase column is never read — `lookup("Fe", …)["phase"] is None` on every iron probe |
| ⑤ | an omitted MgSiO₃ node is chosen deliberately and prints «PALEOS 없음», with its grid coordinates |
| ⑥ | lookups, seeks and wall time, printed by `paleos.cost_line()` |
"""
from __future__ import annotations

import math
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import eos                                                            # noqa: E402
import ice_fr2015                                                     # noqa: E402

GPA = 1e9
ENGINE = pathlib.Path(__file__).resolve().parent

# ⚠ 대조는 **import 전에** 뜬다 — paleos 가 무엇을 건드렸는지 보려면 그 전의 수가 있어야 한다.
_CONTROL_PROBES = (("fe_eps", 200.0 * GPA, 2000.0),
                   ("silicate", 100.0 * GPA, 1500.0),
                   ("h2o", 100.0 * GPA, 500.0))
_BEFORE = {name: eos.MATERIALS[name].density(p, t, 0.0) for name, p, t in _CONTROL_PROBES}

import paleos                                                         # noqa: E402

# ⚠ **표 셋은 레포 밖에 산다** — `docs/phase3/_papers/` 의 추적되지 않는 파일이고, 그 기계에
#   없으면 이 시험은 물어볼 대상이 없다. **그때는 실패가 아니라 이름 붙인 SKIP 이다** (C96, ⓒ).
#   ⚠ **분모를 함께 찍는다** — 「0 of 3」과 「3 of 3 인데 못 읽음」은 다른 사건이고, 분모가 없으면
#   둘이 같은 줄로 인쇄된다. 판단은 이 파일이 한다: 게이트가 따로 세면 같은 규칙이 두 자리에
#   앉고, 시험을 혼자 돌릴 때는 아무도 안 세게 된다.
# ⚠ **어느 파일을 읽는지 판마다 한 번 인쇄한다.** 사유 줄은 「어느 격자 칸인가」를 답하는
#   자리라 조회마다 상수를 되풀이할 데가 아니고, 「어느 파일인가」는 **판당 한 번**이면 된다.
#   그 한 줄이 게이트 로그에 남아 **사람이 볼 대조표**가 된다 — 판본은 우리 선언이므로
#   **파일명과 갈라졌는지 볼 수 있는 자리가 로그에만 있다.**
print("  [기록] PALEOS 표 — "
      + " · ".join(f"{name} v{t.version} `{t.file}`" for name, t in sorted(paleos.TABLES.items())))
_found = [t.file for t in paleos.TABLES.values() if (paleos.PAPERS / t.file).is_file()]
if len(_found) < len(paleos.TABLES):
    print(f"  [SKIP] SKIP — PALEOS tables: {len(_found)} of {len(paleos.TABLES)} found "
          f"({paleos.PAPERS}/*.dat) — 물어볼 표가 없다, 실패가 아니다")
    raise SystemExit(0)

fails: list[str] = []


def ok(cond: bool, msg: str) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    if not cond:
        fails.append(msg)


# ── ① 배달되는 수는 하나도 안 움직인다 ──────────────────────────────────────
print("① 배달 셀 무변경 — 소비처가 없다는 것을 grep 으로, 값은 비트로")

_users = subprocess.run(
    ["grep", "-rln", "-e", "import paleos", "-e", "from paleos", "--include=*.py", "."],
    cwd=ENGINE, capture_output=True, text=True).stdout.split()
_users = [u for u in _users if pathlib.Path(u).name != "test_paleos.py"]
ok(not _users,
   "엔진 파일 중 `paleos` 를 읽는 곳 0 개 — 이 시험 말고는 소비처가 없다"
   + (f" (발견: {' · '.join(_users)})" if _users else ""))

_after = {name: eos.MATERIALS[name].density(p, t, 0.0) for name, p, t in _CONTROL_PROBES}
_moved = [k for k in _BEFORE if _BEFORE[k].hex() != _after[k].hex()]
ok(not _moved,
   "import 전후로 우리 값 셋이 비트까지 같다 — "
   + " · ".join(f"{k} {_BEFORE[k]:.6f}" for k in _BEFORE)
   + (f" ⚠ 움직인 것: {_moved}" if _moved else ""))

# ── 같은 실행 대조 — 이미 아는 수를 이 실행이 다시 낸다 ─────────────────────
print("\n같은 실행 대조 — C82-2 의 띠 양끝은 이 실행에서도 같은 수인가")
_e295 = ice_fr2015.pressure(ice_fr2015.FIT_RHO_MAX, 295.0)
_e2000 = ice_fr2015.pressure(ice_fr2015.FIT_RHO_MAX, 2000.0)
ok(abs(_e295 - 342.1843) < 5e-4 and abs(_e2000 - 353.8167) < 5e-4,
   f"P(FIT_RHO_MAX, T) = {_e295:.4f} GPa @295 K · {_e2000:.4f} GPa @2000 K "
   "(기대 342.1843 · 353.8167) — 대조가 틀리면 아래 수는 전부 버린다")

# ── ⑥/§6 A 그들의 상자도 이름으로 ───────────────────────────────────────────
print("\n§6 A·Amendment 1 — 두 상자를 **이름과 머리말**로, 타이핑한 수 없이")
print(f"  우리 상자 — Fe 위끝 `DOROGOKUPETS_FIT_P_MAX` {eos.DOROGOKUPETS_FIT_P_MAX / GPA:.4g} GPa · "
      f"H₂O 위끝 `P(FIT_RHO_MAX, T)` {_e295:.4f} GPa @295 K")
for _t in ("Fe", "MgSiO3", "H2O"):
    f = paleos.facts(_t)
    npd_p, npd_t = f.nodes_per_decade()
    print(f"  그들의 상자 — {_t}: P {f.p_lo:.6g}–{f.p_hi:.6g} Pa · T {f.t_lo:.6g}–{f.t_hi:.6g} K · "
          f"격자 {f.n_p} × {f.n_t} · 십진당 P {npd_p:.4f} · T {npd_t:.4f} · 머리말 {f.comment_lines} 줄")
    # ⚠ 이분법이 기대는 두 사실을 **이 실행이 확인한 것**으로 인쇄한다 (감사석) — 정렬과 열 자리.
    print(f"    정렬 확인 {f.sorted_note} · `{paleos.PHASE_COLUMN}` 은 머리말이 인쇄한 "
          f"{f.phase_field() + 1} 번째 열 (열 {len(f.columns)} 개)")

_t_axes = {t: paleos.facts(t).nodes_per_decade()[1] for t in ("Fe", "MgSiO3", "H2O")}
ok(abs(_t_axes["Fe"] - 150.2252) < 5e-4 and abs(_t_axes["H2O"] - 150.0) < 5e-4,
   f"축 스텝은 축마다 다르고 **끝점에서 나온다** — Fe·MgSiO₃ 의 T 축 {_t_axes['Fe']:.4f} 대 "
   f"H₂O 의 T 축 {_t_axes['H2O']:.4f}. 한쪽 수를 다른 축에 옮기면 0.876 % 밀린다")

# ── ②/③/④ 발화 수를 **세어서** 인쇄 ────────────────────────────────────────
print("\n② 발화 수 — 두 식구를 따로 센다 (읽은 수이지 가정이 아니다)")

# 로스터 쪽 — 우리 상자 **안** 을 묻는다. 여기서 PALEOS 가 발화하면 그게 발견이다.
ROSTER_PROBES = (("Fe", 150.0 * GPA, 3000.0), ("Fe", 300.0 * GPA, 4000.0),
                 ("MgSiO3", 50.0 * GPA, 2000.0), ("MgSiO3", 200.0 * GPA, 3000.0),
                 ("H2O", 10.0 * GPA, 500.0), ("H2O", 100.0 * GPA, 1000.0))
# 앵커 쪽 — 우리 상자 **밖**. 얼음의 위끝은 그 T 에서의 함수다 (C82-2).
# ⚠ 규산염의 위끝은 **13 500 GPa** 다 — 첫 판에서 5 000 GPa 를 「상자 밖」이라 적었다가
#   실행이 「상자 안」이라고 답했다. 사다리의 끝을 **이름으로** 읽어 그 위를 묻는다.
_SILICATE_TOP = max(ph.p_max for ph in eos.MATERIALS["silicate"].phases)
ANCHOR_PROBES = (("Fe", 500.0 * GPA, 5000.0), ("Fe", 900.0 * GPA, 6000.0),
                 ("MgSiO3", _SILICATE_TOP * 2.0, 4000.0),
                 ("H2O", (_e2000 + 50.0) * GPA, 2000.0))


def _in_our_box(table: str, p: float, t: float) -> bool:
    """우리 적합이 근거를 가진 구간인가 — **상수와 함수 이름으로**, 타이핑한 수 없이."""
    if table == "Fe":
        return p <= eos.DOROGOKUPETS_FIT_P_MAX
    if table == "H2O":
        return (eos.FR2015_FIT_P_MIN <= p
                <= ice_fr2015.pressure(ice_fr2015.FIT_RHO_MAX, t) * GPA)
    phases = eos.MATERIALS["silicate"].phases
    return any(ph.p_min <= p < ph.p_max for ph in phases)


for label, probes, expect_fire in (("로스터(상자 안)", ROSTER_PROBES, 0),
                                   ("앵커(상자 밖)", ANCHOR_PROBES, len(ANCHOR_PROBES))):
    fired = 0
    for table, p, t in probes:
        inside = _in_our_box(table, p, t)
        if inside:
            continue                    # 우리 값이 근거를 가진다 — 둘째 의견을 안 묻는다
        fired += 1
        r = paleos.lookup(table, p, t)
        print(f"    {table} {p / GPA:.6g} GPa · {t:.0f} K → [{r['grade']}] "
              + (f"ρ {r['density']:.2f} kg/m³" if r["density"] is not None else "값 없음")
              + (f" · 상 {r['phase']}" if r["phase"] else "")
              + f" — {r['why']}")
    ok(fired == expect_fire,
       f"{label}: 발화 {fired} 회 (기대 {expect_fire}) · 물음 {len(probes)} 개")

print("\n③ 등급은 수와 함께 다닌다 — 등급 없는 답이 하나라도 있으면 실패")
_answers = [paleos.lookup(t, p, tt) for t, p, tt in ANCHOR_PROBES]
ok(all(a["grade"] in (paleos.GRADE_HIT, paleos.GRADE_ABSENT, paleos.GRADE_OUT) for a in _answers),
   f"답 {len(_answers)} 개가 전부 세 등급 중 하나를 달고 나왔다 — "
   + " · ".join(sorted({a["grade"] for a in _answers})))

print("\n④ 철의 상 열은 읽지 않는다")
_iron = [paleos.lookup("Fe", p, t) for tbl, p, t in ANCHOR_PROBES if tbl == "Fe"]
ok(all(a["phase"] is None for a in _iron),
   f"철 물음 {len(_iron)} 개 전부 `phase is None` — 그 열은 `liquid` 와 `unknown` 뿐이라 "
   "읽을 이름이 없다")

# ── ⑤ 빠진 노드를 **일부러 골라** 발화시킨다 ────────────────────────────────
print("\n⑤ 「PALEOS 없음」 경로 — 빠진 MgSiO₃ 노드를 골라 발화시킨다")
_absent = None
_f = paleos.facts("MgSiO3")
for _i in (0, 5, 20, 60, 120, 300, 600, 900, 1200, 1340):
    for _j in (0, 10, 50, 120, 200, 300, 370, 379):
        _p = 10.0 ** (math.log10(_f.p_lo) + _i * _f.dlog_p)
        _t = 10.0 ** (math.log10(_f.t_lo) + _j * _f.dlog_t)
        _r = paleos.lookup("MgSiO3", _p, _t)
        if _r["grade"] == paleos.GRADE_ABSENT:
            _absent = (_i, _j, _p, _t, _r)
            break
    if _absent:
        break
ok(_absent is not None,
   "빠진 노드를 찾았다" if _absent is None else
   f"빠진 노드 (i_p {_absent[0]} · j_t {_absent[1]}) = {_absent[2]:.6g} Pa · {_absent[3]:.6g} K "
   f"→ [{_absent[4]['grade']}] {_absent[4]['why']}")

# ── ⑥ 비용은 수다 ───────────────────────────────────────────────────────────
print("\n⑥ 비용 — 이 값을 만든 커밋이 그 값을 센다")
print(f"  {paleos.cost_line()}")
ok(paleos.PALEOS_COST["lookups"] > 0 and paleos.PALEOS_COST["seconds"] > 0.0,
   f"조회 {paleos.PALEOS_COST['lookups']} 회 · seek {paleos.PALEOS_COST['seeks']} 회 · "
   f"{paleos.PALEOS_COST['seconds']:.3f} s — 조회당 seek "
   f"{paleos.PALEOS_COST['seeks'] / max(paleos.PALEOS_COST['lookups'], 1):.1f} 회")

print("\n모두 통과" if not fails else f"\n실패 {len(fails)}건")
for f_ in fails:
    print(f"  · {f_}")
raise SystemExit(1 if fails else 0)
