# RP-1 / RSS integration — context notes

Decisions and reasoning, appended as work proceeds.

## 2026-06-26 — kickoff + grounding

- **Trigger.** Owner: "RP-1은 rss 기반이고, 알아서 잘 호환하게 만들어야 해." So
  RP-1 compat is now an active goal; RSS support (previously deferred in
  `guideline.md`) is pulled in-scope because RP-1 requires it.

- **Why classic RSS, not RSS-Reborn.** RP-1's required stack (its README) is
  RealismOverhaul + classic `KSP-RO/RealSolarSystem`. RSS-Reborn (our
  Sol-Configs lineage) is not in it. So we support classic RSS as a *second
  mutually-exclusive base*, not a swap.

- **The big simplifier.** Epoch (`JD2433282.5`), scale (1:1 real), root
  (`Sun`), and our ICRF Cartesian states are all base-independent. Verified:
  RSS+Principia's `solar_system_epoch` == our existing principia-cfg epoch.
  DB stores real distances (e.g. 5.95 pc → `icrs_x_km ≈ -3.18e13`), emitted
  uncompressed. ⇒ body physics is shared; only gating + career layers differ.

- **Principia constraint that bit us conceptually.** Once *any*
  `principia_initial_state` exists, it must cover *every* body. RSS+Principia
  already ships a full one ⇒ we cannot use the gravity-model-only Keplerian
  fallback (the IO-Extrasolar pattern). We must append full Cartesian states
  for all NearStars bodies. We have them.

- **ResearchBodies correction.** The earlier `rp1-compat.md` leaned on a
  Tracking-Station "observatory" mechanic. Grounded finding: RP-1 has **no
  observatory mechanic**; TS is comms/DSN. Discovery is part-based. Correct
  move = reseat RB telescope parts from the dead `spaceExploration` node to
  `scienceSatellite`, and ship `CC_RB_*` contracts `:NEEDS[!RP-0]`. The doc
  needs a rewrite (not yet done).

- **MM token gotcha.** RP-1's MM token is `RP-0` (hyphen-zero), not `RP-1`,
  despite the repo/folder rename. Gate on `:NEEDS[RP-0]`.

- **ROKerbalism tag gotcha.** Profile name is `RealismOverhaul`; the usable
  NEEDS tag is `ProfileRealismOverhaul` (Kerbalism's `Profile<Name>` rule) —
  not `ProfileRealism`/`ProfileRO`/`ROKerbalism`.

- **Emit posture.** Standing convention = emit deferred to project end
  (multiple memories). So this session captures conventions into skills + this
  plan; it does not write final cfgs. Stated to owner; awaiting confirm.

- **Unverified foundation.** No RSS-1:1 interstellar pack precedent exists
  (Extrasolar/Kcalbeloh are stock-scale; RSS Constellations/REX are abandoned
  on old KSP). The claim "NearStars bodies load on classic RSS" is inferred,
  not tested. Needs the owner's Windows install.

## 2026-06-26 — strategy pivot (owner steer)

- **Owner correction.** "RP-1은 Sol을 공식 지원 안 함. 반대로 솔 쪽에서 RP-1
  호환 가능하도록 작업을 계획하고 있긴 한데 — 기다리는 중." So RP-1 ⊥
  Sol-Configs officially, BUT ballisticfox/Sol-Configs is building its own RP-1
  compat (upstream, awaited).
- **Consequence — we do NOT build a classic-RSS branch.** NearStars stays
  Sol-based and rides on Sol-Configs' upcoming RP-1 bridge. The whole
  dual-base / RSS-coordinate-variant track (old WS1/WS2) is dropped.
- **Why we can still build now.** NearStars' RP-1 career patches gate on
  `RP-0` / `RealismOverhaul` / `ProfileRealismOverhaul` / `Principia` — never on
  the base-system tag. So Sol-Configs' bridge *mechanism* (whether it registers
  `RealSolarSystem`, how it does launch sites, etc.) is irrelevant to our
  patches. We author the career layers now; only final in-game validation waits
  on upstream.
- **Net remaining work** = ResearchBodies RP-1 patch (rewrite the stale
  rp1-compat.md), ROKerbalism RadiationBody nodes, Principia stays as-is (Sol),
  RealAntennas limitation doc. Emit still deferred to project end.

## 2026-06-26 — verification confirms pivot + scope locked

- **Mechanism (grounded).** MM tags come from loaded DLL assembly names, not
  cfg. Classic RSS ships `RealSolarSystem.dll` → registers `RealSolarSystem`,
  which RP-1/RO patches gate on. **Sol-Configs is config-only (no DLL)** →
  registers only `SolSystem` → RP-1/RO patches do not fire on it today. Sol
  V1.0 (ballisticfox Patreon 2025-05-29) declares "100% RP-1 compatible",
  replacing RSS — expected to provide the `RealSolarSystem` tag bridge itself.
  Body names (`Moon` internal) + launch sites (`us_cape_canaveral`) already
  align; the MM tag is the sole current blocker, and it's upstream's to fix.
- **Scope locked (owner).** Target = **RP-1 on Sol V1.0 only**. RP-1 on classic
  RealSolarSystem is explicitly out of scope — our `SolSystem`-gated bodies
  won't load there and we are NOT building a `:NEEDS[RealSolarSystem]` body
  branch. Consequence: NearStars is RP-1-compatible only once Sol V1.0 ships;
  today's classic-RSS RP-1 majority is not served. Conscious trade.
