# Body-Tree Spec — Sun-rooted, stars as direct children

> Status: **SPEC** (owner-approved 2026-07-18, s25 proposal R6/M-F). Records the
> de-facto shape the pipeline already emits; new emitters and Principia-side code
> may rely on it.

**The spec.** The NearStars body tree is **single-rooted at the stock `Sun`**, with
every star (or barycenter standing in for a close binary) a **direct child of
`Sun`** (`referenceBody = Sun`); planets/moons/disks parent to their star or
barycenter as usual. Interstellar space is therefore, in stock terms, the Sun's
SOI. Each star carries a **stock Keplerian placeholder orbit** around Sun — a
representational slot so KSP/Kopernicus can build the tree, never a physical
claim — while the **real state is Principia-Cartesian** (`principia_initial_state`
per body); under Principia management the placeholder and stock SOI mechanics in
the void are irrelevant. Stock SOI/orbit semantics matter only in the windows
where a vessel is *released* from Principia management — chiefly the WS4 warp
cruise, whose re-adoption step ("set the destination stock orbit around the
destination star") assumes exactly this single-rooted tree with stars as stock
bodies.

**Grounding (verified 2026-07-18):**

- Emitter: `.claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py` emits
  `referenceBody = Sun` for every star Body node (line ~857).
- Live test config: `test-configs/ws5-principia-probe/GameData/NearStars-Configs/`
  (`NearStars-Stars-Kopernicus.cfg` + `NearStars-StockKeplerian-Orbits.cfg`) —
  the configs the in-game WS5/WS5-C gates ran on.
- This is also the standard Kopernicus interstellar-pack shape, so third-party
  tooling expectations match.

**Out of scope here:** the warp watchdog (timing/ownership still an open owner
call, deferred to a separate discussion — not decided by this spec).
