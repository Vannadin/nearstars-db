# plans/ — Research notes

This directory holds **research notes**: one-off investigations that do
not (yet) produce changes to the DB pipeline, schema, or generated
configs in this repo.

If your work will touch code or data, you are in the wrong place. Use
`phase2/<topic>/` with the plan/checklist/context-notes trio instead.
See [AGENTS.md §2](../AGENTS.md#2-document-hierarchy) for the
decision rule.

---

## What belongs here

- Reading source code of an upstream mod (Principia, Kopernicus,
  Persistent Thrust, …) and writing up what you learned.
- Studying a published paper's methodology and recording findings.
- Scoping an idea that has not been greenlit for implementation.
- Comparing external data sources before deciding which to integrate.

## What does NOT belong here

- Active implementation work with a checklist → `phase2/<topic>/`
- Permanent reference documentation (schemas, methodology, format specs)
  → `docs/reference/`
- Plans that will produce code/data deltas in the next few sessions
  → `phase2/<topic>/`

---

## File conventions

1. **One file per topic.** `plans/<short_kebab_topic>.md`. No
   subdirectories.

2. **No checklist field in frontmatter.** Checklists imply implementation
   progress. Research notes are descriptive, not progress-tracked. If
   you find yourself wanting a checklist, you are actually doing
   implementation work — move to `phase2/<topic>/`.

3. **Repo-relative paths only.** No `/home/<user>/...` or `C:\...`. If
   you reference external code, link to its GitHub URL.

4. **State the NearStars connection in the first paragraph.** Why does
   this research matter for NearStars? Without this, the document
   cannot justify its place in the repo.

5. **Start from the template.** See [`_template.md`](_template.md).

---

## Lifecycle

A `plans/` document can be:

- **Active** — being read or extended in the current cycle.
- **Promoted** — its findings have moved to a permanent home, either
  `phase2/<topic>/` for active implementation or `docs/reference/`
  for long-lived reference documentation (with `ko/docs/reference/`
  mirror). The original `plans/` file stays as a stub with a
  top-of-file note pointing to the promoted location.
- **Archived** — superseded or abandoned. Either delete, or move to
  `plans/_archive/` (create if needed).

There is no "complete" state for a research note. It is either still
useful as reference, or it is not.
