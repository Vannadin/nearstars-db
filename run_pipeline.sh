#!/usr/bin/env bash
# NearStars 데이터 파이프라인 실행 스크립트

set -e
cd "$(dirname "$0")"

SCRIPTS=scripts/pipeline

echo "=== NearStars Pipeline ==="

# fetch 단계 (순서 무관)
echo "[1/6] fetch_astrometry.py"
python3 $SCRIPTS/fetch_astrometry.py

echo "[2/6] fetch_photometry.py"
python3 $SCRIPTS/fetch_photometry.py

echo "[3/6] fetch_stellar_props.py"
python3 $SCRIPTS/fetch_stellar_props.py

echo "[4/6] fetch_planets.py"
python3 $SCRIPTS/fetch_planets.py

# 조립
echo "[5/6] build_systems.py"
python3 $SCRIPTS/build_systems.py

echo "[6/6] validate.py"
python3 $SCRIPTS/validate.py

# 사이트 빌드
python3 $SCRIPTS/build_site.py

echo ""
echo "=== 완료 ==="
