# R3 — SOI cutoff numerical/physics correctness

리서치 에이전트: opus. 소스 head 440310a9 + numerical-methods 문헌.

## 0. Two reframing facts (change the whole risk calculus)
1. **QT12는 symplectic이 아니라 symmetric linear multistep 방법입니다** (`integrators/methods.hpp:1041` `struct QuinlanTremaine1990Order12 : SymmetricLinearMultistep`; 적분은 symplectic RKN 경로가 아니라 `symmetric_linear_multistep_integrator_body.hpp`가 담당합니다). no-drift 보장은 symplecticity가 아니라 **time-reversibility** (force = f(q) only) + 대칭 계수에서 나옵니다. Principia의 "conjugate-symplectic"은 backward-error 해석상 symplectic처럼 거동한다는 뜻이지만, 실제로 하중을 받치는 성질은 reversibility + f의 매끄러움입니다. **cutoff는 (a) reversibility [위치만의 힘]와 (b) order-12 오차 상수가 전제하는 smoothness를 모두 보존해야 합니다. cutoff가 (a)를 지키면서도 (b)를 파괴할 수 있습니다.**
2. **적분 경로는 두 개이며 one-way로 결합되어 있습니다**: massive backbone (fixed-step QT12, O(N²), 대칭 dual update `ephemeris_body.hpp:1372-1378`, 운동량 보존) — 수십 개 천체, 저렴합니다. massless 선박 (adaptive `FlowWithAdaptiveStep` `ephemeris.hpp:64`, one-way `:1415+`, backbone으로의 피드백 없음) — 비용은 선박당·substep당 항성 수에 비례합니다. **실질적인 이득은 vessel 경로에 있고, 실질적인 위험은 backbone에 있습니다.**

## 1. Hard-zero energy damage
절단된 potential Φ̃ = −μ/r (r<r_c), 0 (r>r_c)은 r_c에서 높이 **μ/r_c = a_c·r_c**의 계단을 갖습니다. 매 crossing마다 |ΔH̃| = μ/r_c가 방향에 따른 부호로 주입됩니다. backward-error 해석은 매끄러운 f를 요구하는데, 불연속면에서는 무효가 됩니다(껍질에서 방법의 order가 없습니다). M번 crossing → 에너지 **random walk** √M·μ/r_c = secular drift, QT12가 막기 위해 존재하는 바로 그 병리입니다. crossing당 점프를 QT12의 유계 ~1e-12…1e-14 진동과 비교하면, r_c=100·a_sma로 잡아도 계단이 ~2e-2 (2%) — 8~12자릿수 더 클 뿐 아니라 종류도 틀렸습니다(진동이 아니라 drift). **hard zero는 backbone / 속박 궤도에 대해 실격입니다.**

## 2. Softening
- (i) Hard cutoff: reversible이지만 C⁻¹, 오차 한계 무효. 기각합니다.
- (ii) POTENTIAL에 대한 **C¹/C² smooth taper**: Φ̃(r)=Φ(r)·S(r), S=1 for r≤r₀, 0 for r≥r_c. Quintic C² switch `S(x)=1−10x³+15x⁴−6x⁵`, x=(r−r₀)/(r_c−r₀). Φ̃는 진짜 위치만의 함수이므로 **reversibility + time-symmetry가 정확히 보존되고, 매끄러운 backward-error Hamiltonian이 성립하여 no-drift가 복원됩니다** (수정된 시스템에 대해). compact support이므로 r_c 바깥은 정확히 0이고, 따라서 진짜로 force-free coasting이 됩니다(오너의 "keep only inertia" 의도를 깔끔하게 달성합니다). 잔차 = 정적인 모델링 bias (실제 tail의 절단)이지 drift가 아닙니다. 비용은 껍질 구간에서 몇 flops 수준입니다.
- (iii) **Verlet neighbor list + skin**: 직교하는 최적화입니다(어떤 pair를 계산할지의 문제이지, potential 자체가 아닙니다). (ii)와 짝지어 씁니다. skin+hysteresis(r_c에서 추가, r_c+δ에서 제거)가 membership chatter를 없앱니다.
순위는 taper > list+skin (중립, 속도) > hard cutoff (최악)입니다. **(ii)⊕(iii)을 권고합니다.**

## 3. Is the property even needed here?
- **Backbone은 절대적으로 보호해야 합니다.** drift는 모든 행성 궤도를 오염시킵니다. cutoff의 이득은 ~0입니다(N_celestial이 수십 개). hard-zero는 절대 금지이며, 광년 떨어진 시스템끼리 decoupling할 때만 터무니없이 먼 곳에 smooth taper를 배치합니다.
- **Vessel/coast에서는 거의 문제되지 않습니다.** one-way 결합(오차가 전염되지 않음)이고, 경로가 이미 adaptive이며(애초에 no-drift 주장이 없음), interstellar tail은 실제로 무시할 만합니다(0.5 ly에서 a_local ~1e-12 m/s²). 우려는 "눈에 보이는 kink/속도 glitch가 없을 것"으로 축소되며, taper가 이를 처리합니다.

## 4. Cutoff placement (principled)
"Hill-sphere 배수"를 1차 기준으로 삼는 것은 기각합니다(Hill은 위성 안정성 기준이지, 힘의 무시가능성 기준이 아닙니다). **규칙: 무시되는 a_cut이 해당 지점에서 적분기 자체의 error floor보다 작아지는 곳에 r₀를 둡니다.**
- Backbone (fixed h, order p=12): tail ≤ a_local·C(ωh)^p ⇒ r_c가 매우 멀리 밀려남 ⇒ 사실상 속박 시스템 내부에서는 절대 truncate하지 않고, 항성계 블록 사이(round-off 이하)에서만 ⇒ **block-diagonal force matrix**. 블록 내부는 full N²입니다.
- Vessel: a_cut/a_dominant = 10⁻k, **k ≥ 6** (ppm tail)인 곳에 r₀를 두거나, tail이 adaptive abs-tolerance보다 작아지는 곳. + skin δ≈0.05–0.1·r_c + hysteresis.

## 5. Recommendation (concrete)
**reversible backbone에 먹이는 어떤 곳에도 hard zero는 없습니다. skinned neighbor list를 통한 smooth compactly-supported potential taper를 씁니다.**
- **A. Vessel path (primary, low risk)**: 선박별 neighbor list(몇 스텝마다 rebuild), 껍질 구간 천체에 대해 potential에 C² quintic switch, r_c 바깥은 정확히 0. r₀는 a_cut/a_dominant=1e-6 지점에 둡니다. 깨끗한 coasting과 지배적인 속도 향상을 ~0에 가까운 위험으로 제공합니다.
- **B. Backbone (secondary, careful)**: 각 속박 시스템 내부는 full N²; 시스템 간 inter-block 항은 0으로 taper (block-diagonal). **동일한 S(r)을 양쪽에 대칭으로 적용해** (`ephemeris_body.hpp:1372-1378`) 힘의 antisymmetry를 유지 ⇒ 운동량이 정확히 보존됩니다. 확신이 없으면 B는 건너뜁니다 — backbone은 병목이 아닙니다.
- **C. Non-negotiables**: POTENTIAL을 taper합니다(힘은 그로부터 유도하고, 힘을 독립적으로 truncate하지 않습니다 → 비보존적이 됩니다); backbone에서는 pair별 대칭; skin+hysteresis; **C² quintic이 최소 기준**; `physics/ephemeris_test.cpp` + `astronomy/ksp_system_test.cpp`/`ksp_resonance_test.cpp`로 **bounded, non-drifting** 에너지를 검증합니다(acceptance gate).

오너가 포기하는 것: 원거리 힘에 대한 ppm 수준의 정적 bias (물리적으로 무시 가능)입니다. 얻는 것: O(N·k) vessel scaling, block-diagonal backbone, force-free interstellar coasting — bounded-energy reversible 거동은 그대로 유지합니다. hard zero는 taper가 어차피 제공하는 속도 향상을 위해 그것을 내던지는 셈입니다.

## Grounding
QT12 symmetric-multistep `methods.hpp:1041`; symmetric backbone kernel `ephemeris_body.hpp:1347-1410` (dual :1372-1378); massless one-way `:1415+`; fixed vs adaptive `ephemeris.hpp:64`; Jool "stability" = setup patch `stabilize_ksp_body.hpp:33-44`. 문헌: Quinlan & Tremaine 1990; Hairer-Lubich-Wanner *Geometric Numerical Integration* ch. XV (symmetric, bounded energy) + ch. IX (backward error needs smooth f); Allen & Tildesley (switching functions, Verlet skin).
