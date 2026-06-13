#!/usr/bin/env bash
# Long-horizon (1 Myr) stability re-run for the stable systems — PARALLEL and
# RESUMABLE. Each system is independent (own bodies + own output file) and
# REBOUND is single-threaded per run, so we launch them concurrently (up to
# MAX) to use idle cores: wall-clock ≈ the slowest single system instead of the
# serial sum. Re-running skips any system already at 1 Myr, so it resumes across
# sessions. Records 3D positions for the viewer.
#   bash phase3/stability-sim/run_1myr.sh [MAX_CONCURRENT=6]
# alpha_centauri is EXCLUDED (its observed orbit ejects by ~50 kyr; its adopted
# stable orbit is already integrated to 1 Myr separately).
set -u
cd "$(dirname "$0")/../.."
PY=.venv/bin/python
MAX=${1:-6}
RES=phase3/stability-sim/results

done1myr(){ # exit 0 if this system's CSV already reaches 1 Myr
  local c="$RES/$1_timeseries.csv"
  [ -f "$c" ] && "$PY" -c "import csv,sys;sys.exit(0 if max(float(r['t_yr']) for r in csv.DictReader(open('$c')))>=999999 else 1)" 2>/dev/null
}
run_sys(){
  local s=$1 ig=$2
  if done1myr "$s"; then echo "skip $s (1 Myr already done)"; return; fi
  while [ "$(jobs -rp | wc -l)" -ge "$MAX" ]; do sleep 5; done
  echo "launch $s ($ig) — $(date +%H:%M)"
  "$PY" phase3/stability-sim/scripts/run.py --years 1000000 --system "$s" --integrator "$ig" \
    > "phase3/stability-sim/log_$s.log" 2>&1 &
}

# integrator per dynamical regime (see ALPHA_CEN_AB_DYNAMICS_STUDY / memory)
for s in 55_cnc 61_vir hd_219134 hd_69830 proxima_cen tau_cet teegardens_star; do run_sys "$s" whfast; done
for s in au_mic barnards_star trappist_1 yz_cet; do run_sys "$s" trace; done
wait
echo "ALL DONE — $(date +%H:%M).  rebuild: python3 scripts/viz/build_starmap.py"
