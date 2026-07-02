# NearStars interstellar branch — START HERE

This directory holds the design + implementation spec for the NearStars
interstellar-precision work. **The code and the spec both live on THIS branch
(`nearstars-interstellar`) of THIS repo (`Vannadin/Principia`).** You should not
need any other repo to implement.

## Repo map (who is who)

```
mockingbirdnest/Principia        upstream, public open source — never edited, just the fork root
        │ fork
        ▼
Vannadin/Principia   ◀── YOU ARE HERE. The only working repo.
   branch: nearstars-interstellar
     ├─ docs/nearstars/        ← this spec (impl-spec.md + research/)
     └─ (all C++ changes land on this same branch, next to the code they describe)

Vannadin/nearstars-db            the NearStars mod repo — keeps a COPY of these docs as a
                                 design/decision record only. No code. Not needed to build.
schultz-dev0/principia-docs      Schultz's doc hub — PR #2 shares this spec with him (FYI/collab).
```

One sentence: **work happens on `Vannadin/Principia` @ `nearstars-interstellar`; the other three repos are the fork root, a record, and a heads-up to Schultz.**

## Where to run the implementation (fable)

The spec was written by opus research agents; the implementation is meant to be
driven by **fable in a separate Claude Code session**, working directly in a
clone of this fork. Concretely:

1. **Clone the fork to a durable location** (NOT a temp/scratch dir — it must
   survive across sessions). For example:
   ```
   git clone https://github.com/Vannadin/Principia ~/Desktop/Principia-nearstars
   cd ~/Desktop/Principia-nearstars
   git checkout nearstars-interstellar
   ```
2. **Start Claude Code in that directory**, set the model to **fable**
   (`/model fable`), and point it at this spec:
   > "Implement WS1 commit 1 from `docs/nearstars/impl-spec.md`. Read
   > `impl-spec.md §2–4` and `research/R1-fp-precision.md` first."
3. fable edits C++ on this branch, commits, and pushes back to
   `Vannadin/Principia`. Each session picks up where the last left off because
   the branch is the shared state.

Notes:
- The `research/R*.md` file:line citations are against upstream master
  `440310a9`. If the branch has been rebased onto a newer master, re-anchor by
  symbol name (functions are stable; line numbers drift).
- **Build gate:** Principia's build is bespoke and heavy (MSVC/clang). Validate
  the headless C++ tests first — WS1 commit 1 (`interstellar_precision_test`)
  needs no KSP install. The KSP-facing commits (WS3, and WS1's plugin wiring)
  need a full build + KSP, which is the slow part.

## Reading order

1. `impl-spec.md` — master: three workstreams, build order, the two key decisions.
2. `research/R1-fp-precision.md` — WS1 (long-distance FP precision).
3. `research/R2-soi-code-map.md` + `research/R3-soi-numerics.md` — WS2 (SOI cutoff).
4. `research/R4-thrust-under-warp.md` — WS3 (thrust under timewarp).
5. `design-draft.md` — earlier narrative (superseded on the SOI question by R3).
