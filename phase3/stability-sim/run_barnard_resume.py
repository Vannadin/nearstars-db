# 재개 가능한 Barnard's Star 안정성 적분 (REBOUND SimulationArchive 체크포인트).
# 매 스냅샷마다 상태를 barnard_ckpt.bin 에 저장 + CSV 증분 기록 → 중단(Ctrl-C/슬립)
# 후 같은 명령을 다시 실행하면 멈춘 지점부터 이어감. 인터넷 불필요.
import sys, os, math, csv, json
HERE = os.path.dirname(os.path.abspath(__file__))          # phase3/stability-sim
sys.path.insert(0, os.path.join(HERE, "scripts"))
import rebound                                             # noqa: E402
import run as R                                            # run.py (main-guarded → import-safe)

RES = os.path.join(HERE, "results")
ARCHIVE = os.path.join(RES, "barnard_ckpt.bin")
CSV = os.path.join(RES, "barnards_star_timeseries.csv")
HEADER = ["t_yr", "body", "a_au", "e", "inc_deg", "Omega_deg", "omega_deg", "f_deg"]
T_END = float(os.environ.get("BARNARD_YEARS", "200000"))   # 1/5 of 1 Myr
N = int(os.environ.get("BARNARD_SNAPS", "200"))
DT_SNAP = T_END / N
times = [T_END * (i + 1) / N for i in range(N)]

_, meta = R.build("barnards_star", None)                   # names/primary
star_name = meta["star"]["name"]
planets = [p["name"] for p in meta["planets"]]


def elements(sim):
    star = sim.particles[star_name]
    rows = []
    for nm in planets:
        o = sim.particles[nm].orbit(primary=star)
        rows.append([nm, o.a, o.e, math.degrees(o.inc), math.degrees(o.Omega),
                     math.degrees(o.omega), math.degrees(o.f)])
    return rows


if os.path.exists(ARCHIVE):                                # ── resume ──
    sim = rebound.Simulation(ARCHIVE)                      # last saved snapshot
    done = int(round(sim.t / DT_SNAP))
    if os.path.exists(CSV):                                # drop any rows past the checkpoint
        with open(CSV) as f:
            rr = list(csv.reader(f))
        body = [r for r in rr[1:] if r and float(r[0]) <= sim.t + 1e-6]
        with open(CSV, "w", newline="") as f:
            w = csv.writer(f); w.writerow(HEADER); w.writerows(body)
    print(f"[resume] t={sim.t:.0f} yr  ({done}/{N} snapshots done)", flush=True)
else:                                                      # ── fresh ──
    sim, meta = R.build("barnards_star", None)
    R.configure_integrator(sim, meta, "trace")
    sim.dt /= float(os.environ.get("BARNARD_DT_DIV", "1"))   # 1/4 step test: does the ~300 kyr ejection survive a finer dt?
    with open(CSV, "w", newline="") as f:
        csv.writer(f).writerow(HEADER)
    sim.save_to_file(ARCHIVE)
    done = 0
    print(f"[fresh] TRACE, dt={sim.dt*365.25:.4f} d, {N} snapshots to {T_END:.0f} yr", flush=True)

with open(CSV, "a", newline="") as f:                      # ── integrate remaining, checkpoint each ──
    w = csv.writer(f)
    for k in range(done, N):
        sim.integrate(times[k], exact_finish_time=0)
        for nm, a, e, inc, Om, om, fa in elements(sim):
            w.writerow([times[k], nm, a, e, round(inc, 5), round(Om, 5), round(om, 5), round(fa, 5)])
        f.flush()
        sim.save_to_file(ARCHIVE)                          # checkpoint (resume point)
        if k % 10 == 0 or k == N - 1:
            print(f"  {times[k]:.0f} yr ({k+1}/{N})", flush=True)

# ── finalize: minimal summary from the CSV (viewer reads the CSV, not this) ──
per = {}
with open(CSV) as f:
    for r in csv.DictReader(f):
        b = per.setdefault(r["body"], {"a_min": math.inf, "a_max": -math.inf,
                                       "e_min": math.inf, "e_max": -math.inf})
        a, e = float(r["a_au"]), float(r["e"])
        b["a_min"] = min(b["a_min"], a); b["a_max"] = max(b["a_max"], a)
        b["e_min"] = min(b["e_min"], e); b["e_max"] = max(b["e_max"], e)
json.dump({"system": "Barnard's Star", "integrator": "trace", "t_end_yr": T_END,
           "n_snapshots": N, "per_body": per,
           "note": "resumable TRACE run (run_barnard_resume.py); MEGNO n/a for TRACE"},
          open(os.path.join(RES, "barnards_star_summary.json"), "w"), indent=2)
print(f"COMPLETE: reached {T_END:.0f} yr ({N} snapshots).", flush=True)
