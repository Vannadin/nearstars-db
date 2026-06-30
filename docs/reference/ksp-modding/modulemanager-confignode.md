---
title: ModuleManager patch DSL & ConfigNode (pillar ④)
status: draft
created: 2026-06-30
---

# ModuleManager patch DSL & ConfigNode

The generic Module Manager (MM) patch language and the ConfigNode substrate it
operates on — the layer **every** NearStars cfg writer emits onto. Grounding policy +
legend: [`README`](README.md).

**Grounding (stronger than usual).** Unlike stock KSP, ModuleManager is
**open-source** (`sarbian/ModuleManager`) — so every claim here is witnessed in the
**parser source itself** (the repo's `README.md` carries no syntax docs; the KSP-forum
"MM Handbook" would only be M). All rows **H** unless flagged, pinned to v4.2.3
`c4561925f983e7ae81d9dfd4d11356a35cb6b9b6`.

**Scope / alignment (read this).** This doc defines the **generic DSL only**. It does
**not** restate:
- NearStars cfg conventions (the `NearStarsSystem` tag, `NearStars/BodyName` identifier,
  Sol/RSS dual-compat, file separation, the Principia no-`:FOR` rule) → owned by
  [`mod-release-layout.md` §2](../mod-release-layout.md).
- per-mod node schemas → owned by the cfg skills (`kopernicus-cfg`, `firefly-cfg`,
  `principia-cfg`, `researchbodies-cfg`).

§10 maps the project's actual MM headers to the DSL features below (the skills are the
in-repo witnesses).

---

## 1. ConfigNode basics
A **node** is `NAME { … }`; a **value** is `key = value`; `//` comments to end of line.
MM parses node *names* and value *keys* for leading/trailing operator characters
(below) and otherwise leaves the ConfigNode format untouched.

## 2. Node operators (leading char of a node name / sub-key)
`CommandParser.Parse` — `switch(name[0])` (`CommandParser.cs:15-54`; enum `Command.cs:5-24`).

| Op | Command | Meaning |
|---|---|---|
| *(none)* | Insert | insert new node/value (default) |
| `@` | Edit | edit an existing node/value |
| `%` | Replace | **edit-or-create** (edit if present, else create) |
| `+` / `$` | Copy | copy an existing node/value |
| `-` / `!` | Delete | delete a node/value |
| `|` | Rename | rename |
| `#` | Paste | paste |
| `*` | Special | special marker (≠ the §7 name-wildcard mechanism) |
| `&` | Create | create |

## 3. Value operators (`@key <op>= value`)
`OperatorParser.Parse` (`OperatorParser.cs:7-54`; enum `Operator.cs:5-14`). The op is the
**last char of the key, recognized only if preceded by a space/tab** (`OperatorParser.cs:15`)
— so `@key += 5` is arithmetic but `@key+=5` is a literal key named `key+`.

| Written | Operator | Meaning |
|---|---|---|
| `@key = v` | Assign | set (default) |
| `@key += v` | Add | |
| `@key -= v` | Subtract | |
| `@key *= v` | Multiply | |
| `@key /= v` | Divide | |
| `@key != v` | **Exponentiate** | power — keyed on trailing `!` (NOT "not-equals") |
| `@key ^= v` | RegexReplace | regex find/replace on existing value |

> **Correction (vs. common belief):** power is `!=` → Exponentiate
> (`OperatorParser.cs:40-42`); `^=` is regex-replace, not power.

## 4. Pass / ordering directives + the `:FOR` vs `:NEEDS` distinction
Pass execution order (`PatchList.GetEnumerator`, `PatchList.cs:108-126`):
**`:INSERT` → `:FIRST` → legacy (no-tag `@…`) → per-mod[ `:BEFORE[m]` → `:FOR[m]` →
`:AFTER[m]` ] → `:LAST[m]` → `:FINAL`.**

**`:FOR` vs `:NEEDS` — the project-critical distinction** (different code paths):
- **`:FOR[mod]`** — `ForPassSpecifier.CheckNeeds` (`ForPassSpecifier.cs:18-24`) calls
  `needsChecker.CheckNeeds(mod)`; if `mod` absent → patch **dropped**. It does double
  duty: (a) schedules the patch into that mod's pass slot, AND (b) **declares `mod` as a
  patch-author identity** (the name in `:FOR[X]` is added to the mod list that later
  `:NEEDS`/`:BEFORE`/`:AFTER` check). ⇒ **use `:FOR[X]` only if X is *your* mod** —
  using it on a node another mod authored falsely claims authorship.
- **`:NEEDS[mod]`** — a pure **conditional filter** (`NeedsChecker`, §5): apply only if
  present. No ordering slot, no identity claim.
- `:BEFORE[m]`/`:AFTER[m]` require `m` installed (drop if absent); **`:LAST[m]` does
  NOT** (`LastPassSpecifier.cs:16` returns `true` unconditionally); `:FIRST`/`:FINAL`
  take no mod arg.

This is exactly why NearStars uses `@Kopernicus:FOR[NearStarsSystem]` (we author it) but
Principia patches are `@principia_…:NEEDS[…]` with **no** `:FOR` (they edit roots
Sol-Configs authored — `:FOR` would claim authorship spuriously). See
[`mod-release-layout.md` §2.1](../mod-release-layout.md) + the `principia-cfg` skill.

## 5. `:NEEDS[...]` boolean syntax
`NeedsChecker.CheckNeedsExpression` (`NeedsChecker.cs:42-70`); extraction `:102-116`
(case-insensitive `:NEEDS[`, content to first `]`, tag stripped from name).

| Syntax | Meaning |
|---|---|
| `,` and `&` | **AND** — equivalent (`Split(',', '&')`, `:46`). `[A&B]` ≡ `[A,B]` |
| `\|` | **OR** within an AND-group (`:49`) |
| `!` (token prefix) | **NOT**, first char of a token (`:54`). `[!A]` |
| precedence | AND outermost, OR within group, NOT per-token → `[A&B\|C]` = `A AND (B OR C)` |
| `X/Y` | also satisfied if dir `GameData/X/Y` exists (`:79-100`) |

Mod match is case-insensitive (`:39`). **No bracket-nesting** inside `:NEEDS` (extraction
stops at first `]`, `:110`). Applied recursively to nested nodes/values (`:118-185`).

## 6. `:HAS[...]` filter
`MMPatchLoader.CheckConstraints` (`MMPatchLoader.cs:~1459`). Top-level `,` = AND; leading
char dispatches:

| Form | Meaning |
|---|---|
| `@NODE[name]` | node present (optional name match) |
| `!NODE[name]` | node absent |
| `#key[value]` | value present and matches (wildcard / numeric) |
| `~key[value]` | value absent, **or** present but ≠ value |
| `#key[<N]` / `#key[>N]` | numeric less-/greater-than |
| `@NODE[n]:HAS[…]` | nests (recurses into matched subnode) |

## 7. Wildcards
`*` → `.*`, `?` → `.` (single char), `^…$`-anchored, rest `Regex.Escape`d
(`MMPatchLoader.cs:1556-1567`). A node-name `name` may list multiple patterns separated
by `,` or `|` (alternation, any-match — `NodeMatcher.cs:25`). (The `?` single-char form
is real but often omitted in community docs.)

## 8. Indexing (`@MODULE[name],0`)
The `,index` trailer after `]` is **captured** by `TagListParser` (the tag's `trailer`
field, `TagListParser.cs:65-90,127-153`) — **H**. The apply-time *semantics* (`,0` = first
match, `,*` = all, last-index) are resolved downstream and were **not witnessed at the
apply site** — **M** (consistent with community docs, not source-confirmed here).

## 9. MM variables (`#`/`&`-vars/`@/` paths) — not verified
A value-substitution/variable subsystem was **not witnessed** in the fetched files
(`#` = Paste command + `:HAS` value marker are the only witnessed `#` uses). **L /
unverified** — do not document MM variables as grounded without a further targeted fetch.

---

## 10. NearStars usage → DSL feature (in-repo witnesses)
The conventions are owned by [`mod-release-layout.md` §2](../mod-release-layout.md) + the
cfg skills; this table just anchors the DSL above to the project's real headers.

| Project header | DSL feature | owner |
|---|---|---|
| `@Kopernicus:FOR[NearStarsSystem]` | `@` edit + `:FOR` pass/authorship (we author the body def) | `kopernicus-cfg`; layout §2.1 |
| `ATMOFX_PLANET_PACK:NEEDS[NearStarsSystem]` | top-level node + `:NEEDS` conditional | `firefly-cfg` |
| `@principia_gravity_model:NEEDS[NearStarsSystem,SolSystem]` | `@` edit + `:NEEDS` with `,`-AND, **no `:FOR`** (edits Sol-authored roots) | `principia-cfg`; layout §2.1 exception |
| `@principia_initial_state:NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale]` | `:NEEDS` with `,`-AND + `!`-NOT (exclude quarter-scale) | `principia-cfg` |
| `RESEARCHBODIES:NEEDS[ResearchBodies&Kopernicus]` `loadAs=mod` | `:NEEDS` with `&`-AND | `researchbodies-cfg` |
| `@EVE_CLOUDS:NEEDS[SolSystem]:FOR[NearStarsSystem]` | combined `:NEEDS` (conditional) + `:FOR` (our authorship/pass) | layout §2.1 |

---

## Gaps / not verified
- Index apply-semantics (`,0`/`,*`/last) — trailer captured (H), apply meaning **M**.
- MM variables — **L / unverified**.
- `:AFTER` install-check — **H by symmetry** with `:BEFORE` (dedicated file not opened).

## Provenance
`sarbian/ModuleManager` @ `c4561925f983e7ae81d9dfd4d11356a35cb6b9b6` (v4.2.3), parser
source read via raw fetch. Permalink base:
https://github.com/sarbian/ModuleManager/blob/c4561925f983e7ae81d9dfd4d11356a35cb6b9b6/

## Related
- [`README`](README.md) — KB index + grounding policy
- [`mod-release-layout.md` §2](../mod-release-layout.md) — canonical NearStars cfg conventions (this doc defers to it)
- cfg skills `kopernicus-cfg` / `firefly-cfg` / `principia-cfg` / `researchbodies-cfg` — per-mod schemas (the §10 witnesses)
