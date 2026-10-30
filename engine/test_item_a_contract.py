# item A 자유 풀이 수렴 계약 시험 — R 의 행(P6 · P9 실측 꼴과 심은 꼴), 접힘 쪽 R · 이른 멈춤, 닫기의 동결 순서 틈(post-freeze note 1), 심은 뜀, 자리마다 변형이 빨갛게 서는지, K4 꼬리표
"""python -B test_item_a_contract.py   (cwd = engine/)

Registration: pc/ea-e18/item-a-prereg.frozen.md (rev 3) with post-freeze note 1 (narrow to x resolution before R; the
answer is the bracket point with the smallest |y|; K3 a reported pin on p_c and T_c). Fakes stand in for the shots; no
integration runs here. FOLD_CONTINUATION is off in the loop cases, so a jump ends as the C152 jump refusal.
"""
from __future__ import annotations

import contextlib
import io
import math
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import eos  # noqa: E402
import interior  # noqa: E402
import rootfind  # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


R = interior._root_evidence
L = math.log

# ① R's rows (frozen §5 A5, directing 1; exact values from p6.json 091f3524 and p9-k100.json fc7fb49c)
XA, ULP = 8.010599562958676, 2.0 ** -49
check("R-a — P6 1730.0: lower branch −6.8307e-5 at xa, +2^25 47-sample +1.2686e-5, +2^24 interior 0.0671: no root (s₂ sign)",
      R(XA, -6.830670127657755e-05, XA + 2 ** 24 * ULP, 0.06714929452531766, XA + 2 ** 25 * ULP, 1.2685986694179635e-05)
      is None)


def _line(x1, y1, x2, y2, x):
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)


xl, xh = L(3012.721554170), L(3012.724353827)
ym = _line(L(3012.718754515), -6.938e-5, xl, -6.250e-5, 0.5 * (xl + xh))
check("R-b — P9 k=100 final rerun bracket (−6.250e-5, +0.06715), interior on the lower branch's line: no root",
      R(xl, -6.250e-5, 0.5 * (xl + xh), ym, xh, 0.06715) is None)
xl2, xh2 = L(3013.024488790), L(3013.025995303)
ym2 = _line(L(3013.017748208), -3.039e-4, xl2, -1.891e-4, 0.5 * (xl2 + xh2))
check("R-b twin — the STEPS-doubled bracket (92/94 samples, −1.891e-4, +0.06717): no root",
      R(xl2, -1.891e-4, 0.5 * (xl2 + xh2), ym2, xh2, 0.06717) is None)
check("R-c — a smooth root (a planted n_rock step across it does not enter R): lin",
      R(-1e-6, -2e-6, 0.0, 0.0 + 1e-9, 1e-6, 2.000000002e-6) == "lin")
check("R-d — a jump with one n_rock throughout: no root", R(-1e-6, -1e-5, 0.0, -1e-5 + 1e-12, 1e-6, 0.05) is None)
check("R-e — a same-sign jump inside a straddling bracket (rev 2 B1's shape): no root",
      R(-1e-6, -1e-5, 0.0, 0.06, 1e-6, 1e-5) is None)
check("R-res — three values at the shot's resolution: res", R(-1e-15, -5e-8, 0.0, 1e-8, 1e-15, 6e-8) == "res")

# ② fold side: refined crossings, R and K3 there, the early stop (r2 N2 on rev 3), mutants fold · locate
def _walk(g_of, outside=None):
    def F(u, v):
        if abs(u) > 1.0 or (outside is not None and outside(u)):
            raise rootfind.FoldOutside
        return v, g_of(u)                              # the curve dm = 0 is v = 0
    return rootfind.fold_walk(F, (-0.5, 0.0), 1e-12, direction=-1.0, refine=interior._contract("locate"))


def _real(g_of, outside=None):
    return interior._fold_real(_walk(g_of, outside))


g_smooth = lambda u: u - 0.3                            # a true crossing at u = 0.3
g_jump = lambda u: -1e-4 if u < 0.3 else 0.05           # a g jump on the walk: its near edge is |g| 1e-4 < T_SURFACE_TOL
check("fold — a smooth crossing is kept (refined, R, K3)", len(_real(g_smooth)) == 1)
check("R-f — a g jump on the walk is not a crossing", len(_real(g_jump)) == 0)
check("fold — an early stop (FoldOutside inside the θ bracket) is «not refined», not a crossing",
      len(_real(g_smooth, outside=lambda u: 0.29 < u < 0.31)) == 0)
g_curved = lambda u: math.expm1(2.0 * (u - 0.3)) + 1e-17   # a root Illinois cannot land on exactly (it lands g = 1e-17)
check("fold — a curved crossing is kept", len(_real(g_curved)) == 1)
for site, g_of, want_on in (("fold", g_jump, 0), ("locate", g_curved, 1)):
    on = len(_real(g_of))
    interior.CONTRACT_SITES_OFF.add(site)
    try:
        off = len(_real(g_of))
    finally:
        interior.CONTRACT_SITES_OFF.discard(site)
    check(f"mutant {site} — restoring today's {('filter' if site == 'fold' else 'Illinois locate')} goes red", on == want_on and off != on,
          f"on {on} · off {off}")

# ③ the frozen order's gap (post-freeze note 1): directly on _close_bracket with fake shots
def _fake_st(t_c, t_surf, p=1e11):
    return types.SimpleNamespace(t_surface=t_surf, p_center=p, rock_samples=(), radius_m=6.4e6, mass_kg=6e24,
                                 floor_truncated=None, p_cmb=None, hot_water_filled=None, crust_blocked=False,
                                 surface_reached=True, ice_samples=(), t_center=t_c, boiling_flips=None)


def _close(y_of, xl, xh, order_off):
    shoot_at = lambda x, hint: (_fake_st(math.exp(x), math.exp(y_of(x))), y_of(x))
    if order_off:
        interior.CONTRACT_SITES_OFF.add("order")
    try:
        return interior._close_bracket(shoot_at, xl, y_of(xl), _fake_st(0, 0), xh, y_of(xh), _fake_st(0, 0))
    finally:
        interior.CONTRACT_SITES_OFF.discard("order")


x0 = L(2100.0)
y_exact = lambda x: 1.8 * (x - x0)                      # «exact»: a smooth root, p_c flat, so K3's pin is 0 from the start
note_e, froz_e = _close(y_exact, x0 - 0.02, x0 + 0.03, False), _close(y_exact, x0 - 0.02, x0 + 0.03, True)
check("note 1 «exact» — narrowed to x resolution, the answer is at the root", note_e[0] and abs(note_e[1]["x"] - x0) < 1e-12,
      str(note_e[1].get("x", note_e)) if note_e[0] else str(note_e))
check("note 1 «exact» control — the frozen order stops on the pin and answers off the root (red under the frozen order)",
      froz_e[0] and abs(froz_e[1]["x"] - x0) > 1e-3, str(froz_e[1]["x"] - x0) if froz_e[0] else str(froz_e))
xj = L(1500.0)
y_wall = lambda x: 0.5 * (x - xj) - 4e-4 if x < xj else 0.01   # «wall met»: a jump with p_c flat across it, no root
note_w, froz_w = _close(y_wall, xj - 0.15, xj + 0.05, False), _close(y_wall, xj - 0.15, xj + 0.05, True)
check("note 1 «wall met» — narrowed to x resolution, R finds no root", not note_w[0], str(note_w)[:80])
check("note 1 «wall met» control — the frozen order accepts a non-root on the wide bracket (red under the frozen order)",
      froz_w[0], str(froz_w)[:80])
check("note 1 — the answer carries the p_c pin (K3), the T_c pin beside it, the shots and the noise used",
      note_e[0] and {"pin", "pin_tc", "shots", "noise"} <= set(note_e[1]))


# note 1 rev 2 (r2 B1, directing): the y resolution of a point is S·SHOOT_TOL; at Mars 1850 K interior.py documents S 147
def _close_s(y_of, xl, xh, s, p_of=None, off=()):
    def st_at(x):
        st = _fake_st(math.exp(x), math.exp(y_of(x)), 1e11 if p_of is None else p_of(x))
        st.shot_s = s
        return st
    shoot_at = lambda x, hint: (st_at(x), y_of(x))
    interior.CONTRACT_SITES_OFF.update(off)
    try:
        return interior._close_bracket(shoot_at, xl, y_of(xl), st_at(xl), xh, y_of(xh), st_at(xh))
    finally:
        interior.CONTRACT_SITES_OFF.difference_update(off)


x18 = L(3012.72)
S_MARS = 147.0
def wig(x):
    """Shot noise of amplitude S·SHOOT_TOL, uncorrelated from one x to the next (a hash of x, so no continuous zero)."""
    h = math.sin(x * 1.2345678e12) * 43758.5453
    return S_MARS * interior.SHOOT_TOL * (2.0 * (h - math.floor(h)) - 1.0)
y_noisy = lambda x: 0.9 * (x - x18) + wig(x)
roots = [x18 + k * 3.7e-7 for k in range(20)]               # 20 continuous roots under the same noise
n_on = [_close_s(lambda x, r=r: 0.9 * (x - r) + wig(x), r - 1e-4, r + 1e-4, S_MARS)[0] for r in roots]
n_off = [_close_s(lambda x, r=r: 0.9 * (x - r) + wig(x), r - 1e-4, r + 1e-4, S_MARS, off=("noise",))[0] for r in roots]
check("note 1 rev 2 — continuous roots under S 147 shot noise (Mars 1850 K) pass R, 20 of 20", all(n_on), f"{sum(n_on)}/20")
check("note 1 rev 2 control — under a fixed 1e-7 threshold most of the same roots fail R (red under rev 1)",
      sum(n_off) <= 10, f"{sum(n_off)}/20 pass")
y_njump = lambda x: (0.9 * (x - x18) - 4e-4 if x < x18 else 0.01) + wig(x)
check("note 1 rev 2 — a jump well above the S 147 noise still fails R",
      not _close_s(y_njump, x18 - 1e-4, x18 + 1e-4, S_MARS)[0])
p_steep = lambda x: 1e11 * math.exp(1e3 * (x - x18))                          # dlnp/dy ≈ 1100: the noise cannot pin p_c
k_on = _close_s(y_noisy, x18 - 1e-4, x18 + 1e-4, S_MARS, p_of=p_steep)
k_off = _close_s(y_noisy, x18 - 1e-4, x18 + 1e-4, S_MARS, p_of=p_steep, off=("pin",))
check("K3 gate (A4, frozen) — a close whose p_c pin exceeds band/10 is not an answer", not k_on[0] and k_on[4] == "pin",
      str(k_on)[:100])
check("K3 gate control — with the gate off the same close answers", k_off[0], str(k_off)[:80])

# ④ the loop: a planted jump; FLAG off ends at L2 with an answer, FLAG on refuses with the jump refusal (the fold's trigger)
T_POT = 1000.0


def run(y_of, ok_of=None, wall=None, passes=None, tst=None, ttol=None):
    real = interior._shoot_pressure
    saved = (interior.T_PASSES, interior.T_SURFACE_TOL, interior.T_TOL, interior.FOLD_CONTINUATION)

    def fake(*a, t_center=None, t_pot=None, p_hint=None, tol=None, **k):
        if wall is not None and t_center > wall:
            raise eos.PhaseGap("fake", 1e9, "벽", temperature_k=t_center, too_cold=False)
        return _fake_st(t_center, T_POT * math.exp(y_of(t_center, tol))), (True if ok_of is None else ok_of(t_center, tol))
    interior._shoot_pressure, interior.FOLD_CONTINUATION = fake, False
    if passes:
        interior.T_PASSES = passes
    if tst:
        interior.T_SURFACE_TOL = tst
    if ttol:
        interior.T_TOL = ttol
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            st, ok = interior.shoot(6e24, 0.3, 0.0, "fe_prem", potential_temperature=T_POT)
        return ("A", round(st.t_center, 5), bool(ok), getattr(st, "contract_exit", None))
    except (ValueError, eos.PhaseGap) as e:
        return ("R", str(e)[:28])
    finally:
        interior._shoot_pressure = real
        interior.T_PASSES, interior.T_SURFACE_TOL, interior.T_TOL, interior.FOLD_CONTINUATION = saved


SC = {
    "smooth a0.3 r1500": dict(y_of=lambda t, tol: 0.3 * math.log(t / 1500.0)),
    "smooth a0.9 r1500": dict(y_of=lambda t, tol: 0.9 * math.log(t / 1500.0)),
    "smooth a3 r1500": dict(y_of=lambda t, tol: 3.0 * math.log(t / 1500.0)),
    "jump e1e-4": dict(y_of=lambda t, tol: 0.9 * math.log(t / 1700.0) * 1e-3 + (-1e-4 if t < 1700.0 else 0.05)),
    "jump e9e-4": dict(y_of=lambda t, tol: 0.9 * math.log(t / 1700.0) * 1e-3 + (-9e-4 if t < 1700.0 else 0.05)),
    "jump e1e-4 steep": dict(y_of=lambda t, tol: 0.9 * math.log(t / 1700.0) + (-1e-4 if t < 1700.0 else 0.05)),
    "jump e9e-4 steep": dict(y_of=lambda t, tol: 0.9 * math.log(t / 1700.0) + (-9e-4 if t < 1700.0 else 0.05)),
    "wall": dict(y_of=lambda t, tol: 0.5 * math.log(t / 1500.0) - 0.0004, wall=1499.0),
    "memo3": dict(y_of=lambda t, tol: 0.9 * math.log(t / 1650.0),
                  ok_of=lambda t, tol: not (tol <= interior.SHOOT_TOL and t < 1670.0), tst=5e-2, ttol=3e-2),
    "exact": dict(y_of=lambda t, tol: 1.8 * math.log(t / 2100.0)),
    "okwin": dict(y_of=lambda t, tol: 0.3 * math.log(t / 1650.0), ok_of=lambda t, tol: not abs(t - 1650.0) < 2.0),
    "short budget": dict(y_of=lambda t, tol: 0.3 * math.log(t / 1650.0), passes=5),
    "short budget wiggle": dict(y_of=lambda t, tol: 0.3 * math.log(t / 1650.0) + 0.002 * math.sin(0.37 * t), passes=5),
    "plateau": dict(y_of=lambda t, tol: 0.02 * math.log(t / 1650.0) + 1e-5 * math.sin(t)),
}
interior.FREE_SOLVE_CONTRACT = False
off_j = run(**SC["jump e1e-4"])
interior.FREE_SOLVE_CONTRACT = True
on_j = run(**SC["jump e1e-4"])
check("planted jump — FLAG off answers on the jump's edge (today's E1 · L2)", off_j[0] == "A", str(off_j))
check("planted jump — FLAG on refuses with «잔차가 뛴다» (the fold's trigger)", on_j[0] == "R" and "잔차가 뛴다" in on_j[1], str(on_j))

# ⑤ one mutant per site (frozen A5): restoring that one site's ecb355d7 behaviour changes the outcome on its scenario
MUT = {"order": "exact", "L2": "jump e9e-4", "L4": "jump e1e-4", "L9": "smooth a3 r1500", "L10": "smooth a0.9 r1500",
       "L11": "smooth a0.3 r1500", "P1": "okwin", "P2": "okwin", "P3": "short budget", "P4": "wall",
       "P5": "short budget wiggle", "P6": "plateau", "P11": "memo3", "R": "jump e1e-4 steep", "handon": "smooth a0.3 r1500"}
for site, sc in MUT.items():
    interior.CONTRACT_SITES_OFF.clear()
    on = run(**SC[sc])
    interior.CONTRACT_SITES_OFF.add(site)
    try:
        off = run(**SC[sc])
    finally:
        interior.CONTRACT_SITES_OFF.clear()
    check(f"mutant {site} — red on «{sc}»", off != on, f"on {on} · off {off}")

# ⑥ K4: every answer of the scenarios with the FLAG on names a closed exit
answers = [(k, run(**v)) for k, v in SC.items()]
bad = [(k, o) for k, o in answers if o[0] == "A" and o[2] and o[3] not in ("brent", "step", "fold", "no-thermal")]
check("K4 — every converged answer names brent, step, fold or no-thermal", not bad, str(bad)[:160])
check("A1 — the mutant switch is empty after the tests", not interior.CONTRACT_SITES_OFF)

# ⑦ fix line «closure by id» (found while coding, directing 10-30): a tagged structure that is freed must not let a later
#   structure with the same id read as closed. The record holds the structure itself, and closure is read from the
#   structure's own attribute. Under the first draft (record {id: info}, closure = «id in record») this check is red: CPython
#   reuses a freed object's id at once for a new object of the same size.
old_hits = new_hits = 0
for _ in range(100):
    old = {}                                       # the first draft's record: {id: info}, closure = «id in record»
    a = _fake_st(1.0, 1.0)
    old[id(a)] = {"exit": "brent"}
    del a
    b = _fake_st(2.0, 2.0)
    old_hits += id(b) in old
    interior.CONTRACT_EXITS.clear()
    a = _fake_st(1.0, 1.0)
    interior._contract_tag(a, {"exit": "brent"})
    del a
    b = _fake_st(2.0, 2.0)
    new_hits += getattr(b, "contract_exit", None) is not None or (id(b) in interior.CONTRACT_EXITS
                                                                  and interior.CONTRACT_EXITS[id(b)][0] is not b)
check("fix «closure by id» — control: the first draft's id-keyed record reads a fresh structure as closed", old_hits > 0,
      f"{old_hits} of 100")
check("fix «closure by id» — the fixed record never does", new_hits == 0, f"{new_hits} of 100")
interior.CONTRACT_EXITS.clear()
interior._FAMILY_TRAIL.pop("exits", None)

print(f"  test_item_a_contract — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
