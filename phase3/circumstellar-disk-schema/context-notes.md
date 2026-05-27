# Circumstellar disk schema — context notes

Append-only decision log. Each entry timestamped + rationale.

## 2026-05-27 — Discovered stellar Phase 3 already exists; revised approach

User asked "행성의 경우 디스크 관련 내용도 추가" mid-design. Before that, user pointed out "이거 알파 센타우리는 항성인데 페이즈 3 했거든? 어케 했는지 봐봐."

**Initial wrong assumption:** Phase 3 only had planet-level synthesis (`docs/phase3/<planet>.md`). I proposed three options for adding stellar disk synthesis — new directory, new yaml schema, or extension of system.yaml.

**Correction after reading `docs/phase3/alpha-centauri-a.md`:** Stellar Phase 3 pattern already exists. 287 lines, identical 8-section structure (Intro / Decisions / Surface / Atmosphere / Rotation & spin / Visual styling / Bibliography / Open items / Related). Korean mirror `ko/docs/phase3/alpha-centauri-a.md` matches block-for-block. HTML build + mirror check + reports index all flow through the same pipeline.

**Implication:**

- No new directory needed (`docs/phase3/<slug>.md` flat is the convention)
- No new schema file (extend `synthesis-template.md`)
- α Cen A is the structural template for stellar Phase 3 (alongside TRAPPIST-1 e/f for planetary)
- α Cen A's Decisions table uses stellar-specific fields (`spectral_type`, `mass_msun`, `radius_rsun`, `teff_k`, `metallicity_fe_h_dex`, `age_gyr`, `activity_log_rhk`, `x_ray_log_lx_cgs_min/max`, `limb_darkening_alpha_h`, `visual_surface_tint_hex_primary`, `stellar_color_temp_k`, `visual_companion_event_*`) — these need formalizing in synthesis-template.md, but they already work in practice

## Decision: disk vs ring vocabulary

Three distinct fields-groups, all rendered via Kopernicus Ring node but attached to different parent bodies:

- **Circumstellar disk** = debris/dust disk around a star (Vega-like). Attaches to star body. Field prefix `disk_`.
- **Planetary ring** = ring around a planet (Saturn-like). Attaches to planet body. Field prefix `ring_`. Already loosely defined in `phase3/kopernicus-emit-workspace/context-notes.md` sidecar yaml; this work formalizes the same names in Phase 3 Decisions schema.
- **Circumplanetary disk** = young protoplanetary disk around a planet (PDS 70 c). Distinct kinematic context from ring; field prefix `circumplanetary_disk_`. Rare for NS targets (no PDS 70-class targets in shortlist) but cheap to add for future-proofing.

All three use the Kopernicus Ring node; `mod-grounded-fields.md` maps each group to that primitive.

## Decision: keep kopernicus-emit-workspace sidecar yaml in sync

`phase3/kopernicus-emit-workspace/context-notes.md` defines a sidecar yaml schema with `ring_present`, `ring_inner_au`, `ring_outer_au`, `ring_color_hex`. The Planetary ring field group in synthesis-template.md uses the **same field names**, so the future kopernicus-cfg emitter can read directly from Phase 3 Decisions without sidecar yaml indirection — or, if sidecar yaml is retained, it just mirrors Phase 3 field names. No name divergence; no translation layer.

## Decision: agent-team structure — 8 parallel sub-agents, one per star

User clarified: "별마다 에이전트 배정해서 하란 소리였는데." Direct 1:1 mapping — 8 stars, 8 sub-agents, fired simultaneously in one dispatch message.

Initial proposal of batched parallelism (Vega pilot + 3-parallel batches) was rejected. User's "효율" intent treats all-at-once as the correct read; the wall-clock gain from concurrent execution outweighs the costs of arXiv rate-limit stall + token-cost spike + main-session post-receipt queue.

**Concurrency cost analysis:**

- arXiv 3 s rate per IP: 8 concurrent `build_bibliography.py` calls will serialize at the rate-limit layer; not fatal, adds a few minutes to bib stage.
- Token cost: ~15–30 paper deep-reads × 8 stars = up to ~240 fetched papers across the 8 sub-agent contexts. User has accepted 10–20 h budget; concurrent execution compresses this into a shorter wall-clock window without changing total token consumption materially.
- Post-receipt: 8 sub-agents will return roughly together. Main session processes them serially (Step 10 VERIFY → Korean mirror → HTML → commit), ~30 min × 8 = ~4 h serialized tail.

**What stays with main session (not delegated):**

- Korean mirror writing — per `feedback-ko-mirror-style`, sub-agents would produce literal translation
- Step 10 VERIFY — paper-by-row re-check matters too much to delegate to the same agent that drafted the row
- HTML build + mirror check + commit — atomic per-star, race-free if main is the single writer

## Decision: per-star workspace per CLAUDE.md §7

Each of 8 stars gets its own `phase3/<star>/` workspace with `system.yaml` + light `checklist.md` + `context-notes.md`. Following the established pattern in `phase3/trappist_1/`, `phase3/alpha_centauri_proxima/`, etc.

This workspace (`phase3/circumstellar-disk-schema/`) is the meta-workspace tracking schema changes + cross-star coordination. The per-star synthesis workspaces are siblings of this one, not children.

The 8 per-star workspaces are created by main session during Stage 2 pre-flight (before sub-agent dispatch), populated by sub-agents during their work (each sub-agent has read-write access to its star's workspace), and finalized by main session post-receipt.

## Risk register

| Risk | Why it matters | Mitigation in plan |
|---|---|---|
| Phase 2 `disk_measurements` missing | SKILL.md Step 1 requires Phase 2 done first; skipping degrades synthesis to Phase 1-grade for disk fields | Pre-flight check before each star; escalate via `nearstars-add-star` if absent (Stage 2 pre-flight step) |
| α Cen A Decisions silent break | If I add a Required field that A doesn't have, A's mirror/HTML breaks | Mark all disk + ring fields as "include only if `*_present=true`"; validation gate runs `check_block_parity.py alpha-centauri-a` before commit |
| τ Cet has 5 planets → much larger workload than other stars | Sub-agent budget assumes ~1–2 h per star; τ Cet needs planet-by-planet synthesis as well as stellar | Treat τ Cet as system-scope; plan revision before Batch 3 |
| AU Mic already has planets b/c in DB; partial Phase 3 may exist | Don't overwrite. SKILL.md autonomy guard #1: Read before overwriting | Pre-flight check for existing Phase 3 markdown; if present, this work *adds* disk to the existing synthesis rather than replaces |
| Sub-agent variance in Step 10 VERIFY rigor | Each Decisions row must trace to a specific paper line. Sub-agent may shortcut | Step 10 VERIFY moved to main session post-receipt; main re-reads each Decisions row against cited paper before commit |

## Open items

- [ ] Schema must distinguish "young pre-main-sequence + protoplanetary disk" from "old debris-disk star." Both use Circumstellar disk fields, but morphology + dust temp + lifetime narrative differ. Solution: `disk_morphology` prose field captures the qualitative distinction; Open-items + Surface synthesis cover the age context.
- [ ] After Vega pilot, evaluate whether `disk_resolved_imaging` should be split into multiple booleans (one per band) or remain a single bool with a multi-observatory prose field. Defer decision to post-Vega review.
- [ ] Stellar Phase 3 has implicit per-paper bibliography pattern (α Cen A's bib block); compare to planetary pattern. May need to surface differences in `synthesis-template.md` bibliography section.

## Related

- [plan](plan.md)
- [checklist](checklist.md)
- [nearstars-phase3 SKILL](../../.claude/skills/nearstars-phase3/SKILL.md)
- [kopernicus-emit-workspace context](../kopernicus-emit-workspace/context-notes.md) — sidecar yaml ring fields stay in sync
