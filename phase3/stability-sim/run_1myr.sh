#!/usr/bin/env bash
# Long-horizon (1 Myr) stability re-run for the stable systems, for higher
# long-term confidence. Records 3D positions (x,y,z) for the star-map viewer.
# alpha_centauri is intentionally EXCLUDED: its observed orbit goes unstable by
# ~50 kyr (planet ejects), so a 1 Myr run there is meaningless — keep its IAS15
# 50 kyr result. Run from the repo root:  bash phase3/stability-sim/run_1myr.sh
# Rough total ≈ 20 h (55 Cnc alone ≈ 8 h). Safe to leave overnight.
set -u
cd "$(dirname "$0")/../.."
PY=.venv/bin/python
RUN="$PY phase3/stability-sim/scripts/run.py --years 1000000"

# integrator per system = the one each was validated with
declare -a WHFAST=(55_cnc 61_vir hd_219134 hd_69830 proxima_cen tau_cet teegardens_star)
declare -a TRACE=(au_mic barnards_star trappist_1 yz_cet)

for s in "${WHFAST[@]}"; do
  echo "=== $s (whfast, 1 Myr) — $(date +%H:%M) ==="
  $RUN --system "$s" --integrator whfast
done
for s in "${TRACE[@]}"; do
  echo "=== $s (trace, 1 Myr) — $(date +%H:%M) ==="
  $RUN --system "$s" --integrator trace
done
echo "=== done — rebuild the viewer:  python3 scripts/viz/build_starmap.py ==="
