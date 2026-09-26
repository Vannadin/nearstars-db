# 핵 경원소 선언 칸(core_light_elements) 시험 — 읽기 · 거절 · 핀 대응 · 화성 황 갈래 비트 (prereg-core-light-elements §3)
"""`interior.read_core_light_elements` · `pin_for` · 화성 황 갈래.

    python3 engine/test_core_light_elements.py
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior                        # noqa: E402
import run                             # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def block(value):
    return {"value": value, "grade": "declared", "source": "test", "counter_evidence_searched": "test"}


print("① 읽기와 거절")
spec, why = interior.read_core_light_elements(block({"S": "fit", "O": 0.04, "C": 0.014}))
check("화성 꼴(S fit · O 0.04 · C 0.014) 읽힘", why is None and spec == {"fit": "S", "S": None, "O": 0.04, "C": 0.014},
      str(spec))
spec, why = interior.read_core_light_elements(block({"S": 0.15, "O": 0.02, "C": 0.01}))
check("수만(S 0.15 · O 0.02 · C 0.01) 읽힘", why is None and spec["fit"] is None and spec["S"] == 0.15)
for name, value, word in (
        ("상자 밖 S", {"S": 0.25, "O": 0.02, "C": 0.01}, "상자"),
        ("상자 밖 O", {"S": 0.15, "O": 0.10, "C": 0.01}, "상자"),
        ("fit 이 S 밖(O)", {"S": 0.15, "O": "fit", "C": 0.01}, "황 전용"),
        ("fit 둘", {"S": "fit", "O": "fit", "C": 0.01}, "황 전용"),
        ("Si 비 0", {"S": 0.15, "O": 0.02, "C": 0.01, "Si": 0.05}, "Si"),
        ("H 비 0", {"S": 0.15, "O": 0.02, "C": 0.01, "H": 0.001}, "H"),
        ("어휘 밖 원소", {"S": 0.15, "O": 0.02, "C": 0.01, "N": 0.01}, "어휘 밖"),
        ("O 없음", {"S": 0.15, "C": 0.01}, "O"),
        ("값이 사전 아님", 0.15, "사전")):
    _, why = interior.read_core_light_elements(block(value))
    check(f"{name} → 이름 대고 거절", bool(why) and word in why, (why or "")[:80])

print("\n② 핀 대응 — 몸 파일의 수가 핀 리터럴과 같은 float 로 읽힘 (9f 덤)")
mars_yaml = Path(__file__).resolve().parent / "bodies" / "mars.yaml"
value = yaml.safe_load(mars_yaml.read_text(encoding="utf-8"))["inputs"]["core_light_elements"]["value"]
spec, _ = interior.read_core_light_elements(block(value))
check("화성 몸 파일 O · C == box_ceiling 핀(float ==)", interior.pin_for(spec) == "box_ceiling",
      f"O {value['O']!r} · C {value['C']!r}")
check("O · C 가 어느 핀과도 다르면 None", interior.pin_for({"O": 0.03, "C": 0.01}) is None)

print("\n③ 화성 황 갈래 — 새 칸이 옛 핀과 같은 답")
mars, _ = run.load_body(mars_yaml)
both = interior._solve_from_state(mars)
old = copy.deepcopy(mars)
old.inputs.pop("core_light_elements")
only_old = interior._solve_from_state(old)
check("새 칸 + 옛 칸 = 옛 칸만 (값 비트)", both.applicable and dict(both.values) == dict(only_old.values),
      f"core_sulphur_wt {both.values.get('core_sulphur_wt')!r}")
new = copy.deepcopy(mars)
new.inputs.pop("light_element_fixing")
only_new = interior._solve_from_state(new)
check("새 칸만 = 옛 칸만 (값 비트)", only_new.applicable and dict(only_new.values) == dict(only_old.values))
clash = copy.deepcopy(mars)
clash.inputs["light_element_fixing"] = {"value": "box_floor", "grade": "declared", "source": "test"}
r = interior._solve_from_state(clash)
check("옛 칸과 새 칸이 어긋남 → 이름 대고 거절", (not r.applicable) and "어긋난다" in (r.reason or ""), (r.reason or "")[:80])
off_pin = copy.deepcopy(mars)
off_pin.inputs.pop("light_element_fixing")
off_pin.inputs["core_light_elements"] = block({"S": "fit", "O": 0.03, "C": 0.01})
r = interior._solve_from_state(off_pin)
check("핀 밖 O · C → 이름 대고 거절(새 앵커는 이 판 밖)", (not r.applicable) and "새 황 앵커" in (r.reason or ""),
      (r.reason or "")[:80])

print("\n④ 선언 조성 몸의 수 경로 — Huang 재질을 끼운 핵, 칸이 없으면 옛 답")
earth, _ = run.load_body(Path(__file__).resolve().parent / "bodies" / "earth.yaml")
base = interior._solve_from_state(earth)
light = copy.deepcopy(earth)
light.inputs["core_light_elements"] = block({"S": 0.15, "O": 0.02, "C": 0.01})
got = interior._solve_from_state(light)
check("지구에 S 0.15 · O 0.02 · C 0.01 → 풀리거나 이름 대고 거절, 옛 답과 다름",
      (got.applicable and got.values.get("radius") != base.values.get("radius")) or (not got.applicable and bool(got.reason)),
      (f"R {base.values.get('radius'):.6f} → {got.values.get('radius'):.6f}" if got.applicable else (got.reason or "")[:80]))
check("재질이 풀이 뒤 치워짐(조성 핵 자리 그대로)", interior.COMPOSITIONS["earth_like"][3] == "fe_prem",
      interior.COMPOSITIONS["earth_like"][3])
fit_no_radius = copy.deepcopy(earth)
fit_no_radius.inputs["core_light_elements"] = block({"S": "fit", "O": 0.04, "C": 0.014})
r = interior._solve_from_state(fit_no_radius)
check("관측 핵 반지름 없는 몸의 S fit → 이름 대고 거절", (not r.applicable) and "핵 반지름" in (r.reason or ""),
      (r.reason or "")[:80])

print(f"  test_core_light_elements — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
