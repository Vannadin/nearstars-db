# 맨틀 조성 선언(C74-2) 시험 — 읽기 · 거절 · 원문 표 수 · 선언 없는 몸 비트 동일 · A′-배관 · 칸 가운데 보간 보고
"""prereg-c74-2-mantle-composition §3 (frozen `2571123c`).

    engine/.venv-gate/bin/python3 engine/test_mantle_composition.py      # ④ 는 BurnMan 이 필요하다

① 읽기와 거절 — 어휘 밖 산화물 · 음수 · 합 100 ± 2 밖 · CFMASNa 빠짐.
② 원문 표 수 — W&H 2005 Table 3 Bulk DMM · Khan+ 2022 Table 1 이 이 시험의 상수와 글자 같음(원문 대조 기록).
③ 선언 없는 몸 비트 동일(A′ ⓐ) · 풀이 뒤 재질이 제자리 · 온도 없는 몸 · 표 없는 조성은 이름 대고 거절.
④ A′-배관 — 표 격자점에서 엔진 밀도 · αK 대 BurnMan 직접 선택기, 상대 ≤ 1e-6(결정 칸 ⑥). 칸 가운데 보간 차는
   보고만(판정 없음), 전이 든 칸과 아닌 칸을 갈라(덧붙임 4).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mantle_composition as mc       # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def block(value):
    return {"value": value, "grade": "literature", "source": "test", "counter_evidence_searched": "test"}


#: W&H 2005 Table 3 «Bulk DMM»(캐시 `2005E_PSL.231...53W.txt` 1661–) — 합 100.00, Na₂O 는 괄호 밖 값.
DMM_WH2005 = {"SiO2": 44.71, "Al2O3": 3.98, "FeO": 8.18, "MnO": 0.13, "MgO": 38.73, "CaO": 3.17, "Na2O": 0.13,
              "Cr2O3": 0.57, "TiO2": 0.13, "NiO": 0.24, "K2O": 0.006, "P2O5": 0.019}
#: Khan+ 2022 Table 1 «Best-fit average … CFMASNa (normalised to 100%)»(캐시 `2022E_PSL.57817330K.txt` 595–).
MARS_KHAN2022 = {"SiO2": 46.66, "Al2O3": 3.49, "MgO": 32.81, "CaO": 2.66, "FeO": 13.68, "Na2O": 0.69}

print("① 읽기와 거절")
wt, why = mc.read_mantle_composition(block(DMM_WH2005))
check("W&H 2005 Bulk DMM 읽힘", why is None and wt["FeO"] == 8.18, why or "")
wt, why = mc.read_mantle_composition(block(MARS_KHAN2022))
check("Khan+ 2022 Table 1 읽힘", why is None and wt["FeO"] == 13.68, why or "")
for name, value, word in (
        ("어휘 밖", dict(MARS_KHAN2022, H2O=0.1), "어휘 밖"),
        ("음수", dict(MARS_KHAN2022, FeO=-1.0), "0 이상"),
        ("합 밖", dict(MARS_KHAN2022, SiO2=60.0), "합"),
        ("CFMASNa 빠짐", {k: v for k, v in MARS_KHAN2022.items() if k != "Na2O"}, "CFMASNa")):
    _, why = mc.read_mantle_composition(block(value))
    check(f"{name} → 이름 대고 거절", bool(why) and word in why, (why or "")[:80])

print("\n② 원문 표 수 — 합")
check("W&H Bulk DMM 합 = 100.00(원문 인쇄 합, ± 0.01)", abs(sum(DMM_WH2005.values()) - 100.0) <= 0.01,
      f"{sum(DMM_WH2005.values()):.3f}")
check("Khan Table 1 합 = 100(정규화, ± 0.01)", abs(sum(MARS_KHAN2022.values()) - 100.0) <= 0.01,
      f"{sum(MARS_KHAN2022.values()):.3f}")

print("\n③ 선언 없는 몸 · 재질 제자리 · 거절")
import copy                            # noqa: E402
import eos                             # noqa: E402
import interior                        # noqa: E402
import registry                        # noqa: E402
import run                             # noqa: E402
registry.load_all()
HERE = Path(__file__).resolve().parent
# ⚠ 몸 파일은 이 칸을 아직 안 켠다(지휘 ⓒ, 덧붙임 9) — 선언은 이 시험이 W&H DMM 을 끼워 만든다.
plain, _ = run.load_body(HERE / "bodies" / "earth.yaml")
check("몸 파일 지구는 선언이 없다(지휘 ⓒ)", plain.inputs.get("mantle_composition") is None)
earth = copy.deepcopy(plain)
earth.inputs["mantle_composition"] = block(DMM_WH2005)
a = interior._solve_from_state(copy.deepcopy(plain))
b = interior._solve_from_state_body(copy.deepcopy(plain))
check("선언 없는 지구 — 입구 대 몸통 값 비트 동일", a.values == b.values and a.notes == b.notes)
saved = (eos.MATERIALS["silicate"], eos.MATERIALS["silicate_chondritic"])
got = interior._solve_from_state(copy.deepcopy(earth))
check("선언 있는 지구가 풀림", got.applicable, getattr(got, "reason", "") or "")
check("풀이 뒤 규산염 두 재질이 제자리(같은 객체)",
      (eos.MATERIALS["silicate"], eos.MATERIALS["silicate_chondritic"]) == saved
      and eos.MATERIALS["silicate"] is saved[0])
check("선언이 inputs · notes 에 남음", got.inputs.get("mantle_composition") == DMM_WH2005
      and any("광물 집합" in n for n in got.notes))
cold = copy.deepcopy(earth)
cold.inputs.pop("potential_temperature", None)
r = interior._solve_from_state(cold)
check("온도 없는 몸 → 이름 대고 거절", not r.applicable and "potential_temperature" in (r.reason or ""), (r.reason or "")[:80])
odd = copy.deepcopy(earth)
odd.inputs["mantle_composition"] = block(dict(DMM_WH2005, FeO=9.18, MgO=37.73))
r = interior._solve_from_state(odd)
check("표 없는 조성 → 이름 대고 거절", not r.applicable and "표" in (r.reason or ""), (r.reason or "")[:80])

print("\n④ A′-배관 — 표 격자점 · 칸 가운데(BurnMan)")
try:
    import burnman                     # noqa: F401
except ImportError:
    burnman = None
    check("BurnMan 이 있다(게이트 venv)", False, "engine/.venv-gate/bin/python3 로 돌린다")
if burnman is not None:
    for body, wt in (("earth", DMM_WH2005), ("mars", MARS_KHAN2022)):
        tab, why = mc.load(wt)
        check(f"{body} 표 읽힘", why is None, why or "")
        if why:
            continue
        mat = mc.table_material(eos.MATERIALS["silicate"], tab.key)
        bulk = mc.atomic_bulk(wt)
        ps = [math.exp(x) for x in tab.lnp]
        window = [i for i, pp in enumerate(ps) if pp <= eos.SILICATE_EN_TO_PREM]
        nodes = [(i, j) for j in range(0, len(tab.t), 7) for i in window[::23]]
        worst, used, skipped = 0.0, 0, 0
        for i, j in nodes:
            name = tab.assemblage[j][i]
            if name is None or name.endswith("*frozen") or mat.phase_at(ps[i])._w(ps[i], tab.t[j]) < 1.0:
                skipped += 1
                continue
            direct, _, _ = mc.select(bulk, ps[i], tab.t[j])
            if direct is None or direct["assemblage"] != name:
                skipped += 1
                continue
            rho = mat.density(ps[i], tab.t[j])
            ak = mat.phase_at(ps[i]).dpdt_v(tab.t[j], 0.0, ps[i])
            worst = max(worst, abs(rho / direct["rho"] - 1.0), abs(ak / direct["alpha_k"] - 1.0))
            used += 1
        check(f"{body} A′-배관 — 격자점 {used} 개에서 ρ · αK 상대 ≤ 1e-6", used > 0 and worst <= 1e-6,
              f"최대 {worst:.3e} · 건너뜀 {skipped}(빈 칸 · 굳힌 칸 · 섞임 띠 · 직접 선택기가 다른 집합)")
        rows = {"전이": [], "전이 없음": []}
        for i in window[:-1][::17]:
            for j in range(0, len(tab.t) - 1, 9):
                q = [tab.assemblage[jj][ii] for jj in (j, j + 1) for ii in (i, i + 1)]
                if None in q or any(n.endswith("*frozen") for n in q):
                    continue
                pm, tm = math.sqrt(ps[i] * ps[i + 1]), 0.5 * (tab.t[j] + tab.t[j + 1])
                if mat.phase_at(pm)._w(pm, tm) < 1.0:
                    continue
                direct, _, _ = mc.select(bulk, pm, tm)
                if direct is None:
                    continue
                rows["전이" if len(set(q)) > 1 else "전이 없음"].append(
                    (abs(mat.density(pm, tm) / direct["rho"] - 1.0), pm, tm))
        band = []
        for i in window[::8]:
            e = tab.edge_at(ps[i])
            if not math.isfinite(e):
                continue
            ph = mat.phase_at(ps[i])
            tt = e - 0.5 * mc.T_STEP - mc.BLEND_K       # 띠 안쪽 끝(w = 1)의 표 값 대 옛 상
            if tt < mc.T_LO:
                continue
            try:
                band.append((abs(tab.at(ps[i], tt)[0] / ph.old.density(ps[i], tt, 0.0) - 1.0), ps[i], tt))
            except Exception:
                continue
        if band:
            m = max(band)
            print(f"  [보고] {body} 섞임 띠 밀도 차(표 대 옛 상, 띠 안쪽 끝) — {len(band)} 열 · 최대 {m[0]:.3e} "
                  f"({m[1] / 1e9:.3f} GPa, {m[2]:.0f} K) · 중앙 {sorted(x[0] for x in band)[len(band) // 2]:.3e}")
        for k, v in rows.items():
            if v:
                m = max(v)
                print(f"  [보고] {body} 칸 가운데 ρ 보간 차 — {k} {len(v)} 칸 · 최대 {m[0]:.3e} "
                      f"({m[1] / 1e9:.3f} GPa, {m[2]:.0f} K) · 중앙 {sorted(x[0] for x in v)[len(v) // 2]:.3e}")
            else:
                print(f"  [보고] {body} 칸 가운데 — {k} 칸 0")

print(f"  test_mantle_composition — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
