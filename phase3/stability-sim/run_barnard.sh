#!/bin/bash
# 비행 중 오프라인용: Barnard's Star TRACE 200 kyr 안정성 적분 + 뷰어 재빌드.
# 버나드는 카오스계(MEGNO~16, Hill-stable)이고 행성이 빽빽해 근접조우 처리가 필요 →
# TRACE 사용. 1 Myr는 ~18시간이라 1/5(20만 년, ≈3-4시간)만. 인터넷 불필요.
# 사용: bash phase3/stability-sim/run_barnard.sh
ROOT="/Users/vana/Desktop/NearStars"
PY="$ROOT/.venv/bin/python"
CSV="$ROOT/phase3/stability-sim/results/barnards_star_timeseries.csv"
LOG="$ROOT/phase3/stability-sim/run_barnard.log"
cd "$ROOT" || exit 1
{
  echo "=== Barnard TRACE 200 kyr — start/resume $(date '+%Y-%m-%d %H:%M') ==="
  # resumable: checkpoints each snapshot to barnard_ckpt.bin. Interrupt (Ctrl-C /
  # sleep) and re-run this same command to continue from where it stopped.
  caffeinate -i "$PY" phase3/stability-sim/run_barnard_resume.py
  echo "=== sim exit ($(date '+%H:%M')); checking completion ==="
  if tail -1 "$CSV" | grep -q '^200000'; then
     echo "reached 1 Myr — rebuilding viewer"
     "$PY" scripts/viz/build_starmap.py | tail -2
     echo "=== DONE $(date '+%H:%M'). 온라인 되면:"
     echo "    git add phase3/stability-sim/results/barnards_star_* docs/starmap.html && \\"
     echo "    git commit -m 'feat(stability): Barnard 1 Myr (WHFast)' && git push"
  else
     echo "!! 1 Myr 미도달(중단/실패) — 뷰어 재빌드 안 함. 나중에 다시 실행."
  fi
} 2>&1 | tee "$LOG"
