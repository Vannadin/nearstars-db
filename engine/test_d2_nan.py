# D2-nan 시험 — D2 줄 모듈(melt_exact · thermal_ale · hop_track)의 NaN 규칙: 자리마다 심은 NaN 은 이름 붙은 거절·None·0.0, 유한 쌍둥이는 고정값 그대로
"""Checks for D2-nan (artifacts d2nan-pkg-c8, pc/d2-nan-c8/plan.md rev 1 e1234269, cleared by 68 as 377a5faf).

N1–N9: each site gets a planted NaN, which must give the named refusal, None or 0.0 and never a sign, and a finite
twin, which must equal the value computed on the same machine with the three modules at engine/stageA-d2 0c05bb5a
(the fix leaves finite arithmetic as it was). An earlier revision froze Mac reprs, which the PC's libm missed by ~1e-12.
The already-guarded sites of plan §1 get one planted line each, so their guards stay pinned. The negative control
runs this file against 0c05bb5a's modules: every N line must be red there, every guarded line and twin green.

    python3 engine/test_d2_nan.py            (the checks)
    python3 engine/test_d2_nan.py --pins [--engine DIR]   (prints the finite twins' values, over DIR's modules)
"""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

#: --engine DIR imports the modules (and mars.yaml) from DIR instead of this file's directory: the --pins run over BASE
ENGINE = Path(sys.argv[sys.argv.index("--engine") + 1]) if "--engine" in sys.argv else Path(__file__).resolve().parent
sys.path.insert(0, str(ENGINE))
import fold_track as ft                # noqa: E402
import hop_track as hp                 # noqa: E402
import melt_exact                      # noqa: E402
import samuel_layer as lay             # noqa: E402
import samuel_model as sm              # noqa: E402
import samuel_structure as ss          # noqa: E402
import samuel_thermal as st            # noqa: E402
import thermal_ale as ta               # noqa: E402
import thermal_stack as ts             # noqa: E402

NAN = float("nan")
PINS_MODE = "--pins" in sys.argv
fails = 0
pins_out: dict = {}

#: The base the finite twins are compared against: this tree's own engine/ with only the D2-nan modules at
#: engine/stageA-d2 0c05bb5a, the commit before the fix. Its values are computed here, on this machine and
#: interpreter, by running this file in --pins mode over that copy, so the twin isolates the fix's diff: not two
#: machines' libm, and not later changes elsewhere in engine/ (which move both sides alike).
BASE = "0c05bb5ad17f2f908eb8b497537ea4e3d4948a63"
BASE_MODULES = ("melt_exact.py", "thermal_ale.py", "hop_track.py")


def base_pins() -> tuple[dict | None, str]:
    """(the twins' reprs over the BASE modules, "") or (None, why)."""
    here = Path(__file__).resolve()
    try:
        old = {m: subprocess.run(["git", "-C", str(here.parent), "show", f"{BASE}:engine/{m}"], capture_output=True,
                                 check=True).stdout for m in BASE_MODULES}
    except (OSError, subprocess.CalledProcessError) as e:
        return None, f"BASE {BASE[:8]}'s modules unreadable from git: {str(getattr(e, 'stderr', e))[:100]}"
    with tempfile.TemporaryDirectory() as d:
        eng = Path(d) / "engine"
        shutil.copytree(here.parent, eng, ignore=shutil.ignore_patterns("__pycache__"))
        for m, blob in old.items():
            (eng / m).write_bytes(blob)
        out = subprocess.run([sys.executable, "-B", str(here), "--pins", "--engine", str(eng)],
                             capture_output=True, text=True)
    if out.returncode != 0:
        return None, f"--pins over BASE rc {out.returncode}: {out.stderr.strip()[-100:]}"
    return json.loads(out.stdout[out.stdout.index("{"):]), ""


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def refuses(fn, site: str):
    """(True, message) when fn() raises sm.Refused naming `site`; (False, what happened) otherwise."""
    try:
        got = fn()
    except sm.Refused as e:
        return site in str(e), str(e)[:120]
    except Exception as e:                          # noqa: BLE001 — any other exception is not the named refusal
        return False, f"{type(e).__name__}: {str(e)[:100]}"
    return False, f"no refusal: returned {str(got)[:80]}"


def twin(key: str, value) -> None:
    """The finite twin: equal to BASE's value on this machine (repr), or recorded in --pins mode."""
    r = repr(value)
    if PINS_MODE:
        pins_out[key] = r
        return
    want = (PINS or {}).get(key)
    why = (f"no BASE value: {PINS_WHY}" if PINS is None else f"BASE has no {key!r}" if want is None
           else f"{r[:80]} · BASE {want[:80]}")
    check(f"{key} — finite twin equals 0c05bb5a", want == r, "" if want == r else why)


PINS, PINS_WHY = (None, "") if PINS_MODE else base_pins()
if not PINS_MODE:
    check("BASE 0c05bb5a's twins computed on this machine (--pins with its three modules)", PINS is not None, PINS_WHY)


ta.reset_stats()                       # the ALE mode's counters, as ta.run sets them
hp.reset_stats()
prof = ss.mars_profile(ENGINE / "bodies" / "mars.yaml")
G = prof.gravity(prof.radius_m)
LAYER = dict(d_d=st.D_D_M, k_d=4.0, lambda_d=14.373, fe_mean=96.97, fe_top=94.1306, nodes=41, melting=True)
STATE = (2158.1024424461625, 1815.5593199821958, 80e3, 20e3)
T_GYR, GRAD = 1.0, -0.02

s2 = ts.samuel_stack(lam=20.0, profile=prof, g=G)
s2.opt["melt_rule"] = "exact"
f0 = ts.state_terms(s2, *STATE, T_GYR, GRAD)
R_TOP = s2.r_p - STATE[2] - f0["delta_u"]
R_BOT = s2.r_base + f0["delta_b"]
D_REF = sm.crust_reference_thickness(s2.r_p, s2.r_c, s2.body["crust_reference_fraction"])
MKW = dict(d_cr=STATE[3], d_ref=D_REF, delta_t_sol=s2.body["delta_t_sol"],
           extraction_below_pa=s2.body["melt_extraction_below_pa"], shells=s2.opt["melt_shells"],
           curves=s2.body["curves"])
P_X = s2.body["melt_extraction_below_pa"]
import samuel_lid as sl                # noqa: E402
LID = sl.LidGrid(s2.lid.params["nodes"], r_p=s2.r_p, t_s=s2.body["t_surface"], rho_m=s2.mantle.params["rho"],
                 c_m=s2.mantle.params["cp"], k_m=s2.mantle.params["k"], rho_cr=s2.lid.params["rho_crust"],
                 c_cr=s2.lid.params["cp_crust"], k_cr=s2.lid.params["k_crust"])     # as thermal_ale._run builds it


def melt(t_m=STATE[1], t_b=f0["t_b"], pressure=s2.melt_p):
    return melt_exact.melt_integrals(t_m, t_b, R_TOP, R_BOT, pressure, **MKW)


# ── N1–N3: melt_exact ────────────────────────────────────────────────────────────────────────────────────────────
print("  N1–N3 melt_exact.melt_integrals")
twin("N1-N3 melt_integrals", melt())
check("N1–N3 setup — the extraction pressure lies inside the shell (a cut is bisected)",
      s2.melt_p(R_TOP) < P_X < s2.melt_p(R_BOT), f"P(top) {s2.melt_p(R_TOP):.4g} · P_x {P_X:.4g} · P(bot) {s2.melt_p(R_BOT):.4g}")
r_cut = R_BOT
lo_, hi_ = R_BOT, R_TOP
for _ in range(200):                                 # the radius of P_x on this profile (the cut the bisection finds)
    mid = 0.5 * (lo_ + hi_)
    lo_, hi_ = (mid, hi_) if s2.melt_p(mid) > P_X else (lo_, mid)
r_cut = 0.5 * (lo_ + hi_)


def p_nan_window(r):                                 # NaN within 1 m of the cut: only the bisection's late midpoints
    return NAN if abs(r - r_cut) < 1.0 else s2.melt_p(r)


if not PINS_MODE:
    ok, msg = refuses(lambda: melt(pressure=p_nan_window), "melt_exact.bisect_root")
    check("N1 — a NaN probe inside the cut bisection refuses by name (melt_exact.bisect_root)", ok, msg)
    ok, msg = refuses(lambda: melt(t_m=NAN), "melt_exact.add")
    check("N2 — a NaN temperature at a piece's ends refuses by name (melt_exact.add)", ok, msg)
    ok, msg = refuses(lambda: melt(pressure=lambda r: NAN if r == R_BOT else s2.melt_p(r)), "melt_exact.cuts")
    check("N3 — a NaN pressure at a shell end refuses by name (melt_exact.cuts)", ok, msg)


# ── N4: thermal_ale._radius_at ───────────────────────────────────────────────────────────────────────────────────
class StubP:
    """melt_p only: a linear pressure, NaN where `nan_at` says."""
    def __init__(self, nan_at=lambda r: False):
        self.nan_at = nan_at

    def melt_p(self, r):
        return NAN if self.nan_at(r) else (3.39e6 - r) * 1.3e4


print("  N4 thermal_ale._radius_at")
P4 = (3.39e6 - 2.7e6) * 1.3e4
twin("N4 _radius_at", ta._radius_at(StubP(), P4, 3.2e6, 2.0e6))
if not PINS_MODE:
    ok, msg = refuses(lambda: ta._radius_at(StubP(lambda r: r == 2.0e6), P4, 3.2e6, 2.0e6), "thermal_ale._radius_at")
    check("N4 — a NaN bracket end refuses by name, not «outside the shell» (None)", ok, msg)
    ok, msg = refuses(lambda: ta._radius_at(StubP(lambda r: abs(r - 2.7e6) < 1.0), P4, 3.2e6, 2.0e6),
                      "thermal_ale._radius_at")
    check("N4 — a NaN midpoint inside the bisection refuses by name", ok, msg)

# ── N5: thermal_ale.event_signs ──────────────────────────────────────────────────────────────────────────────────
print("  N5 thermal_ale.event_signs")
s2._ale_state = {"grad": GRAD, "tb": None, "th": None}
real_terms = ta.state_terms


def signs_with(override: dict, y=STATE):
    # the terms are the finite STATE's own (with `override`), so a NaN in y reaches event_signs' own check, not
    # state_terms' (which would refuse first, through melt_exact)
    ta.state_terms = lambda s, *a, **k: {**real_terms(s, *STATE, *a[4:], **k), **override}
    try:
        return ta.event_signs(s2, list(y), T_GYR, 1.0)
    finally:
        ta.state_terms = real_terms


twin("N5 event_signs", signs_with({}))
if not PINS_MODE:
    for key in ("stefan", "t_b", "delta_u", "delta_b"):
        ok, msg = refuses(lambda key=key: signs_with({key: NAN}), "thermal_ale.")
        check(f"N5 — a NaN {key} refuses by name, never a False sign", ok, msg)
    ok, msg = refuses(lambda: signs_with({}, y=(STATE[0], STATE[1], STATE[2], NAN)), "thermal_ale.event_signs")
    check("N5 — a NaN D_cr in the state refuses by name", ok, msg)

# ── N6: hop_track.hump_sign ──────────────────────────────────────────────────────────────────────────────────────
print("  N6 hop_track.hump_sign")
root = ft.Root(100.0, dx=1.0, lo=50.0, hi=150.0)
twin("N6 hump_sign", hp.hump_sign(lambda x: x - 110.0, root))
if not PINS_MODE:
    got = hp.hump_sign(lambda x: NAN, root)
    check("N6 — a NaN midpoint gives 0.0 («no hump»), not −1.0", got == 0.0, repr(got))
    lost = hp.lost(lambda x: x - 110.0, ft.Root(100.0, dx=1.0, lo=50.0, hi=150.0, g=0.0), "δ_b")
    check("N6 — lost() reads r.g = 0.0 as no fold (Lost(False))", lost.fold is False, repr(lost.fold))

# ── N7: thermal_ale.lid_coeffs ───────────────────────────────────────────────────────────────────────────────────
print("  N7 thermal_ale.lid_coeffs")
twin("N7 lid_coeffs", ta.lid_coeffs(LID, STATE[2], STATE[3], 1e-8, 5e-8))
if not PINS_MODE:
    ok, msg = refuses(lambda: ta.lid_coeffs(LID, STATE[2], NAN, 1e-8, 5e-8), "thermal_ale.lid_coeffs")
    check("N7 — a NaN D_cr refuses by name, not an all-crust lid", ok, msg)
    ok, msg = refuses(lambda: ta.lid_coeffs(LID, NAN, STATE[3], 1e-8, 5e-8), "thermal_ale.lid_coeffs")
    check("N7 — a NaN D_l refuses by name", ok, msg)

# ── N8: thermal_ale._basal_solve ─────────────────────────────────────────────────────────────────────────────────
print("  N8 thermal_ale._basal_solve")
s4 = ts.samuel_stack(lam=10.0, profile=prof, g=G, model="bml", layer=LAYER)
ts.state_terms(s4, *STATE, T_GYR, GRAD)            # the basal grid starts inside the first state_terms
lg = s4.layer_grid
t_mid = [0.5 * (a + b) for a, b in zip(lg.t_sol, lg.t_liq)]           # inside the melting interval: φ is live
rhs = ta._basal_energy(lg, t_mid, ta._basal_phi(lg, t_mid))
B_ARGS = (lg, rhs, 1e12, t_mid[0], t_mid[-1], t_mid)
check("N8 setup — the plate 4 basal grid melts (latent set)", lg.latent is not None, repr(lg.latent))
twin("N8 _basal_solve", ta._basal_solve(*B_ARGS))
if not PINS_MODE:
    real_tri = lay._solve_tridiagonal

    def tri_nan(*a, **k):                            # a NaN at the second interior node, not the first difference
        x = real_tri(*a, **k)
        x[2] = NAN
        return x
    lay._solve_tridiagonal = tri_nan
    try:
        ok, msg = refuses(lambda: ta._basal_solve(*B_ARGS), "thermal_ale._basal_solve")
    finally:
        lay._solve_tridiagonal = real_tri
    check("N8 — a NaN node after the solve refuses by name, never «converged»", ok, msg)

# ── N9: thermal_ale._run's step over τ ───────────────────────────────────────────────────────────────────────────
print("  N9 thermal_ale._run step")
if not PINS_MODE:
    s9 = ts.samuel_stack(lam=20.0, profile=prof, g=G)
    s9.body["age_gyr"] = s9.body["t_initial_gyr"] + 0.002
    real_tau = ta._tau_s
    ta._tau_s = lambda y, f: NAN
    try:
        out9 = ta.run(s9, 5.0)
    finally:
        ta._tau_s = real_tau
    check("N9 — a NaN τ refuses by name, never a step at cap", "thermal_ale._run.tau" in str(out9.get("refused")),
          str(out9.get("refused"))[:120])

# ── already guarded (plan §1): one planted line each ─────────────────────────────────────────────────────────────
if not PINS_MODE:
    print("  guarded sites (no change)")
    check("hop_track.bisect — a NaN probe returns None (nan_safe)",
          hp.bisect(lambda x: NAN if x > 0.4 else x - 0.7, 0.0, 1.0, -0.7) is None)
    check("hop_track.changes_sign — a NaN end is no sign change", not hp.changes_sign(NAN, 1.0)
          and not hp.changes_sign(-1.0, NAN))
    check("hop_track.checked — a NaN residual refuses the root (None)", hp.checked(lambda x: NAN, 1.0) is None)
    lo2 = hp.lost(lambda x: NAN, ft.Root(100.0, dx=1.0, lo=50.0, hi=150.0, g=1.0), "δ_b")
    check("hop_track.lost — a NaN on the hump is no fold (Lost(False))", lo2.fold is False, repr(lo2.fold))
    real_ls = ta._lid_solve
    ta._lid_solve = lambda *a, **k: [NAN] * LID.n
    try:
        f_lid = {**f0, "ddl": 1e-9, "lid_gradient": GRAD}
        try:
            ta._lid_stage(s2, LID, [0.0] * LID.n, 1.0, list(STATE), T_GYR, f_lid)
            lid_ok, lid_msg = False, "no Lost"
        except ft.Lost as e:
            lid_ok, lid_msg = e.equation == "Ḋ_l" and e.fold is False, f"Lost({e.equation}, {e.fold})"
    finally:
        ta._lid_solve = real_ls
    check("thermal_ale._lid_stage — a NaN secant never converges: Lost(«Ḋ_l», False)", lid_ok, lid_msg)
    print("  (hop_track.switch_branch's residual — `not (abs(fu) <= EPS …)` refuses on NaN — needs a fold state; not "
          "planted here, read in plan §1)")

if PINS_MODE:
    print(json.dumps(pins_out, indent=1, sort_keys=True))
    sys.exit(0)
print(f"test_d2_nan — {'all passed' if fails == 0 else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
