# Context notes — floor-backfill

Append-only. Started 2026-07-20.

## 2026-07-20 — program start

- Scope is the owner's: **all curated hosts ≤50 ly**, not roster-only.
- **Tiering was the useful move.** The raw "129 hosts below floor" reads as one
  huge program; the actual distribution is bimodal — 11 hosts need 1–2
  determinations (Tier A/B) while 112 have never had a Phase-2 pass at all
  (Tier D, 5–6 categories each). Sequencing A→D means the roster and the
  already-used planet hosts stop being the weak link early, and the long tail
  becomes a batched background program instead of a blocker.
- Tier A is only 2 hosts (40 Eridani C: activity + rotation; Fomalhaut:
  rotation) — the roster was in better shape than the headline number implied.
- **Checked before assuming a curation gap**: Sirius B / Procyon B / Van
  Maanen's Star each hold mass + radius only, while the WD floor also wants
  teff + age. These are famous, well-measured white dwarfs, so this is a
  curation gap and not a measurement gap — worth stating because the opposite
  case (floor asking for something nobody has measured) is a real possibility
  elsewhere in the list and should be recorded as an honest N/A rather than
  chased forever.
- First batch delegated: WD trio (teff + cooling age), rotation trio (Fomalhaut,
  40 Eri C, Delta Pavonis), age quintet (55 Cnc, GJ 9066, HD 219134, YZ Cet,
  eps Ind A). Agents research and return structured blocks; the main thread
  applies via `apply_phase2.py` and verifies.
- 40 Eri C carries prior history the agent was told to respect rather than
  rediscover blind: Shan 2024 P_rot 8.56 d was examined before and deliberately
  left uncurated as a quality-D value (it is nevertheless the input the stellar
  J₂ row uses, as a documented divergence). The agent was asked for a verdict on
  whether that exclusion still holds.
