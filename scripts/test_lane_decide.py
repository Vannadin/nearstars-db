# auto-lane 기대 빨강 인정 규칙(C128)의 합성 로그 자기 시험 다섯
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import lane_decide as ld

T = [{"id": "C59", "step": "run.py bodies/mars.yaml (출하값 대조)", "mismatch_keys": ["nmoi"],
      "values": {"nmoi": [0.3571, 0.3634]}}]
M = "run.py bodies/mars.yaml (출하값 대조)"


def body(step, mis, fail=True):
    out = [f"    [어긋남] {k:<14} 엔진    {a} · 보드   {b}   (1.7% / 허용 1%)" for k, a, b in mis]
    if fail:
        out.append(f"  [FAIL] {step} — 비0 종료 (이 단계가 fail=1 을 세웠다)")
    out += [f"  [TIME] {step} — 1 s", f"  [COST] {step} — instr 1"]
    return out


def log(*parts):
    return "\n".join(["GATE START"] + [l for p in parts for l in p] + ["GATE END rc=1"])


def run(text):
    return ld.expected_red_only(text, T)[0]


def test_known_shape_accepted():
    assert run(log([f"  [STEP] {M} — 시작 (풀)"], body(M, [("nmoi", "0.3571", "0.3634")])))


def test_1_extra_key_rejected():
    assert not run(log(body(M, [("nmoi", "0.3571", "0.3634"), ("radius", "1", "2")])))


def test_2_other_step_rejected():
    assert not run(log(body("run.py bodies/earth.yaml (출하값 대조)", [("nmoi", "1", "2")])))


def test_3_rc0_accepted_with_green_note():
    import tempfile
    tmp_path = pathlib.Path(tempfile.mkdtemp())
    real_load = ld._load_expected_red
    ld._load_expected_red = lambda: T
    try:
        _test_3_body(tmp_path)
    finally:
        ld._load_expected_red = real_load                     # r2 n2 (3b): restore, so later tests see the file


def _test_3_body(tmp_path):
    (tmp_path / "gate-x.log").write_text(
        "GATE START\n" + "\n".join(body(M, [], fail=False)) +
        "\nGATE END sha=abc1234 date=2026-09-29+0900 lane=full rc=0\n")
    real = ld.subprocess.run
    ld.subprocess.run = lambda *a, **k: type("R", (), {"returncode": 0})()   # sha 조상 판별만 건너뜀
    try:
        ok, notes = ld.full_ran_today(tmp_path, "2026-09-29")
    finally:
        ld.subprocess.run = real
    assert ok and any("C59 가 초록" in n for n in notes)


def test_4_rc1_no_fail_rejected():
    assert not run(log(body(M, [("nmoi", "0.3571", "0.3634")], fail=False)))


def test_5_neighbour_mismatch_not_counted():
    # 이웃 풀 단계의 [어긋남] 은 C59 구간 밖 — 키 집합은 {nmoi} 그대로
    other = ["    [어긋남] radius  엔진 1 · 보드 2", "  [TIME] test_x — 1 s", "  [COST] test_x — instr 1"]
    assert run(log(other, body(M, [("nmoi", "0.3571", "0.3634")])))
    # 반대로 구간 안에 들어오면 불인정
    assert not run(log(body(M, [("nmoi", "0.3571", "0.3634"), ("radius", "1", "2")])))


def test_size_change_noted():
    ok, notes = ld.expected_red_only(log(body(M, [("nmoi", "0.3580", "0.3634")])), T)
    assert ok and any("크기 바뀜" in n for n in notes)


def test_size_change_noted_on_a_rejected_log():
    """s4r C59-NOTE-DROPPED (지휘 11-08): the s4r shape — an unexpected FAIL first (the unwired list), then C59's step
    with a moved engine value. The verdict is False, and the value note still comes back, after the reason. Mutant: the
    old return (`return False, [why]` with the notes dropped) gives no «크기 바뀜» here."""
    first = ["  [FAIL] 안 엮인 시험 engine/test_d2_nan.py"]
    ok, why = ld.expected_red_only(log(first, PC_BLOCKS[C59["step"]]), [C59])
    assert not ok
    assert why[0].startswith("기대 밖 FAIL: [FAIL] 안 엮인 시험 engine/test_d2_nan.py"), why
    assert "참고: ⚠ C59 core_radius_fraction 엔진 0.5003 · 보드 0.5398 (옛 0.5002 · 0.5398) — 크기 바뀜" in why, why
    # an unmoved value gives no note on a rejected log either
    same = _edit(PC_BLOCKS[C59["step"]], "엔진    0.5003", "엔진    0.5002")
    assert not any("크기 바뀜" in w for w in ld.expected_red_only(log(first, same), [C59])[1])


def test_no_cost_line_rejected():
    assert not run(log([f"    [어긋남] nmoi 엔진 0.3571 · 보드 0.3634", f"  [FAIL] {M} — 비0 종료 (이 단계가 fail=1 을 세웠다)"]))



# ── SG-MARS-HOLD-ENGINE (kind table_triggers; ES-f6 note 3 §3.1, r2 B1 on bdde1c54) ─────────────────────────────
#: the three step ranges of the PC gate of record (artifacts 05eb977a pc/vr-base/out-pc/gate.log), verbatim
PC_BLOCKS = json.loads(r'''{
"structure_grid.py --check": [
"  [PASS] earth.json — 방아쇠 그대로",
"  [FAIL] mars.json — 데이터 방아쇠 ['declared.basal_layer_density', 'declared.basal_layer_thickness_km', 'declared.core_light_elements', 'declared.mantle_composition', 'bytes.chain.yaml', 'bytes.reference_adiabats.json', 'chain_reads', 'sulphur_fixings', 'mantle_table'] 가 움직였다 — `--refresh mars`",
"  [PASS] venus.json — 방아쇠 그대로",
"  [FAIL] structure_grid.py --check — 비0 종료 (이 단계가 fail=1 을 세웠다)",
"  [TIME] structure_grid.py --check — 22:40:16 → 22:40:16 · 0 s · RSS 63 MB",
"  [COST] structure_grid.py --check — user 2.25 · sys 0.28 · invcsw 5901 · pf 0 · pr 26126 · instr 16422275812 · cycles 10495300404 · blkin 0 · blkout 0"
],
"test_structure_grid.py": [
"  [PASS] 굳힌 표가 있다 — earth.json, mars.json, venus.json",
"  [PASS] earth.json — 방아쇠 그대로 — 격자 1369.0–3090.0 K · T_ok None",
"  [PASS] earth.json — 격자 아래 거절 — 구조 표 격자 아래 — t_m 1367.9603209180652 K < 1368.9603209180652 K (외삽 없음, prereg-structure-grid 덧붙임 7 ①)",
"  [PASS] earth.json — 격자 위 거절(구조가 풀리는 표) — 구조 표 격자 위 — t_m 3091.0 K > 3090.0 K (외삽 없음)",
"  [PASS] earth.json — 격자 점에서 그 점의 값(비트)",
"  [PASS] earth.json — 두 점 사이는 두 값 사이",
"  [PASS] earth.json — 선언이 움직이면 낡은 표로 거절 — 구조 표가 낡았다 — 방아쇠 ['declared.potential_temperature'] 가 움직였다. 조용히 다시 풀지 않는다: `python3 engine/structure_",
"  [FAIL] mars.json — 방아쇠 그대로 — 구조 표가 낡았다 — 방아쇠 ['declared.basal_layer_density', 'declared.basal_layer_thickness_km', 'declared.core_light_elements', 'declared.mantle_composition', 'bytes.chain.yaml', 'bytes.reference_adiabats.json', 'chain_reads', 'sulphur_fixings', 'mantle_table'] 가 움직였다. 조용히 다시 풀지 않는다: `python3 engine/structure_grid.py --refresh mars`",
"  [PASS] venus.json — 방아쇠 그대로 — 격자 1723.3–3188.9 K · T_ok None",
"  [PASS] venus.json — 격자 아래 거절 — 구조 표 격자 아래 — t_m 1722.2707215742134 K < 1723.2707215742134 K (외삽 없음, prereg-structure-grid 덧붙임 7 ①)",
"  [PASS] venus.json — 격자 위 거절(구조가 풀리는 표) — 구조 표 격자 위 — t_m 3189.87 K > 3188.87 K (외삽 없음)",
"  [PASS] venus.json — 격자 점에서 그 점의 값(비트)",
"  [PASS] venus.json — 두 점 사이는 두 값 사이",
"  [PASS] venus.json — 선언이 움직이면 낡은 표로 거절 — 구조 표가 낡았다 — 방아쇠 ['declared.potential_temperature'] 가 움직였다. 조용히 다시 풀지 않는다: `python3 engine/structure_",
"  [PASS] 받을 답 없는 구간 안 → gap · 높은 T 끝 값 — gap 3.0",
"  [PASS] 구간 밖 → 보간 그대로 — ok 1.5",
"  [PASS] 구간 끝점 t₊ → 그 점의 값(ok) — ok",
"  [PASS] 덧붙임 55 — 풀 1 · 풀 3 바이트 같음 · 받을 답 없는 구간 있음",
"  [PASS] 덧붙임 55 — 버린 미리 풀기 > 0 — [2]",
"  [PASS] 덧붙임 57 ① — 판 깊이 1 · 2, 풀 1 · 3 바이트 같음(힌트 없음)",
"  [PASS] 덧붙임 55 음성 N1 — 찾기 전 캐시에 넣으면 ④ 대조가 떨어진다 — fake: 미리 푼 점이 찾기 전에 캐시에 들었다 [1002.25, 1003.75] (덧붙임 55 ④)",
"  [PASS] 덧붙임 57 — 오름 · 내림 · 힌트 · 풀 3 판정 줄 바이트 같음",
"  [PASS] 덧붙임 57 — 힌트 없으면 거절될 점이 고정 출발 셋으로 답(2075 꼴) — [2075.0]",
"  [PASS] 덧붙임 57 음성 — 힌트가 a 멤버에 새면 오름 · 내림이 갈린다",
"  [PASS] 덧붙임 58 ② — 초반에만 헤맨 풀이는 가족 검사가 안 섬",
"  [PASS] 덧붙임 58 ② 음성 — 같은 풀이를 옛 «모든 시행» 으로 세면 선다 — 3",
"  [PASS] 덧붙임 58 노트 — 첫 시행 전에 거절한 호출은 창 없음(앞 호출을 안 빌림)",
"  [PASS] 덧붙임 59 ② — 가운데 점에서만 선 가족 검사도 그 구간을 1 K 까지 쪼갬(1003 이 표 점) — [1000.0, 1002.0, 1003.0, 1004.0, 1006.0, 1008.0]",
"  [PASS] 덧붙임 59 음성 — 끝점 판이면 같은 가짜에서 구간이 닫혀 끝 점검이 이름 대고 거절 — fake: 닫힌 구간 안에 가족 검사가 선 점이 남았다 (덧붙임 59 ④) — [(1002.0, 1004.0, [1003.0])]",
"  [PASS] 덧붙임 59 ① — 미리 풀기 깊이 1 · 2 바이트 같음(버린 미리 풀기는 F 밖)",
"  [PASS] 덧붙임 58 ① — 용융 상태가 바뀌는 구간을 거절 없이 0.25 K 까지 쪼갬 — [1005.25, 1005.5]",
"  [PASS] C162 ① — 안쪽 한 점의 C152 거절은 멈춤 없이 «거절» 구간 하나(까닭 · 폭 ≤ 1 K) — [[1002.75, 1003.25, '표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0 을 건너뛴다 (C152 가짜)', 'refusal', None, {'s_min': None, 'graze_points': 0, 'points': 1}]]",
"  [PASS] C162 ① — 짓기 로그가 그 구간을 «(거절)» 로 찍음",
"  [PASS] C162 ① — 읽기는 그대로: 구간 안은 gap — gap",
"  [PASS] C162 ② — 거절 구간 셋이면 상한(둘) 넘음: 구간 전부를 이름 대고 멈춤 — fake: 거절 구간이 상한을 넘는다 (3 개 > 2) — [1000.75, 1001.25] K 폭 0.500 K: 표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0 을 건너뛴다 (C152 가짜) · [1002.75, 1003.25] K 폭 0.500",
"  [PASS] C162 ② — 폭 2.0 K 넘는 거절 구간 하나면 멈춤 — fake: 거절 구간이 상한을 넘는다 (폭 3.000 K > 2.0 K) — [1002.5, 1005.5] K 폭 3.000 K: 표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0 을 건너뛴다 (C152 가짜)",
"  [PASS] C157 메모 5 — 스침 표지 3 K 거절 구간은 멈추지 않음(다섯째 칸 onset_graze · 폭 3 K 그대로 기록) — [[1002.5, 1005.5, '표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0 을 건너뛴다 (C152 가짜) — 경계 스침 — 고상선 · silicate 16.600 GPa (T − T_경계 -0.200 K) · 민감도 S 6522 (C157 메",
"  [PASS] C157 메모 5 음성 — 같은 폭의 표지 없는 구간은 멈춤(위 «C162 ② 폭» 과 같은 가짜, 표지만 뺌)",
"  [PASS] C157 메모 5 — 표지 구간도 개수 상한(둘)엔 셈: 셋이면 멈춤 — fake: 거절 구간이 상한을 넘는다 (3 개 > 2) — [1000.75, 1001.25] K 폭 0.500 K: 표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0 을 건너뛴다 ",
"  [PASS] C157 메모 5 — 문서 판: 표지 구간은 폭 사유 없음, 표지 없는 같은 폭은 사유",
"  [PASS] 메모 7 — 모두 S > 10 · 스침 하나 이상인 3 K 구간은 표지(폭 면제) · 여섯째 칸 셈 — [[1002.5, 1005.5, '표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0 을 건너뛴다 (C152 가짜) — 경계 스침 — 고상선 · silicate 16.600 GPa (T − T_경계 -0.200 K) · 민감도 S 6522 (C157 메모 5)', 'refusal', 'onset_graze', {'s_min",
"  [PASS] 메모 7 음성 — 거절 한 점이라도 S < GRAZE_SLOPE 면 표지 없음 → 폭 상한에 멈춤 — fake: 거절 구간이 상한을 넘는다 (폭 3.000 K > 2.0 K) — [1002.5, 1005.5] K 폭 3.000 K: 표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0",
"  [PASS] 메모 7 음성 — 모두 S > 10 이어도 스침 점이 없으면 표지 없음 → 멈춤 — fake: 거절 구간이 상한을 넘는다 (폭 3.000 K > 2.0 K) — [1002.5, 1005.5] K 폭 3.000 K: 표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0",
"  [PASS] 메모 7 규칙 5 — 쌍이 없는(S 없는) 거절 문구는 S None",
"  [PASS] 메모 7 수락 2b — 실제 거절 문구를 같은 파서가 S 6522 · 16.627 GPa 스침으로 읽음 — 6522.0 고상선 · silicate 16.627 GPa (T − T_경계 -0.206 K)",
"  [PASS] 메모 7 규칙 4 — 형식기 → 파서 왕복(S 1.578e+04 · 스침) — 15780.0 고상선 · silicate 16.628 GPa (T − T_경계 -0.308 K)",
"  [PASS] C162 ② — 판정 구간(셋째 칸까지)은 상한에 안 셈",
"  [PASS] C162 ② — 문서 판: 거절 구간 셋 · 폭 넘는 하나는 상한 사유",
"  [PASS] C162 음성 — C157 뒷받침 거절은 멈춤 그대로(규칙 3) — fake: 1003.0 K 에서 구조가 거절한다 — 격자 안에서 단조가 아니다: 사격 질량이 p_c 에서 뛴다 (적분 피적분 불연속) — 가짜",
"  [PASS] C162 음성 — 아래 끝 거절은 멈춤(격자 끝) — fake: 격자 끝 1000.0 K 가 받을 답 아님 — 표면온도 잔차가 뛴다 — 중심 온도 [4052.41, 4052.42] K 사이에서 0 을 건너뛴다 (C152 가짜)",
"  [PASS] C162 음성 — cmf 어긋남은 멈춤 — fake: 1004.0 K 의 cmf 0.31 가 S0 0.3 와 다르다 — 조성이 고정이 아니다",
"  [PASS] C162 ② — --check 가 구간 전부를 까닭과 찍음: 거절 [WARN] · 판정 [기록], 상한 안이면 FAIL 없음(표 없는 몸 둘만) — bad 2",
"  [PASS] C157 메모 5 — --check 가 표지 구간을 폭 · 표지와 찍고 FAIL 없음(18 K 띠) — bad 2",
"  [PASS] C157 메모 5 — 열진화 메모가 건넌 구간의 폭을 찍음 — ('구조 표의 받을 답 없는 구간 [2073.00, 2091.00] K (폭 18.00 K) 를 높은 T 쪽 값으로 건넘 — 5 걸음 (호출 2, 냉각 이력, prereg-structure-grid 덧붙임 50)',",
"  [PASS] C162 ② — 거절 구간 셋을 든 표는 --check FAIL — bad 3",
"  [PASS] 표가 없는 바디 → 이름 대고 거절 — 구조 표가 없다 — `engine/structure_grid/nosuchbody.json`. 열진화는 걸음마다 구조 표를 보간한다(오너 결정 2026-09-24). `python3",
"  [PASS] 덧붙임 60 — 고정 풀이는 호출 동안만 interior._PIN 에 (S0 T_c · 중심압) 을 걸고 지운다 — {'pin': (2440.18, 39930000000.0), 't': 1600.0}",
"  [PASS] 덧붙임 60 — 같은 T_c 의 같은 풀이는 통과(칸마다 SHOOT_TOL 대비 비율을 찍음) — SHOOT_TOL 대비 radius 0 · nmoi 0 · core_radius 0 · core_radius_fraction 0 · cmb_pressure 0 · cmb_temperature 0 (가장 큰 칸 rad",
"  [PASS] 덧붙임 60 음성 — 심은 조성 불일치(반지름 SHOOT_TOL 의 10 배)는 고정 T_c 에서 실패 — SHOOT_TOL 대비 radius 10 · nmoi 0 · core_radius 0 · core_radius_fraction 0 · cmb_pressure 0 · cmb_temperature 0 (가장 큰 칸 ra",
"  [PASS] 덧붙임 60 음성 — 고정 T_c 를 1e-6 흔들면 실패(고정이 안 잡혔다) — 고정이 안 잡혔다 — 돌려받은 T_c 2440.1824401799995 K 대 S0 2440.18 K",
"  [PASS] 덧붙임 60 — 고정 풀이가 답을 안 내면 실패",
"  [PASS] 덧붙임 61 — 뜀 확인 이분이 받을 답 없는 점에 닿으면 그 둘레를 구간으로 싣고 끝난다(죽지 않음) — [[2401.3671875, 2401.751708984375, '수렴 표지 False — 표면 온도가 허용(T_SURFACE_TOL) 밖이거나 사격이 안 닫힘']]",
"  [PASS] 덧붙임 61 음성 — 고치기 전 코드(e9e8ab3f)는 같은 가짜에서 _NoAnswer 로 죽는다(시험이 그 길을 밟는다)",
"  [PASS] 덧붙임 61 — 지문 불연속 이분이 받을 답 없는 점에 닿아도 _NoAnswer 로 죽지 않는다(등록된 지문 멈춤까지 간다) — fake61f: 보간 불가 구간 [2400.0, 2400.68359375] K — 지문 ['rocky', None, 'liquid'] → ['rocky', Non",
"  [PASS] 덧붙임 61 음성 — 고치기 전 코드는 지문 이분에서도 _NoAnswer 로 죽는다",
"  [PASS] 덧붙임 60 후속 — 풀이 동안 구조를 붙잡으면 id 가 안 겹치고 마지막 구조의 호출 번호가 맞다 — 7 vs 7 · 재사용 False",
"  [PASS] 덧붙임 60 후속 음성 — 붙잡기를 끄면 id 가 재사용되고 기록이 옛 호출 번호를 돌려준다(시험이 그 길을 밟는다) — 0 vs 7 · 재사용 True",
"  [PASS] 덧붙임 60 후속 음성 — `_integrate_raw` 의 붙잡기 줄을 지운 변형은 목록이 켜져 있어도 id 가 재사용된다(E-id 의 자리를 잰다) — 0 vs 7 · 재사용 True",
"  [PASS] 덧붙임 60 후속 — 이력 무관: 고정 풀이 한 번 뒤에도 지구 2062 K 의 값 · 바깥 호출 기록이 비트까지 같다 — 답 호출 6 대 6 · 값 같음 True",
"  [PASS] 덧붙임 60 후속 음성 — 둘째 이력에 id 충돌을 심으면 답 호출이 갈라져 잡힌다 — 심음 0 대 6",
"  [기록] C152 메모 8 화성 1782 · 1771.5 K 네 줄 — 층 판 황 앵커가 아니다(box_ceiling cmf 0.21265490746167065): 이 창에 안 놓여 해당 없음",
"  [PASS] C163 F-planted — 근 위 두 시행(|y| 5e-4 · 3e-4 < tol)이 다른 띠면 가족 둘(진짜 «답 둘» 은 여전히 선다) — [(2.0, 7.0, 0.41), (3.0, 8.0, 0.41)]",
"  [PASS] C163 F-planted 짝 — 먼 띠가 근 밖 시행(|y| 5e-3)에만 있으면 가족 하나(거르지 않으면 둘 — 거르기가 일한다) — 걸러서 1 · 안 걸러서 2",
"  [PASS] C157 메모 11 — 심은 뜨거운 물 곡선의 스침이 실제로 밟은 재료 h2o_hot 에 붙는다(암석 0%) — ('심은 곡선', 'h2o_hot', 100111287066.82376, 0.500001237104243)",
"  [PASS] C157 메모 11 — 심은 뜨거운 물 곡선의 스침이 실제로 밟은 재료 h2o_hot_rock 에 붙는다(암석 20%) — ('심은 곡선', 'h2o_hot_rock', 99840204655.94116, 0.5000025575413929)",
"  test_structure_grid — 실패 1",
"  [FAIL] test_structure_grid.py — 비0 종료 (이 단계가 fail=1 을 세웠다)",
"  [TIME] test_structure_grid.py — 22:41:09 → 22:52:05 · 656 s · RSS 621 MB",
"  [COST] test_structure_grid.py — user 654.29 · sys 1.26 · invcsw 2072 · pf 0 · pr 358056 · instr 6570885753661 · cycles 3092000715682 · blkin 0 · blkout 0"
],
"run.py bodies/mars.yaml (출하값 대조)": [
"  [고리] 시행 7 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8241e-07",
"  [고리] 시행 7 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8241e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 1.37876297567896e-07: T_c 2279.763692 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 5.2101e-08",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 7.664807485374681e-08: T_c 2448.107831 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 2.6116e-07",
"  [고리] 시행 5 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8085e-07",
"  [고리] 시행 7 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 5.2532e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 2.989655145668735e-08: T_c 2838.573290 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 8.5519e-08",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1.4754126920202282e-08 · 1e-08: T_c 2948.239626 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 2.5793e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 7.40736913584783e-08 · 6.542002168208328e-07: T_c 3003.762874 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 6.7998e-08",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 3.5316530877516075e-08 · 1.924528720609331e-07: T_c 3118.500655 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 6.3556e-10",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 7.280576228563263e-08: T_c 2448.107904 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 2.9956e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 8.657751915386314e-08: T_c 2448.107644 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.6184e-07",
"  [고리] 시행 5 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8086e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 4.280141725487852e-08: T_c 2530.454405 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.4934e-07",
"  [고리] 시행 8 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 6.6851e-07",
"  [고리] 시행 7 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8241e-07",
"  [고리] 시행 7 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8241e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 1.37876297567896e-07: T_c 2279.763692 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 5.2101e-08",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 7.664807485374681e-08: T_c 2448.107831 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 2.6116e-07",
"  [고리] 시행 5 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8085e-07",
"  [고리] 시행 7 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 5.2532e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 2.989655145668735e-08: T_c 2838.573290 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 8.5519e-08",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1.4754126920202282e-08 · 1e-08: T_c 2948.239626 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 2.5793e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 7.40736913584783e-08 · 6.542002168208328e-07: T_c 3003.762874 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 6.7998e-08",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 3.5316530877516075e-08 · 1.924528720609331e-07: T_c 3118.500655 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 6.3556e-10",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 7.280576228563263e-08: T_c 2448.107904 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 2.9956e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 8.657751915386314e-08: T_c 2448.107644 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.6184e-07",
"  [고리] 시행 5 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8086e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 4.280141725487852e-08: T_c 2530.454405 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.4934e-07",
"  [고리] 시행 8 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 6.6851e-07",
"  [고리] 시행 7 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8241e-07",
"  [고리] 시행 7 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8241e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 1.37876297567896e-07: T_c 2279.763692 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 5.2101e-08",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 7.664807485374681e-08: T_c 2448.107831 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 2.6116e-07",
"  [고리] 시행 5 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8085e-07",
"  [고리] 시행 7 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 5.2532e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 2.989655145668735e-08: T_c 2838.573290 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 8.5519e-08",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1.4754126920202282e-08 · 1e-08: T_c 2948.239626 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 2.5793e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 7.40736913584783e-08 · 6.542002168208328e-07: T_c 3003.762874 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 6.7998e-08",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 3.5316530877516075e-08 · 1.924528720609331e-07: T_c 3118.500655 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 6.3556e-10",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 7.280576228563263e-08: T_c 2448.107904 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 2.9956e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 8.657751915386314e-08: T_c 2448.107644 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.6184e-07",
"  [고리] 시행 5 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.8086e-07",
"  [C152 메모 6] 뜀 — 괄호 끝 허용 1e-08 · 4.280141725487852e-08: T_c 2530.454405 K 에서 SHOOT_TOL 로, 통과 14 로 다시",
"  [고리] 시행 1 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 1.4934e-07",
"  [고리] 시행 8 걸음 · 완화 걸린 걸음 0 · 마지막 어긋남 6.6851e-07",
"Mars (planet)",
"  선언된 입력 22 · 도출값 180 · 범위 밖 4",
"      body_class               class=rocky, classes=rocky, decided_by=radius valley, agrees_with_declared=True",
"      cmb_heat_flux            q_cmb=cannot-say (경계층 δ_b 82235 km ≥ 맨틀 1694 k, q_cmb_min=cannot-say (경계층 δ_b 82235 km ≥ 맨틀 1694 k, q_cmb_max=cannot-say (경계층 δ_b 82235 km ≥ 맨틀 1694 k, cmb_boundary_layer=cannot-say (경계층 δ_b 82235 km ≥ 맨틀 1694 k, cmb_heat_flux_density=cannot-say (경계층 δ_b 82235 km ≥ 맨틀 1694 k, eta_bottom=1.471e+28 Pa s, q_adiabat=9.022e+11 W, q_adiabat_min=5.413e+11 W, q_adiabat_max=1.263e+12 W, adiabat_gradient_cmb=-0.4993 K/km, g_cmb=3.165 m/s2, k_core=50 W/(m K), cmb_jump=40.34 K, cmb_flux_verdict=cannot-say (경계층 δ_b 82235 km ≥ 맨틀 1694 k, q_cmb_in_paper_range=cannot-say (경계층 δ_b 82235 km ≥ 맨틀 1694 k",
"      core_energy_balance      core_cmb_temperature_solved=3383 K, core_cmb_temperature_solved_min=3354 K, core_cmb_temperature_solved_max=3904 K, core_cmb_temperature_declared=2000 K, core_cmb_solved_minus_declared=1383 K, q_cmb_solved=1.635e+11 W, q_s=1.515e+11 W, q_l=0 W, q_g=0 W, q_r=1.2e+10 W, icb_radius_solved=0 km, icb_pressure_solved=0 GPa, c_r_km_per_k=0 km/K, has_inner_core=False, core_profile_mass_residual=-0.1778, core_center_pressure_solved=31.87 GPa, balance_residual=-1.12e-15, band_corners_with_root=4",
"      core_entropy_production  entropy_production=-1.108e+07 W/K, entropy_production_min=-2.158e+07 W/K, entropy_production_max=4.47e+07 W/K, entropy_production_h0=-1.044e+07 W/K, e_r=-6.394e+05 W/K, e_s=1.584e+07 W/K, e_l=0 W/K, e_g=0 W/K, e_h=0 W/K, e_k=2.627e+07 W/K, entropy_positive_present=False, entropy_band_straddles_zero=True, entropy_corners_positive=5, inner_core_branch_taken=False, entropy_integration_width=1.102e+05 W/K",
"      core_state               core_gamma_cmb=2.873 dimensionless, core_gamma_material=2.873 dimensionless, core_gamma_fallback=1, core_gamma_verdict=composition-substitute, core_gamma_density_path=phase-mismatch, core_gamma_partial_repair=1, core_gamma_center=1.5 dimensionless, core_gamma_verdict_center=graded-disagreement, core_gamma_split=1, conductor_phase=liquid, cmb_melt_temperature=1781 K, center_melt_temperature=2051 K, core_cmb_temperature_used=2000 K, core_center_temperature_used=2188 K, icb_pressure=0 GPa, center_margin=137.8 K, cmb_margin=218.6 K, center_margin_fraction=0.0672 dimensionless, gamma_flip=0.4165 dimensionless, gamma_flip_in_alfe_range=False, k0_flip=None, melt_splice_disagreement=None, margin_condition=comfortable",
"    · core_thermal_history     cannot-say (구조 표가 낡았다 — 방아쇠 ['declared.basal_layer_density', 'declared.b",
"      dynamo_rocky             dipole_moment=0 M_earth, b_eq=0 uT, b_pol=0 uT, regime=dead (stagnant lid, declared), ladder_regime=5, dynamo_alive=dead (stagnant lid, declared), dipole_moment_min=None, dipole_moment_max=None, b_eq_multipolar_min=None, b_eq_multipolar_max=None",
"      heat_transport_mode      mode=not decided by flux, total_surface_flux=0.0132 W/m2, regime_candidates=['episodic lid', 'plutonic-squishy lid',, regime_flux_cannot_decide=['heat pipe (a stagnant-lid sub-case)', , regime_excluded=[], lid_regime=stagnant, lid_regime_source=declared, lid_regime_why=declared tectonic_regime «stagnant» (C15, lid_heat_pipe_ratio=0.1962, lid_q_sl_max=0.06729 W/m2, lid_mu_crit=0.04548, lid_korenaga=R4 not run — no `lid_friction` (μ) decla",
"      interior_layers          nmoi=0.3628 dimensionless, core_temperature=2531 K, cmb_temperature=1960 K, cmb_temperature_core=1960 K, cmb_temperature_mantle=1960 K, cmb_pressure=20.53 GPa, ice_column_state=none, silicate_melt_state=solid, silicate_melt_fraction_max=0, basal_silicate_state=solid, basal_layer_thickness_solved_km=150 km, core_plus_layer_radius_solved_km=1846 km, ocean_thickness=0 km, ice_shell_thickness=0 km, core_radius_fraction=0.5003 dimensionless, core_radius=0.2662 R_earth, crust_thickness=0 km, radius=0.532 R_earth, core_pressure=39.31 GPa, bulk_porosity=0 dimensionless, voids_expected=False, integrator_core_gamma_verdict=composition-substitute, integrator_red_gamma_used=0, fe_prem_dt_min=None, fe_prem_dt_max=None, fe_prem_dt_beyond_steps=None, fe_prem_thermal_grade=None, fe_prem_thermal_source=None, fe_prem_thermal_counter_evidence_searched=None, silicate_thermal_pressure=None, silicate_thermal_pressure_steps=None, silicate_thermal_pressure_gap_min=None, silicate_thermal_pressure_grade=None, silicate_thermal_pressure_source=None, silicate_thermal_pressure_counter_evidence_searched=None, converged=True, unconverged_solvers=[], bracket_invalid=[], substituted_solvers=[], fallback_solvers=[], trial_unconverged=[], trial_bracket_invalid=[], finish_subst_from_tc=None, finish_subst_to_tc=None, finish_subst_delta_tc=None, finish_subst_y=None, core_mass_fraction=0.2127 dimensionless, ice_mass_fraction=0 dimensionless, core_sulphur_wt=0.1478 dimensionless, figure_relaxation=cannot-say (temperature belongs to anoth, maxwell_time_mantle_top=None, relaxation_threshold_max=None, composition=inferred",
"      internal_heat_nontidal   l_int=1.906e+12 W, t_int=21.97 K, radiogenic_power=1.906e+12 W, mantle_radiogenic_power=1.334e+12 W, crust_radiogenic_power=5.718e+11 W, radiogenic_power_low=None, radiogenic_concentration_grade=literature, radiogenic_concentration_default=False, radiogenic_heat_w_m2=0.0132 W/m2, radiogenic_power_history_4gyr=4.26 dimensionless, mantle_top_boundary_layer=81.15 km, implied_surface_heat_flux=0.05566 W/m2, implied_surface_heat_flow=8.036e+12 W, heat_flow_consistency=declaration-implies-more-heat-than-secul, urey_ratio=0.2372 dimensionless, mantle_temperature_floor_min=1019 K, mantle_temperature_floor_max=1358 K, mantle_temperature_floor_verdict=band (radiogenic-only floor on the mantl, mantle_temperature_width_zeta=281.6 K, mantle_temperature_width_set=0 K, mantle_temperature_width_denominator=105.5 K, mantle_temperature_width_surface=44.93 K, l_int_total=None, t_int_total=None, mantle_temperature_floor_total_min=None, mantle_temperature_floor_total_max=None, mantle_temperature_floor_total_verdict=cannot-say (no tidal_heating value — tot",
"      mass_radius_relation     radius_mr_screen=0.5218 R_earth, density=4.167 g/cm3, composition_preset_used=1",
"    · tidal_heating            cannot-say (no orbit): semi_major_axis, perturber_mass, eccentricity_for",
"    · tidal_locking            no semi_major_axis_km, perturber_mass_earth — the despin formula needs a",
"    · tidal_response           this body declares no tidal_response block, so the node does not run — a",
"",
"  계산 노드 35 중 — 값 냄 10 · 범위 밖 4 · 입력 부족 1 · 레시피 없음 20",
"",
"  이미 출하된 값과 대조",
"    [어긋남] core_radius_fraction 엔진    0.5003 · 보드   0.5398   (7.3% / 허용 3%)",
"             출처: 1830 / 3390 km, 같은 표",
"    [일치] nmoi           엔진    0.3628 · 보드   0.3634   (0.2% / 허용 1%)",
"  [FAIL] run.py bodies/mars.yaml (출하값 대조) — 비0 종료 (이 단계가 fail=1 을 세웠다)",
"  [TIME] run.py bodies/mars.yaml (출하값 대조) — 22:36:23 → 23:13:07 · 2204 s · RSS 106 MB",
"  [COST] run.py bodies/mars.yaml (출하값 대조) — user 1760.68 · sys 442.15 · invcsw 35787 · pf 0 · pr 44223760 · instr 18468214446521 · cycles 8104729290257 · blkin 0 · blkout 0"
]
}''')
SG = "structure_grid.py --check"
TS = "test_structure_grid.py"
NINE = ["declared.basal_layer_density", "declared.basal_layer_thickness_km", "declared.core_light_elements",
        "declared.mantle_composition", "bytes.chain.yaml", "bytes.reference_adiabats.json", "chain_reads",
        "sulphur_fixings", "mantle_table"]
HOLD = {"id": "SG-MARS-HOLD-ENGINE", "kind": "table_triggers", "steps": [SG, TS], "table": "mars.json", "triggers": NINE}
C59 = {"id": "C59", "step": "run.py bodies/mars.yaml (출하값 대조)", "mismatch_keys": ["core_radius_fraction"],
       "values": {"core_radius_fraction": [0.5002, 0.5398]}}


def _with(blocks, table=(C59, HOLD)):
    return ld.expected_red_only(log(*blocks), list(table))


def _edit(block, a, b):
    out = [l.replace(a, b) for l in block]
    assert out != block, a
    return out


def test_hold_p1_pc_gate_of_record_accepted():
    ok, notes = _with([PC_BLOCKS[SG], PC_BLOCKS[TS], PC_BLOCKS[C59["step"]]])
    assert ok, notes
    assert any("SG-MARS-HOLD-ENGINE 만 있음" in n for n in notes) and any("C59 만 있음" in n for n in notes)


def test_hold_p2_test_structure_grid_alone_accepted():
    ok, notes = _with([PC_BLOCKS[TS]])
    assert ok, notes


def test_hold_p3_c59_only_with_the_row_present():
    ok, notes = _with([PC_BLOCKS[C59["step"]]])
    assert ok, notes


def test_hold_n1_tenth_trigger_rejected():
    assert not _with([_edit(PC_BLOCKS[SG], "'mantle_table']", "'mantle_table', 'code.interior.py']")])[0]


def test_hold_n2_eight_trigger_subset_rejected():
    assert not _with([_edit(PC_BLOCKS[TS], ", 'mantle_table']", "]")])[0]


def test_hold_n3_extra_fail_in_a_range_rejected():
    b = list(PC_BLOCKS[SG])
    b.insert(1, "  [FAIL] venus.json — 재검 차 2e-3 > ε")
    assert not _with([b])[0]


def test_hold_n4_other_table_rejected():
    assert not _with([_edit(PC_BLOCKS[SG], "[FAIL] mars.json", "[FAIL] earth.json")])[0]


def test_hold_n5_form_bound_to_its_step():
    form1 = next(l for l in PC_BLOCKS[SG] if "데이터 방아쇠" in l)
    b = [form1 if "방아쇠 그대로" in l else l for l in PC_BLOCKS[TS]]
    assert not _with([b])[0]


def test_hold_n6_exit_only_range_rejected():
    # r2 B1 (3b 8a2b9cf9): structure_grid.py --check dies with a traceback — no mars.json line, only the exit line
    b = [l for l in PC_BLOCKS[SG] if "데이터 방아쇠" not in l]
    assert b != PC_BLOCKS[SG] and any("비0 종료" in l for l in b)
    b.insert(1, "Traceback (most recent call last):")
    b.insert(2, "KeyError: 'mantle_table'")
    ok, notes = _with([b])
    assert not ok and any("종료 줄만" in n for n in notes), notes


def test_hold_row_in_the_file_matches_the_frozen_text():
    import yaml                                   # read the file itself: test_3 replaces _load_expected_red
    rows = yaml.safe_load(ld.EXPECTED_RED.read_text(encoding="utf-8"))
    row = next(r for r in rows if r["id"] == "SG-MARS-HOLD-ENGINE")
    assert {k: row[k] for k in HOLD} == {**HOLD, "triggers": row["triggers"]} and set(row["triggers"]) == set(NINE)
D = {"id": "SG-MARS-HOLD", "step": "derived 1-mars", "derived_entry": "1-mars", "triggers": ["x"]}
DS = "derived 1-mars"


def dbody(lines, fail=True):
    out = [f"[RED] 1-mars — stamp unchanged, but the table's own read rules fail: data triggers moved ['x']"] + lines
    if fail:
        out.append(f"  [FAIL] {DS} — 비0 종료 (이 단계가 fail=1 을 세웠다)")
    return out + [f"  [TIME] {DS} — 1 s", f"  [COST] {DS} — instr 1"]


def test_derived_expected_line_accepted():
    """sg-gate SG-MARS-HOLD: the derived step's red is accepted only with derived/check.py's EXPECTED RED line for its id."""
    ok, notes = ld.expected_red_only(log(dbody(["  1-mars: EXPECTED RED, gate_expected_red.yaml id SG-MARS-HOLD — r"])),
                                     T + [D])
    assert ok, notes


def test_derived_without_expected_line_rejected():
    assert not ld.expected_red_only(log(dbody([])), T + [D])[0]
    assert not ld.expected_red_only(log(dbody(["  1-mars: not the red gate_expected_red.yaml id SG-MARS-HOLD expects"])),
                                    T + [D])[0]
    # another id's EXPECTED line, or the line outside the step's range, does not count
    assert not ld.expected_red_only(log(dbody(["  1-mars: EXPECTED RED, gate_expected_red.yaml id C59 — r"])), T + [D])[0]
    assert not ld.expected_red_only(log(["  1-mars: EXPECTED RED, gate_expected_red.yaml id SG-MARS-HOLD — r",
                                         "  [COST] other — instr 1"], dbody([])), T + [D])[0]


def test_c59_row_still_read_beside_a_derived_row():
    """the C59 form is unchanged when the table also holds a derived row (no KeyError on mismatch_keys)."""
    assert ld.expected_red_only(log(body(M, [("nmoi", "0.3571", "0.3634")])), [D] + T)[0]


if __name__ == "__main__":   # pytest 없는 게이트 venv 에서도 돈다
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for n, f in tests:
        f()
        print(f"  [PASS] {n}")
    print(f"{len(tests)} 통과")
