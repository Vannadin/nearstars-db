<!-- 데이터가 어떻게 만들어지고 검증되는지(Phase 1~4 개요) -->
# Data & Methodology

Ask where any single number in NearStars comes from and there is always an answer. This repository is the mod's data engine, and its whole job is to turn published astronomy into validated, per-system data that the config writers (Kopernicus, Principia) can consume without anyone hand-tuning a value on a hunch. The rule the project holds itself to is `cfg = f(database, synthesis, art-direction)`: the game configs are a function of the data, never the other way around.

Getting from a raw catalog entry to an in-game world takes four phases, each building on the last.

## The four-phase pipeline

The first two phases gather facts; the third turns them into decisions; the fourth freezes the choices for the game.

| Phase | What it does | Output |
|---|---|---|
| **1: Catalog baseline** | Fetches astrometry, photometry, stellar properties, and exoplanet data from Gaia DR3, SIMBAD, NASA Exoplanet Archive, and ORB6 | `db/systems/*.json` (strictly derived, never hand-edited) |
| **2: Paper-cited curation** | Adds precise measurements from individual papers, each carrying its bibcode | curated DB layers |
| **3: Synthesis** | Derives cfg-ready values no single paper provides (surface tints, atmospheres, rotation states), decision by decision, each row re-verified against its cited paper | per-body synthesis reports with a machine-readable Decisions table |
| **4: Art direction** | The owner picks final in-game values, gated against the Phase 2/3 evidence window, and freezes each override | per-system boards |

Only after all four does the mod emit any config. That final step is deterministic and deliberately left until the end, once the data has stopped moving.

## The rules that keep it honest

Phase 3 is where a project like this can quietly go wrong, inventing a plausible-looking number and forgetting it was a guess. A handful of standing rules stop that from happening:

- **Provenance everywhere.** Every curated measurement names its paper, and papers are fetched and read through the ADS/arXiv pipeline so citations are checked against the actual text rather than from memory.
- **No silent defaults.** If a value has not been measured, it stays null in the database. Derived layers never fill the gap with an invented number.
- **Interesting-first, inside the window.** Where observations genuinely allow several readings, the mod picks the most visually or gameplay-distinctive one that the evidence still permits.
- **Documented divergence.** When the mod does depart from the canonical scientific reading, the report says so in a dedicated "Canonical alternatives" section, never buried in a footnote.
- **Gated fiction.** Bodies invented for variety pass a plausibility check against published constraints, stability simulations included, and stay flagged as fictional all the way into the game.

## How it is verified

None of this is taken on trust. Every data layer is schema-validated, with measurement methods whitelisted and provenance required before anything is accepted. Multi-planet and moon configurations are run through n-body stability simulations (REBOUND, with long-term integrations and MEGNO chaos indicators) to confirm the orbits actually hold. And a single repo-wide health check, `scripts/check.sh`, runs ten gates covering schema, English/Korean mirror sync, dead links, naming contracts, and pipeline-boundary consistency, so a regression in any of them fails loudly.

## Fully open working conventions

The openness extends past the data to the way it is produced. The project's entire working discipline lives in the repository: the behavioral guidelines ([CLAUDE.md](https://github.com/Vannadin/nearstars-db/blob/main/CLAUDE.md)), the full working conventions ([CONVENTIONS.md](https://github.com/Vannadin/nearstars-db/blob/main/CONVENTIONS.md)), the contributor guide with its document taxonomy ([AGENTS.md](https://github.com/Vannadin/nearstars-db/blob/main/AGENTS.md)), and even the config-writer skills themselves (`.claude/skills/`). Anyone can audit not just what the data says but how it came to say it.

## Browse it yourself

- [Live database viewer](https://vannadin.github.io/nearstars-db/) covers every system, filterable, with a 3D star map
- [Curation reports](https://vannadin.github.io/nearstars-db/reports.html) give the Phase 2/3 reports per body, with an English/Korean toggle
- [`docs/reference/`](https://github.com/Vannadin/nearstars-db/tree/main/docs/reference) holds the repository reference docs: methodology, the pipeline contract, and per-topic references
