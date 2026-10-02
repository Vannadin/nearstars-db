# CLAUDE.md

NearStars: a KSP star-system mod built from a curated nearby-stars database (`db/`, `phase2`–`phase4`, `scripts/pipeline/`) plus an interior-structure engine developed on `engine/*` branches by several parallel seats.
Full working conventions live in [`CONVENTIONS.md`](CONVENTIONS.md). Open the section you need when its topic comes up; don't read it whole at session start.

## Always on

- **Replies to the owner are Korean.** 존댓말 only in the directing seat (whatever its current address is); work, parallel and audit seats reply in 명사형/반말 with no pleasantries (owner decision 2026-09-19). Seat-to-seat and PC messages are English.
- **No closing colons in Korean.** Every Korean sentence ends with `.`, `?` or `!`, never `:` (colons are fine in code, labels and key-value pairs).
- **New source files start with a one-line Korean comment stating their role** (under any shebang or directive; skip config files). Agents read files selectively, so this header is their map.
- **`.md` is English source-of-truth.** Reader-facing docs (`docs/`, `plans/`, root `README.md`, `CONVENTIONS.md`) get a natural-Korean `ko/<same-path>` mirror in the same commit.
- **Git.** Commits are in English with identity `VaNnadin <vannadin00@gmail.com>`. One logical change per commit. Never `git add -A`. On engine work only the directing seat pushes.
- **Autonomy.** When a step doesn't need the owner, keep going and put status in the same message as the next action. Stop to ask only for owner-level decisions, or before deleting or overwriting content you didn't create. No break or pace suggestions.
- **Verify before "done".** If you touched code, run its tests (`./scripts/check.sh` for the DB/pipeline). Read the actual error line before fixing.

## Gotchas

- Curated DB JSON is never written with plain `json.dump`. Use `apply_phase2.py` or `schema.write_canonical` so indent and key order survive. `db/systems/*.json` is derived; don't hand-edit it.
- Python's `csv` writer defaults to CRLF. Pass `lineterminator='\n'` and cite file hashes only after commit.
- Multi-step work outside the engine's prereg flow: keep the task list and the decisions-with-reasons in files in the workspace (`checklist.md`, `context-notes.md`), not in scrollback. Compaction drops scrollback.
