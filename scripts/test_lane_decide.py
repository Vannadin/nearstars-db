# auto-lane 기대 빨강 인정 규칙(C128)의 합성 로그 자기 시험 다섯
import sys, pathlib
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
    ld._load_expected_red = lambda: T
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


def test_no_cost_line_rejected():
    assert not run(log([f"    [어긋남] nmoi 엔진 0.3571 · 보드 0.3634", f"  [FAIL] {M} — 비0 종료 (이 단계가 fail=1 을 세웠다)"]))


if __name__ == "__main__":   # pytest 없는 게이트 venv 에서도 돈다
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for n, f in tests:
        f()
        print(f"  [PASS] {n}")
    print(f"{len(tests)} 통과")
