#!/usr/bin/env bash
# NearStars 데이터 파이프라인 실행 스크립트

set -e
cd "$(dirname "$0")"

SCRIPTS=scripts/pipeline

echo "=== NearStars Pipeline ==="

# fetch 단계 (순서 무관)
echo "[1/8] fetch_astrometry.py"
python3 $SCRIPTS/fetch_astrometry.py

echo "[2/8] fetch_photometry.py"
python3 $SCRIPTS/fetch_photometry.py

echo "[3/8] fetch_stellar_props.py"
python3 $SCRIPTS/fetch_stellar_props.py

echo "[4/8] fetch_planets.py"
python3 $SCRIPTS/fetch_planets.py

echo "[5/8] fetch_stellarium_ids.py"
# 신규/null 컴포넌트만 쿼리 (모두 매핑되어 있으면 즉시 종료, idempotent).
# 노쿠아 또는 SIMBAD 가 다운돼도 null 만 남기고 빌드는 계속 진행.
python3 $SCRIPTS/fetch_stellarium_ids.py || echo "  ⚠ stellarium id 조회 실패 — 빌드는 계속"

# 조립
echo "[6/8] build_systems.py"
python3 $SCRIPTS/build_systems.py

echo "[7/8] validate.py"
python3 $SCRIPTS/validate.py

# 사이트 빌드
echo "[8/8] build_site.py"
python3 $SCRIPTS/build_site.py

echo ""
echo "=== 완료 ==="
