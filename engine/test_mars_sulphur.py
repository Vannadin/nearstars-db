# 화성 핵의 황 맞춤을 게이트에서 한 번만 풀고, 그 답을 지문과 함께 굳힌다.
"""화성 핵 황 맞춤 — 굳힌 답과 지금 코드가 같은 답을 내는가.

    python3 engine/test_mars_sulphur.py              대조 (게이트 단계)
    python3 engine/test_mars_sulphur.py --refresh    다시 굳힘 → mars_sulphur_anchor.json

⚠ **왜 굳히는가.** 맞춤 한 번은 사원계 역산 **아홉 번**(괄호 둘 + 반분 여섯 + 보고점 하나, ≈612 s)이다.
화성 노드를 푸는 자리마다 그것을 물리면 한 게이트가 역산을 열세 번 더 푼다 — 측정
(2026-09-20): 픽스처만으로 `test_interior.py` 가 633 s 에서 1447 s 로, **+814 s**.
그래서 맞춤은 **이 단계 하나**에서만 돌고, 노드와 픽스처는 굳힌 값을 읽는다.
얼음거대행성 앵커(`ice_giant_anchor.json`, C88)와 같은 꼴이다.

⚠ **이 파일은 그 얼음거대행성 앵커의 감시 입력이기도 하다** — `interior.py` 가 이름을 대므로
`trigger_files()` 의 그물에 걸린다. 그래서 **다시 굳히는 순서는 황 먼저, 얼음거대행성 나중**
이고, 굳힌 값에 **초를 담지 않는다**(`_record` 의 주석).

⚠ **고정 둘을 다 굳힌다.** 픽스처가 묻는 것은 «두 고정이 다른 답을 주느냐» 이고, 한쪽만
굳히면 다른 쪽은 손으로 적은 수가 된다 — 그러면 자가 아니라 손을 시험한다. 선언된 고정은
착지 정밀도로(반분 6 회), 다른 고정은 «갈리느냐» 만 보므로 성기게(반분 2 회) 굳힌다.
"""
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path

import yaml

import interior
# 코드 자는 한 번만 정의한다 — 바이트 자와 다른 질문(«파일이 **하는 일**이 바뀌었나»)이고,
# 두 벌로 지으면 두 앵커가 서로 다른 자를 쓰게 된다.
from test_ice_giant import _feed_code

ANCHOR_FILE = interior.SULPHUR_ANCHOR_FILE
MARS_FILE = Path(__file__).resolve().parent / "bodies" / "mars.yaml"

#: 물리 쪽 방아쇠. `mars.yaml` 은 여기 없다 — 그 파일은 **값**으로 잰다(`declared`).
TRIGGER_FILES = ("interior.py", "eos.py", "chain.yaml")

#: 선언된 고정은 착지 정밀도, 다른 고정은 «갈리느냐» 만.
#: ⚠ 한 맞춤의 역산은 **반분 회수 + 3** 이다 — 괄호 둘, 반분마다 하나, 그리고 보고하는
#: `w_s` 에서 한 번 더(고리 안의 마지막 시행은 `w_s` 가 아닌 중점에서 풀렸다).
HALVINGS_DECLARED = interior.SULPHUR_FIT_HALVINGS
HALVINGS_OTHER = 2

#: 두 고정의 황이 이만큼은 갈려야 `light_element_fixing` 이 무엇인가를 하고 있는 것이다.
APART_MIN_WT = 0.01

#: 굳힌 황과 다시 푼 황의 허용 차. 반분 6 회의 해상도는 (0.25 − 0.13) / 2⁶ = 0.1875 wt% 이므로
#: 그보다 잘게 요구하면 이분법 자신의 눈금을 재게 된다.
SULPHUR_TOL_WT = 0.002


def declared_inputs() -> dict:
    """`mars.yaml` 이 선언한 다섯 — 굳힌 답을 움직이는 것 전부."""
    doc = yaml.safe_load(MARS_FILE.read_text(encoding="utf-8"))["inputs"]

    def value(x):
        return x.get("value") if isinstance(x, dict) else x

    out = {k: value(doc.get(k)) for k in interior.SULPHUR_ANCHOR_DECLARATIONS}
    out["core_radius_km"] = float(out["core_radius_km"])
    return out


def file_digests() -> dict:
    """방아쇠 파일마다 바이트 자와 (파이썬이면) 코드 자."""
    here = Path(__file__).resolve().parent
    out = {}
    for name in TRIGGER_FILES:
        f = here / name
        rec = {"bytes": hashlib.sha256(f.read_bytes()).hexdigest()[:16]}
        if f.suffix == ".py":
            h = hashlib.sha256()
            _feed_code(h, compile(f.read_bytes(), f.name, "exec"))
            rec["code"] = h.hexdigest()[:16]
        out[name] = rec
    return out


def _fit(declared: dict, pin: str, halvings: int) -> tuple:
    t0 = time.perf_counter()
    w_s, res = interior.fit_sulphur_to_core_radius(
        declared["mass_earth"], declared["radius_earth"], declared["core_radius_km"], pin,
        potential_temperature=declared["potential_temperature"], halvings=halvings)
    return w_s, res, time.perf_counter() - t0


def _record(w_s: float, res, halvings: int, declared: dict) -> dict:
    """굳히는 값. ⚠ **초는 여기 안 들어간다.**

    이 파일은 `interior.py` 가 이름을 대는 데이터 파일이라 `engine/test_ice_giant.py@«def trigger_files»`
    의 그물(소스에서 `.json` 리터럴을 긁는다)에 걸리고, 그쪽 `input_digests()` 가 **이 파일 전체
    바이트를 해시**한다. 초를 담으면 물리가 하나도 안 바뀐 재굳힘도 바이트를 움직여 얼음거대행성
    앵커가 빨개진다 — **초는 기록만 하고 판정하지 않는다**는 규칙이 해시 안에서 뒤집힌다
    (감사석, 2026-09-20). 걸린 시간은 인쇄로 남는다."""
    v = res.values
    r_m = v["core_radius"] * interior.EARTH_RADIUS_M
    m_core = declared["mass_earth"] * interior.EARTH_MASS_KG * v["core_mass_fraction"]
    return {"halvings": halvings,
            "core_sulphur_wt": w_s,
            "core_radius_km": r_m / 1e3,
            "core_radius_fraction": v["core_radius_fraction"],
            "core_mass_fraction": v["core_mass_fraction"],
            # ⚠ **맞춘 조성이 부딪는 두 번째 발표값** — Durán+ 2022 는 반지름 구간과 평균 핵밀도
            #   6–6.2 g/cm³ 를 **같은 문장**에서 낸다. 반지름은 맞춤이 소비했으므로 이 밀도가
            #   그 논문 쪽에 남은 대조다. 우리 값은 질량분율과 소비된 반지름의 함수라 «독립 측정»
            #   이 아니고, **발표값과 우리 답이 만나는 자리**다.
            "core_mean_density_gcc": m_core / (4.0 / 3.0 * math.pi * r_m ** 3) / 1e3,
            "nmoi": v["nmoi"]}


def refresh() -> int:
    declared = declared_inputs()
    pin_declared = declared["light_element_fixing"]
    out = {"python": platform.python_version(), "frozen_at": time.strftime("%Y-%m-%d"),
           "bracket": list(interior.SULPHUR_FIT_BRACKET), "declared": declared,
           "files": file_digests(), "fixings": {}}
    for pin in sorted(interior.LIGHT_ELEMENT_PINS):
        n = HALVINGS_DECLARED if pin == pin_declared else HALVINGS_OTHER
        print(f"{pin} — 맞춤 (역산 {n + 3} 회) …", flush=True)
        w_s, res, seconds = _fit(declared, pin, n)
        if w_s is None:
            print(f"  거절 — {(res.reason or '')[:90]}")
            return 1
        rec = _record(w_s, res, n, declared)
        print(f"  {seconds:.0f} s · S {w_s * 100:.4f} wt% · 핵 {rec['core_radius_km']:.2f} km "
              f"· C/MR² {rec['nmoi']:.6f}")
        # ⚠ **밀도는 낸 쌍과 함께 인쇄한다** — 수 하나만 두면 다음 사람이 검산을 못 하고, 실제로
        #   다른 표의 `cmf` 와 짝지어져 6.09 대 6.88 로 갈린 적이 있다(감사석, 2026-09-20).
        print(f"       평균 핵밀도 {rec['core_mean_density_gcc']:.3f} g/cm³ "
              f"= cmf {rec['core_mass_fraction']:.7f} × M 화성 / (4/3 π r³, r = "
              f"{rec['core_radius_km']:.2f} km)")
        out["fixings"][pin] = rec
    ANCHOR_FILE.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"굳혔다 → {ANCHOR_FILE.name}")
    # ⚠ **순서가 있다 — 황 먼저, 얼음거대행성 나중.** 이 파일이 얼음거대행성 앵커의 감시 입력이라
    #   거꾸로 굳히면 얼음 쪽이 낡은 바이트를 들고 남는다.
    print("다음: `python3 engine/test_ice_giant.py --refresh` — 이 파일은 얼음거대행성 앵커의 "
          "감시 입력이다 (황 먼저, 얼음 나중)")
    return 0


def _check_declared(frozen: dict, declared: dict, fails: list) -> None:
    for key in interior.SULPHUR_ANCHOR_DECLARATIONS:
        want, got = frozen["declared"].get(key), declared.get(key)
        same = want == got
        print(f"  [{'PASS' if same else 'FAIL'}] 선언 `{key}` {got!r}")
        if not same:
            fails.append(f"선언 `{key}` 가 굳힘과 다르다 (굳힘 {want!r} · 지금 {got!r}) — "
                         "같은 선언이 맞으면 **이 커밋에서 `--refresh`**")


def _check_files(frozen: dict, fails: list) -> None:
    """⚠ **어느 자가 움직였는지 먼저 말하고, 그 다음에 `--refresh` 를 말한다.**

    바이트만 움직이면 주석·빈 줄이고, 코드까지 움직이면 그 파일이 **하는 일**이 바뀐 것이다 —
    읽는 사람이 둘을 구분해야 `--refresh` 가 생각 없이 누르는 단추가 되지 않는다."""
    now = file_digests()
    for name in TRIGGER_FILES:
        then, here = frozen["files"].get(name, {}), now[name]
        moved = [ruler for ruler in ("bytes", "code")
                 if ruler in here and then.get(ruler) != here[ruler]]
        print(f"  [{'PASS' if not moved else 'FAIL'}] `{name}` "
              + ("자 그대로" if not moved else f"{'·'.join(moved)} 가 움직였다"))
        if moved:
            what = ("주석·빈 줄만 움직였다 (코드 자는 그대로)" if moved == ["bytes"]
                    else "이 파일이 **하는 일**이 바뀌었다")
            fails.append(f"`{name}`: {'·'.join(moved)} 자가 굳힘과 다르다 — {what}. "
                         f"굳힘 {then.get(moved[0])} · 지금 {here[moved[0]]}. "
                         "의도한 변화면 **이 커밋에서 `--refresh`** 로 다시 굳혀 diff 에 남겨라")


def check() -> int:
    if not ANCHOR_FILE.exists():
        print(f"[FAIL] {ANCHOR_FILE.name} 이 없다 — `--refresh` 로 굳혀라")
        return 1
    frozen = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
    declared = declared_inputs()
    fails: list = []

    print("굳힌 맞춤 — 선언과 방아쇠 파일")
    _check_declared(frozen, declared, fails)
    _check_files(frozen, fails)

    print("\n굳힌 맞춤 — 같은 코드가 같은 황을 내는가")
    for pin in sorted(frozen["fixings"]):
        rec = frozen["fixings"][pin]
        w_s, res, seconds = _fit(declared, pin, rec["halvings"])
        if w_s is None:
            fails.append(f"{pin}: 다시 풀었더니 값이 안 나왔다 — {(res.reason or '')[:70]}")
            print(f"  [FAIL] {pin:12} 거절 — {(res.reason or '')[:70]}")
            continue
        gap = abs(w_s - rec["core_sulphur_wt"]) * 100
        ok = gap <= SULPHUR_TOL_WT
        if not ok:
            fails.append(f"{pin}: 굳힌 S {rec['core_sulphur_wt'] * 100:.4f} wt% 와 지금 "
                         f"{w_s * 100:.4f} wt% 가 {gap:.4f} wt% 갈린다 (허용 "
                         f"{SULPHUR_TOL_WT:.3f}) — 의도한 변화면 **이 커밋에서 `--refresh`**")
        print(f"  [{'PASS' if ok else 'FAIL'}] {pin:12} S {w_s * 100:7.4f} wt% "
              f"(굳힘 {rec['core_sulphur_wt'] * 100:7.4f} · 차 {gap:.4f}) · {seconds:.0f} s")

    # ⚠ **축이 목표를 감싸지 못하면 값이 아니라 없음이 나와야 한다** — 상자를 넓히는 것은 이
    #   레시피의 일이 아니다. 괄호 둘만 풀고 끝나므로 역산 **두 번**이다.
    # ⚠ **선언된 고정으로 묻는다** — 고정 이름을 박아 두면 오너가 선언을 바꾼 날 시험이
    #   **선언이 아니라 옛 결정**을 재게 된다(2026-09-20 게이트에서 실제로 그렇게 빨개졌다).
    far, res, seconds = _fit({**declared, "core_radius_km": 1200.0},
                             declared["light_element_fixing"], 1)
    ok = far is None
    if not ok:
        fails.append("목표 1200 km 는 이 축이 감싸지 못하는데 값을 냈다 — 감싸지 못하면 거절해야 한다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 목표 1200 km 는 이 축이 **감싸지 못한다** → 값 없음 "
          f"({seconds:.0f} s)")

    apart = abs(frozen["fixings"]["box_floor"]["core_sulphur_wt"]
                - frozen["fixings"]["box_ceiling"]["core_sulphur_wt"])
    ok = apart > APART_MIN_WT
    if not ok:
        fails.append(f"두 고정의 S 가 {apart * 100:.2f} wt% 밖에 안 갈린다 — 고정 선택이 답을 "
                     "안 움직인다면 그 선언은 아무것도 안 하고 있는 것이다")
    print(f"  [{'PASS' if ok else 'FAIL'}] 두 고정이 **다른 답**을 준다 — S {apart * 100:.2f} wt% 차")

    if fails:
        print(f"\n[FAIL] {len(fails)}")
        for f in fails:
            print(f"  · {f}")
        return 1
    print(f"\n[PASS] 굳힌 고정 {len(frozen['fixings'])} · 방아쇠 파일 {len(TRIGGER_FILES)} "
          f"· 굳힌 날 {frozen['frozen_at']}")
    return 0


def main() -> int:
    if "--refresh" in sys.argv[1:]:
        return refresh()
    return check()


if __name__ == "__main__":
    raise SystemExit(main())
