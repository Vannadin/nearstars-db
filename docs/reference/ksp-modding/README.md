---
title: KSP modding knowledge base — index
status: living
created: 2026-06-30
---

# KSP modding knowledge base

**What this is.** A Claude-facing, *grounded* knowledge base for authoring the
NearStars C# plugins (relativity, warp, planner, flux-tube) against KSP 1.12.x.
It exists because stock-API knowledge was previously ungrounded training memory —
and that memory was wrong at least once (`ScaledSpace.Factor` → actually
`ScaleFactor`). The KB replaces assertion with citation, and it **accretes by
grounding, not by memory-dump**.

**Grounding policy (applies to every doc here).**
- KSP is **closed-source**. There is no public KSP repo to cite by `file:line`, so
  every stock-API claim is **witnessed by an open-source mod that calls it** (a mod
  compiling `FlightGlobals.fetch.SetVesselTarget(...)` proves the member exists).
  Citations are `repo path:line` (+ permalink), verified by fetching raw files.
- **Confidence:** **H** direct code witness · **M** decompiled-XML doc mirror /
  indirect · **L** not witnessed / inferred.
- **DLL decompile is the gold standard, deferred** — no KSP install on this dev
  machine. When obtained, `Assembly-CSharp.dll` (ILSpy/dnSpy) supersedes the
  M-confidence rows. License: only *interop facts* are committed; the DLL and any raw
  decompiled dump stay local/gitignored. See [[project_ksp_stock_api_grounding]].

---

## Coverage map

| # | Pillar | Home | Status |
|:-:|--------|------|--------|
| ① | **Stock C# API** (Assembly-CSharp surface) | [`ksp-stock-api.md`](ksp-stock-api.md) | **live** — planner slice (targeting, map camera, scaled-space rendering, orbit/body data); grows as touched |
| ② | **Plugin scaffolding & build** (KSPAddon, PartModule, VesselModule, MonoBehaviour lifecycle, .csproj/refs, AssemblyLoader, deployment) | [`plugin-scaffolding.md`](plugin-scaffolding.md) | **live** |
| ③ | **Unity-for-KSP** (GameObject/Transform, coroutines, LineRenderer/GL, IMGUI, layers, ScaledSpace) | [`unity-for-ksp.md`](unity-for-ksp.md) | **live** |
| ④ | ModuleManager & ConfigNode (patch syntax, persistence nodes) | — | deferred (lower priority; cfg-side partly in the skills below) |
| ⑤ | **Persistence & Harmony** (OnSave/OnLoad, ProtoVessel, scenario modules, Harmony patterns, the part-force / `FashionablyLate` channel) | [`persistence-harmony.md`](persistence-harmony.md) | **live** |
| ⑥ | Integration subsystems (Kopernicus, Principia, Kerbalism, Firefly, ResearchBodies) | *skills + reference* | **already grounded** — see below, not duplicated here |

**Scope chosen 2026-06-30:** the **plugin-authoring core (①②③⑤)** first — the real gap
that unblocks NearStars' C# plugins. ④ deferred; ⑥ already covered.

### ⑥ is already grounded elsewhere (do not duplicate)
- cfg-writing skills: `kopernicus-cfg`, `firefly-cfg`, `principia-cfg`, `researchbodies-cfg`
- [`principia-cfg-reference`](../principia-cfg-reference.md) — open-source (MIT), cited `file:line`

---

## Open / deferred (do not assume)
- **Interstellar-scale map view** — can a body a light-year away be selected/rendered
  in stock map view? Not answerable from public source; needs the DLL or an in-game
  test. See [`ksp-stock-api.md` §6](ksp-stock-api.md).
- **KB gaps to close** (M/L, witness pending) — `VesselModule.OnSave` override,
  `[KSPScenario]` attribute args + registration path, `part.AddForceAtPosition`,
  `WaitForSeconds`/`WaitForFixedUpdate`. See each pillar doc's *Gaps* section.
- **DLL decompile** — the gold-standard grounding, pending a KSP install.

## Related
- [`gameplay/interstellar-expansion/`](../../../gameplay/interstellar-expansion/) — the plugins this KB serves
- [`plugins/`](../../../plugins/) — the draft C# whose `// VERIFY:` markers this KB resolves
