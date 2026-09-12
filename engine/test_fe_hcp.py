# hcp 철 열 세트 — Table 1 의 «열» 을 꽂은 식이 자기 기준을 되돌려주고, 등급·배달 규칙이 축 둘을 다 본다 (브리프 187)
"""Gate: the Dorogokupets+ 2017 hcp column, wired as `fe_eps`'s γ·c_V set.

    python3 engine/test_fe_hcp.py

Anchors, each written before the run (`187-fe-eps-hcp-thermal-prereg.md`, 818cef2a + amendments):

J1  each column evaluated at its own T₀ and P = 0 returns its own printed V₀ — float precision.
    The reference temperature is a field of the column, and getting it wrong shifts the whole
    thermal pressure **silently**; this is the assertion that makes that failure loud.
J2  the electronic block's signs follow `g` and `g(1 − g)`, not `g` twice. hcp is the only
    column with a negative `g`, and `K_T,e = P_e(1 − g)` is negative for `g < 0` and `g > 1` alike.
J3  `thermal_at` is finite and continuous across the compression range — the path has never been
    walked with a negative `g` before this item.
J4  above the fit range the integrator and the core nodes get the **same** γ. That is the property
    the `graded-extrapolation` delivery rule exists to protect (Amendment 2).
J5  the grade reads both axes: pressure inside the range but temperature outside is graded, and a
    bounded set asked **without** a temperature is graded rather than passed (Amendment 3).
J6  `fe_prem`'s verdicts are untouched at both of its intervals.
J7  the ICB point is printed, not judged — see the SKIP note.
"""
from __future__ import annotations

import io
import os
import subprocess
import sys

import eos
import fe_liquid

GPA = 1e9

PAPERS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "docs", "phase3", "_papers")
SI_DOC = os.path.join(PAPERS, "2017NatSR...741863D-si-s1.doc")
PREM_TXT = os.path.join(PAPERS, "1981PEPI...25..297D-model-prem-burnman-v2.1.txt")

#: Table S3 의 열 이름, 인쇄된 순서. 값은 시험 시점에 파일에서 읽고 여기 적지 않는다.
S3_COLUMNS = ("p_gpa", "t_k", "x", "alpha_e6", "s", "c_v", "c_p", "k_t", "k_s",
              "gamma_th", "k_prime", "g_kj")


def _read_table_s3() -> list[dict]:
    """보유 SI 의 «Table S3. Thermodynamic properties of hcp-Fe» 를 읽는다.

    ⚠ **값을 코드에 적지 않는다** — 논문의 표는 파일에 있고, 시험은 그 파일에서 읽는다. 그래서
    표가 바뀌면 시험이 바뀌고, 우리가 옮겨 적은 수가 조용히 낡는 일이 없다.
    ⚠ `.doc` 은 legacy OLE 이라 macOS 의 `textutil` 로 푼다. 없으면 **건너뛰지 않고 이름을 대고
    비운다** — «도구가 없어서 안 돌았다» 와 «통과했다» 는 다른 사실이다."""
    if not os.path.exists(SI_DOC):
        return []
    try:
        out = subprocess.run(["textutil", "-convert", "txt", "-stdout", SI_DOC],
                             capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0:
        return []
    text = out.stdout.decode("utf-8", "replace")
    # ⚠ **상은 S-번호가 아니라 문자열로 고른다** (감사석, 2026-09-11). 보유 파일 이름은 논문의
    #   번호와 한 칸 어긋나 있다 — 논문의 «Table S3 = hcp» 인데 파일은 `si-s3-fcc`, `si-s4-hcp`
    #   다. 그래서 여기서는 캡션의 **상 이름**으로 잡고, 잡은 덩어리에 다른 상의 캡션이 섞여
    #   있지 않은지 확인한다. (`.doc` 은 표 전부를 담고 있으므로 파일 이름 함정은 워크북 쪽 것이다.)
    i = text.find("Thermodynamic properties of hcp-Fe")
    if i < 0:
        return []
    tail = text[i + 10:]
    ends = [tail.find(m) for m in ("Table S", "properties of liquid Fe", "properties of fcc-Fe")]
    ends = [e for e in ends if e >= 0]
    body = text[i:i + 10 + min(ends)] if ends else text[i:]
    for other in ("fcc-Fe", "bcc-Fe", "liquid Fe"):
        if other in body:
            return []
    rows: list[dict] = []
    for chunk in body.split("\x07\x07"):
        cells = [c.strip() for c in chunk.replace("\n", "\x07").split("\x07") if c.strip()]
        nums: list[float] = []
        for c in cells:
            try:
                nums.append(float(c))
            except ValueError:
                nums = []
                continue
        if len(nums) == len(S3_COLUMNS):
            rows.append(dict(zip(S3_COLUMNS, nums)))
    # ⚠ **상을 수로 한 번 더 확인한다** (감사석, 2026-09-11). 캡션 문자열만으로는 약하다:
    #   «328.9 GPa / 6000 K 행이 있다» 는 액체 표에도 있으므로 상을 가르지 못하고, «1811 K 행이
    #   없다» 는 **첫 행이 살아남았을 때만** 참이다 — 감사석의 파서는 각 압력 블록의 첫 행을
    #   떨어뜨렸고, 그러면 그 판별이 액체 표에서도 통과한다. 그래서 수로 묻는다: 상온·상압 행의
    #   K_T 는 Table 1 의 그 상 K₀ 다 (hcp 148.0 · fcc 146.2 · bcc 164.0 · liquid 83.7).
    ambient = [r for r in rows if r["t_k"] == 298.15 and r["p_gpa"] < 1.0]
    if not ambient:
        return []
    if abs(ambient[0]["k_t"] - fe_liquid.HCP.k0 / 1e9) > 0.01:
        return []
    return rows


def _read_prem_icb() -> tuple[float, float, float] | None:
    """PREM 표에서 내핵 경계의 두 밀도를 읽는다 — (반지름 m, 외핵쪽 ρ, 내핵쪽 ρ).

    ⚠ **단위 라벨이 틀렸다** (병렬석 실측): 머리글은 `Density(g/m^3)` 이라고 적는데 값은 kg/m³
    이다 (지각 2.6e3 … 중심 1.308848e4). **수를 믿고 라벨을 믿지 않는다.**
    ⚠ **불연속은 같은 깊이의 두 행으로 적혀 있다** — 그래서 «ICB 의 밀도» 는 조회가 아니라
    **어느 쪽인가의 선택**이다. 논문의 결손은 PREM **내핵쪽**에 대한 것이므로 그 행을 쓰고,
    둘 다 인쇄한다."""
    if not os.path.exists(PREM_TXT):
        return None
    rows = []
    for line in io.open(PREM_TXT, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.split()
        if len(f) >= 4:
            rows.append((float(f[1]), float(f[3])))       # radius, density
    pairs = {}
    for radius, rho in rows:
        pairs.setdefault(radius, []).append(rho)
    for radius, rhos in sorted(pairs.items()):
        # 내핵 경계는 «두 행이 있는 가장 안쪽 깊이»가 아니라 반지름으로 고른다: 중심에서 가장
        # 가까운 중복 반지름이 ICB 다 (그 아래는 내핵 한 상뿐이다).
        if len(rhos) == 2 and radius > 0.0:
            return radius, min(rhos), max(rhos)
    return None


def main() -> int:
    fails: list[str] = []
    notes: list[str] = []

    # ── J1 ────────────────────────────────────────────────────────────────
    for col in (fe_liquid.LIQUID, fe_liquid.HCP):
        v = fe_liquid.volume_at(0.0, col.t_ref, col)
        if abs(v / col.v0 - 1.0) > 1e-9:
            fails.append(f"J1 {col.name}: 자기 T₀({col.t_ref} K)·P=0 에서 V₀ 를 못 되돌린다 "
                         f"({v:.6e} 대 {col.v0:.6e})")

    # ── J2 ────────────────────────────────────────────────────────────────
    # ⚠ g > 1 인 열은 Table 1 에 없다. 규칙을 규칙으로 시험하려면 **합성 열**이 필요하고,
    #   그것이 철에 대한 주장이 아니라는 것을 여기 적는다 — 시험하는 것은 부호 규칙이다.
    synthetic = fe_liquid.Column(
        name="synthetic_g_gt_1", n_atom=1.0, v0=fe_liquid.HCP.v0, k0=fe_liquid.HCP.k0,
        k0p=fe_liquid.HCP.k0p, theta0=fe_liquid.HCP.theta0, gamma0=fe_liquid.HCP.gamma0,
        beta=fe_liquid.HCP.beta, gamma_inf=0.0, e0=fe_liquid.HCP.e0, g_el=1.5,
        t_ref=fe_liquid.HCP.t_ref, ref="synthetic — sign rule only, not a column of the paper")
    for col in (fe_liquid.LIQUID, fe_liquid.HCP, synthetic):
        v = col.v0 * 0.7
        p_e = fe_liquid._p_el(col, v, 4000.0)
        k_e = fe_liquid._k_t_el(col, v, 4000.0)
        if (p_e > 0) != (col.g_el > 0):
            fails.append(f"J2 {col.name}: P_e 의 부호가 g 를 따르지 않는다 (g={col.g_el}, P_e={p_e:.3e})")
        want_neg = col.g_el * (1.0 - col.g_el) < 0.0
        if (k_e < 0) != want_neg:
            fails.append(f"J2 {col.name}: K_T,e 의 부호가 g(1−g) 규칙과 다르다 "
                         f"(g={col.g_el}, K_T,e={k_e:.3e})")

    # ── J3 ────────────────────────────────────────────────────────────────
    prev = None
    for p_gpa in range(10, 601, 10):
        out = fe_liquid.thermal_at(p_gpa * GPA, 4000.0, fe_liquid.HCP)
        for key, val in out.items():
            if val != val or abs(val) == float("inf"):
                fails.append(f"J3 {p_gpa} GPa: {key} 가 유한하지 않다 ({val})")
        if prev is not None:
            jump = abs(out["gruneisen"] / prev["gruneisen"] - 1.0)
            if jump > 0.05:
                fails.append(f"J3 {p_gpa} GPa: γ 가 한 걸음에 {jump * 100:.1f} % 튄다 — 연속이 아니다")
        prev = out

    # ── J4 ────────────────────────────────────────────────────────────────
    mat = eos.MATERIALS["fe_eps"]
    p, t = 400.0 * GPA, 5000.0
    rho = mat.density(p, t, 0.0)
    integrator_gamma = mat.gruneisen(p, rho, t, 0.0)
    node_gamma, verdict, own, _density = eos.core_gamma(mat, p, t, 0.0, rho)
    if verdict != "graded-extrapolation":
        fails.append(f"J4: 적합 범위 위의 판정이 graded-extrapolation 이 아니다 ({verdict})")
    if abs(node_gamma - integrator_gamma) > 1e-12:
        fails.append(f"J4: 한 질문에 답이 둘이다 — 적분기 {integrator_gamma!r} 대 핵 노드 {node_gamma!r}")
    if abs(own - integrator_gamma) > 1e-12:
        fails.append(f"J4: «재질이 말한 값» 칸이 적분기의 값과 다르다 ({own!r} 대 {integrator_gamma!r})")

    # ── J5 ────────────────────────────────────────────────────────────────
    ph = mat.phases[0]
    cases = ((100.0, 3000.0, "ok"),
             (349.0, 6000.0, "ok"),
             (100.0, 7000.0, "graded-extrapolation"),
             (400.0, 5000.0, "graded-extrapolation"))
    for p_gpa, t_k, want in cases:
        got, _dens = ph.thermal_label(mat.fit_composition, p_gpa * GPA, t_k)
        if got != want:
            fails.append(f"J5 {p_gpa} GPa / {t_k} K: 판정 {got!r}, 등록된 것은 {want!r}")
    got_no_t, _dens = ph.thermal_label(mat.fit_composition, 100.0 * GPA)
    if got_no_t != "graded-extrapolation":
        fails.append(f"J5: 온도 없이 물었는데 {got_no_t!r} 다 — 「온도 모름」은 통과가 아니라 등급이다")

    # ── J5B — 바닥만 선언한 세트가 그 아래를 등급으로 낸다 (C84, 브리프 198) ───────────────
    # ⚠ **이 검사가 지키는 것은 이른 반환이다.** `covers_t` 의 예전 판은 `t_max` 가 없으면 `t` 를
    #   보지도 않고 참을 냈다. 거기에 하한만 더하면 «하한만 선언한 세트» 는 여전히 무경계로 남고,
    #   그 모양이 바로 액체 철 두 세트다 — 198 B 가 바닥을 선언할 가장 유력한 자리다. 그래서 축을
    #   **하나만** 든 세트를 여기서 직접 만들어 묻는다. 출하 세트는 198 에서 아무도 바닥을 선언하지
    #   않으므로(그래서 값이 안 움직인다) 이 경우는 합성으로만 존재한다.
    floor_only = eos.ThermalSet(p_min=0.0, p_max=1e30, t_min=1000.0,
                                ref=ph.gamma_sets[0].ref,
                                source_state=ph.gamma_sets[0].source_state,
                                source_composition=ph.gamma_sets[0].source_composition)
    checks = ((None, False, "온도 없이"), (500.0, False, "바닥 아래"),
              (5000.0, True, "바닥 위"))
    for t_k, want, label in checks:
        if floor_only.covers_t(t_k) is not want:
            fails.append(f"J5B: 하한만 선언한 세트에 {label} 물었더니 {floor_only.covers_t(t_k)!r} "
                         f"— 등록된 것은 {want!r} (이른 반환이 바닥을 건너뛴다)")
    unbounded = eos.ThermalSet(p_min=0.0, p_max=1e30, ref=ph.gamma_sets[0].ref,
                               source_state=ph.gamma_sets[0].source_state,
                               source_composition=ph.gamma_sets[0].source_composition)
    if not all(unbounded.covers_t(x) for x in (None, 1.0, 1e9)):
        fails.append("J5B: 두 끝이 다 비었는데 무경계가 아니다 — 198 은 기존 거동을 안 바꾼다")

    # ── J6 ────────────────────────────────────────────────────────────────
    prem = eos.MATERIALS["fe_prem"]
    for p_gpa, t_k, want in ((25.0, 2100.0, "composition-substitute"),
                             (40.0, 3000.0, "graded-disagreement")):
        got, dens = prem.phases[0].thermal_label(prem.fit_composition, p_gpa * GPA, t_k)
        if got != want or dens != "phase-mismatch":
            fails.append(f"J6 fe_prem {p_gpa} GPa: ({got!r}, {dens!r}) — 예전과 다르다, "
                         f"({want!r}, 'phase-mismatch') 여야 한다")

    # ── J3R — 논문 자신의 표를 되짚는다 (Table S3, 보유 SI) ─────────────────
    # ⚠ 이 표는 **같은 식을 저자가 돌린 값**이다. 그래서 차이가 인쇄 반올림보다 크면 그것은
    #   «다른 데이터» 가 아니라 **우리 구현이 다르다** 는 뜻이고, 그것이 이 시험의 내용이다.
    #   허용오차는 값을 보기 전에 정한다: 밀도(x) 0.2 %, 그 밖의 열량 0.5 %.
    s3 = _read_table_s3()
    if not s3:
        notes.append("[SKIP] J3R Table S3 — SI 를 못 읽었다 (파일 없음 또는 `textutil` 없음). "
                     "«안 돌았다» 이고 «통과» 가 아니다")
    else:
        want = [(0.0001, 298.15), (100.0, 2000.0), (328.9, 6000.0)]
        picked = [r for r in s3 if (round(r["p_gpa"], 4), r["t_k"]) in
                  {(round(p, 4), t) for p, t in want}]
        if len(picked) < 3:
            fails.append(f"J3R: 등록한 세 행 {want} 중 {len(picked)}개만 표에서 찾았다")
        # ⚠ **이 재현이 덮는 곳을 같이 인쇄한다** (감사석, 2026-09-11). 표의 격자는 압력
        #   0.0001·10·100·200·328.9 GPa 이고 온도 천장은 압력과 함께 2500 K 에서 6000 K 까지
        #   올라간다 — 즉 **전부 구간 ① 안**이다. «J3R 통과» 를 외삽 구간 ② 의 증거로 읽으면
        #   안 되고, 그 사실은 시험 자신이 말해야 한다.
        p_axis = sorted({r["p_gpa"] for r in s3})
        t_ceiling = max(r["t_k"] for r in s3)
        if p_axis[-1] * GPA > eos.DOROGOKUPETS_FIT_P_MAX or t_ceiling > eos.DOROGOKUPETS_FIT_T_MAX:
            fails.append(f"J3R: 표가 적합 범위 밖까지 뻗는다 ({p_axis[-1]} GPa · {t_ceiling} K) — "
                         "구간 ① 안이라는 이 시험의 전제가 깨졌다")
        notes.append(f"  J3R 격자 {p_axis} GPa · 온도 천장 {t_ceiling:.0f} K — **전부 구간 ①** "
                     f"(≤ {eos.DOROGOKUPETS_FIT_P_MAX / GPA:.0f} GPa · "
                     f"≤ {eos.DOROGOKUPETS_FIT_T_MAX:.0f} K) 안이다. 외삽 구간 ② 를 시험하는 "
                     "인쇄 자료는 없다")
        for row in picked:
            p_pa, t_k = row["p_gpa"] * GPA, row["t_k"]
            got = fe_liquid.thermal_at(p_pa, t_k, fe_liquid.HCP)
            x_got = fe_liquid.volume_at(p_pa, t_k, fe_liquid.HCP) / fe_liquid.HCP.v0
            checks = ((("x", x_got, row["x"], 0.002)),
                      ("gamma_th", got["gruneisen"], row["gamma_th"], 0.005),
                      ("c_v", got["c_v"] * fe_liquid.MOLAR_MASS, row["c_v"], 0.005),
                      ("k_t", got["k_t"] / GPA, row["k_t"], 0.005))
            for name, mine, printed, tol in checks:
                if printed == 0.0:
                    continue
                rel = abs(mine / printed - 1.0)
                if rel > tol:
                    fails.append(f"J3R {row['p_gpa']} GPa / {t_k} K {name}: {mine:.6g} 대 인쇄값 "
                                 f"{printed:.6g} — {rel * 100:.3f} % 로 {tol * 100:.1f} % 를 넘는다")

    # ── J8 — 재질의 **호출 표면**이 두 구간 다에서 수를 낸다 ─────────────────
    # ⚠ **이 시험이 있는 이유가 187 의 교훈이다** (지휘석 규칙, 2026-09-11): 깨끗한 트리에서
    #   `fe_prem.c_p` 는 35 GPa 위에서 `ZeroDivisionError` 를 던지고 있었고, **어떤 천체도 그
    #   메서드를 안 불러** 천체 기준선 전체가 초록이었다. 수용선은 천체가 아니라 **재질의 호출
    #   표면**까지 재야 한다. 평가자 세트는 `c_v_ref` 가 0 이므로 상수 경로로 들어가면 0 으로
    #   나눈다 — 그 길이 다시 열리면 여기서 잡힌다.
    for name in ("fe_eps", "fe_prem"):
        mat_s = eos.MATERIALS[name]
        for p_gpa in (1.0, 19.5, 40.0, 100.0, 349.0, 351.0, 1000.0):
            for t_k in (300.0, 2000.0, 5000.0):
                for call in ("c_p", "grad_ad", "k_t"):
                    try:
                        val = getattr(mat_s, call)(p_gpa * GPA, t_k)
                    except Exception as exc:                      # noqa: BLE001
                        fails.append(f"J8 {name}.{call}({p_gpa} GPa, {t_k} K): "
                                     f"{type(exc).__name__} — 호출 표면이 예외를 던진다")
                        continue
                    if val != val or abs(val) == float("inf"):
                        fails.append(f"J8 {name}.{call}({p_gpa} GPa, {t_k} K): {val}")

    # ── J7 — ICB 결손, 논문이 인쇄한 값에 대해 판정한다 ──────────────────────
    # ⚠ 논문이 인쇄하는 것은 밀도가 아니라 **PREM 대비 결손 4.4 %** 다 (T = 5882 K,
    #   P = 328.9 GPa). 그래서 PREM 쪽 수가 필요하고, 그것은 보유 모델표에서 읽는다.
    icb = fe_liquid.thermal_at(328.9 * GPA, 5882.0, fe_liquid.HCP)
    prem = _read_prem_icb()
    if prem is None:
        notes.append(f"[SKIP] J7 ICB — PREM 모델표 미보유. hcp 밀도 {icb['density']:.1f} kg/m³ "
                     f"인쇄만 하고 판정 안 함")
    else:
        radius, rho_outer, rho_inner = prem
        # ⚠ **판정하지 않는다 — 분모가 인쇄되어 있지 않다** (브리프 187 Amendment 8). 논문은
        #   4.4 % 를 두 번 적고 **정의는 한 번도 적지 않는다**. 철을 분모로 잡으면 4.2 %, PREM 을
        #   분모로 잡으면 4.4 % 이고, 둘 중 하나를 골라 «맞았다» 고 말하는 것은 우리가 정의를
        #   고르는 것이다. 구현의 증거는 J3R 이다 — 저자 자신의 표를 같은 (P, T) 에서 다섯 자리로
        #   되짚는다. 이 줄은 그 옆의 참고 수치다.
        d_iron = (1.0 - rho_inner / icb["density"]) * 100.0
        d_prem = (icb["density"] / rho_inner - 1.0) * 100.0
        notes.append(f"  J7 ICB {radius / 1e3:.1f} km — PREM 외핵쪽 {rho_outer:.1f} · 내핵쪽 "
                     f"{rho_inner:.1f} kg/m³ (라벨은 g/m^3 이지만 값은 kg/m³), hcp "
                     f"{icb['density']:.1f} kg/m³ → 결손 {d_iron:.2f} %(철 분모) / {d_prem:.2f} "
                     f"%(PREM 분모) 대 인쇄 4.4 %. **판정 안 함** — 논문은 수를 두 번 적고 정의를 "
                     f"한 번도 안 적는다")

    for f in fails:
        print(f"  [FAIL] {f}")
    for n in notes:
        print(f"  {n}")
    if not fails:
        print("  [PASS] hcp 열 세트 — J1 두 열의 V₀ 복원(부동소수) · J2 g 와 g(1−g) 부호 규칙 "
              "(합성 열로 g>1 까지) · J3 10–600 GPa 연속·유한 · J3R 저자의 Table S3 세 행 재현 "
              "(0.0001·100·328.9 GPa, 값은 보유 SI 에서 시험 시점에 읽는다) · J4 적분기와 핵 "
              "노드가 같은 γ (graded-extrapolation 배달) · J5 축 둘 다 보는 등급 · J5B 하한만 선언한 "
              "세트가 그 아래를 등급으로 낸다 (C84) · 온도 없으면 "
              "등급 · J6 fe_prem 판정 불변 · J8 두 재질의 호출 표면(c_p·grad_ad·k_t)이 두 "
              "구간 다에서 유한 · J7 은 인쇄만 (정의 미인쇄)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
