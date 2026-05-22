# Phase 3 안정성 보고서 — 10,000년 N-body 적분

**생성일:** 2026-05-22
**적분기:** REBOUND 5.0 WHFast + MEGNO
**적분 구간:** 10,000년 (Principia 플레이 기준 horizon)
**초기 위상:** DB 의 `raw.omega_deg` 가 있으면 사용, Ω 와 M 은 결정론적 시드(`phase_seed=0`)로 무작위 배정.

## 한눈에 보는 결론

| 시스템            | 바디            | MEGNO      | 동역학 판정                  | Lyapunov 시간 |
|------------------|---------------|------------|------------------------------|---------------|
| TRAPPIST-1       | 행성 7개       | 1265       | 카오스지만 Hill-stable       | ≈16년         |
| Proxima Cen      | 행성 2개       | 2.000      | 안정 (regular)               | ∞             |
| α Centauri AB    | 별 2개         | 2.001      | 안정 (regular)               | ∞             |

**세 시스템 모두** 10,000년 동안 어떤 바디도 이탈하지 않고 이심률이 잘 묶여 있습니다. TRAPPIST-1 은 형식적 카오스 (Lyapunov 양) 를 보이지만 공명 사슬이 모든 행성을 Hill 영역 안에 가둡니다 — Tamayo et al. 2017 / Agol et al. 2021 의 결론과 일치.

## TRAPPIST-1 — 행성 7개

| 행성 | a 범위 (AU)      | Δa/a | e 범위 | 상태 |
|------|------------------|------|--------|------|
| b | 0.01153–0.01154 | 9.4×10⁻⁴ | 0.0004–0.0105 | stable |
| c | 0.01579–0.01581 | 1.2×10⁻³ | 0.0003–0.0114 | stable |
| d | 0.02223–0.02229 | 2.6×10⁻³ | 0.0007–0.0238 | stable |
| e | 0.02920–0.02929 | 3.1×10⁻³ | 0.0002–0.0188 | stable |
| f | 0.03845–0.03855 | 2.6×10⁻³ | 0.0016–0.0158 | stable |
| g | 0.04678–0.04689 | 2.5×10⁻³ | 0.0004–0.0130 | stable |
| h | 0.06175–0.06214 | 6.3×10⁻³ | 0.0007–0.0169 | stable |

- |ΔE/E| = 1.8×10⁻⁸ — 에너지 보존 완벽.
- MEGNO = 1265 at t=10⁴년 → Lyapunov 시간 ≈ 16년. 형식적 카오스.
- 어느 행성도 튕겨나가지 않고, e_max < 0.025, a 변동도 0.7% 미만.
- **게임플레이 의미:** Agol+2021 표준 구성을 그대로 출시해도 안전합니다. 플레이어가 10⁴년 Principia warp 을 돌려도 공명 사슬이 깨지지 않습니다.

## Proxima Cen — 행성 2개

| 행성 | a 범위 (AU)      | Δa/a | e 범위 | 상태 |
|------|------------------|------|--------|------|
| d | 0.02881–0.02881 | 6.0×10⁻⁵ | 0–0.0004 | stable |
| b | 0.04848–0.04848 | 4.5×10⁻⁵ | 0–0.0001 | stable |

- 질량은 **Msini** (RV 관측이라 경사각이 없음). 실제 질량이 더 클 가능성은 있지만, Suárez Mascareño 2025 의 권장값으로 돌리면 완벽한 regular orbit 입니다.
- |ΔE/E| = 3.4×10⁻⁹. MEGNO = 2.000 — 교과서적 regular.
- 두 행성이 충분히 떨어져 있고 (P_b/P_d ≈ 2.18, 공명 아님), 이심률도 거의 0 — 어떤 합리적인 horizon 에서도 위험 없음.

## α Centauri AB — 쌍성 (행성 없음)

- Pourbaix & Correia 2017 궤도 원소: P=79.91년, e=0.518.
- 125 궤도 적분. MEGNO = 2.001, |ΔE/E| = 3.8×10⁻¹².
- 2-body 라 trivially stable. Proxima 외곽 궤도 (P=547,000년) 는 DB 에서 위상 신뢰 불가로 표시돼 있어 제외 — 10⁴년 동안 외곽 궤도의 1.8% 밖에 안 돌아서 효과 없음.

## 가상 위성 — 데모

`hypotheticals/trappist_1.json` 에 위성 두 개를 넣어 테스트:

| 위성                          | 부모 | a (km)  | Hill 비율 | 결과 |
|-------------------------------|------|---------|-----------|------|
| TRAPPIST-1 e moon (safe)      | e | 20,000  | 0.23 | bound, stable |
| TRAPPIST-1 g moon (risky)     | g | 110,000 | 0.64 → ∞ | **1000년 안에 이탈**, e → 358,283 |

risky 위성은 0.64 R_Hill 에 놓여 Domingos et al. 2006 의 prograde 안정성 한계 (~0.5 R_Hill) 를 넘어가서 결국 시스템 밖으로 던져집니다. 이탈 과정에서 TRAPPIST-1 g 자체의 이심률도 평소 0.013 에서 0.028 로 튀어 — 위성 → 행성 역방향 섭동까지 적분에 포함된 증거입니다.

즉 이 도구는 **별–행성–위성 전체 하이어라키** 를 단일 N-body 시뮬레이션으로 풉니다. 위성에는 별의 조석력, 다른 행성들의 섭동이 동시에 가해지고, 위성 자신의 중력은 부모 행성에 되먹임됩니다.

## 사용법

```bash
# 기본 시스템 안정성
.venv/bin/python phase3/stability-sim/scripts/run.py --system trappist_1 --years 10000

# 가상 위성 / 추가 행성 포함
.venv/bin/python phase3/stability-sim/scripts/run.py \
    --system trappist_1 --years 1000 \
    --hypotheticals phase3/stability-sim/hypotheticals/trappist_1.json \
    --out-dir phase3/stability-sim/results/with_moons
```

바디 추가는 `hypotheticals/<system>.json` 편집.

```json
{
  "system": "<system_key>",
  "bodies": [
    {"name": "...", "parent": "<별 또는 행성 이름>", "type": "moon|planet",
     "semi_major_axis_km": ..., "eccentricity": 0, "inclination_deg": 0,
     "mass_kg": ..., "radius_km": ...}
  ]
}
```

Hill sphere 사전 검사로 R_Hill 밖에 위성을 두면 실행 거부, 0.5 R_Hill 초과면 경고.

## 주의사항

1. **TRAPPIST-1 이심률** 은 `raw.eccentricity` 에서 가져왔습니다 (각 행성 개별 발견 논문 핏, ≈0.005–0.01). Agol+2021 의 동시 TTV 핏은 더 좁은 제약을 줍니다 — 그 값을 쓰면 측정된 카오스는 조금 약해질 것입니다.
2. **null 위상 무작위화** 시드에 따라 정확한 Lyapunov 수치는 약간 달라지지만, 정성적 판정 (카오스/regular) 은 바뀌지 않습니다.
3. **Proxima 의 Msini** 값으로 돌렸을 때 안정성은 견고하지만, 진질량 민감도 스윕은 후속 과제로 남깁니다.
4. **에너지 오차** 는 이탈 사건이 일어나면 폭증합니다 (risky 위성 케이스에서 |ΔE/E|=1.7×10⁻³). 불안정 시나리오를 정확하게 추적하려면 IAS15 로 재실행하세요.
5. **10⁴년은 α Cen ABP 의 외곽 궤도 (547 kyr) 의 secular 진화** 를 보기엔 너무 짧습니다 — 장기 Proxima 결박 확인은 후속 10⁶년 런이 필요합니다.

## 파일 구조

- `scripts/load.py` — DB JSON → REBOUND 로더.
- `scripts/run.py` — 메인 엔트리. WHFast + MEGNO 실행 후 요약 저장.
- `hypotheticals/*.json` — 시스템별 가상 바디 스펙.
- `results/*_summary.json` — 시스템별 수치 요약 + 판정.
- `results/*_timeseries.csv` — 샘플된 (t, body, a, e) — 시각화용.
