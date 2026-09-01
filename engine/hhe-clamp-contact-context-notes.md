# Do our integrations read the clamped nodes? — context notes (Brief 30)

2026-09-01. Registration: `hhe-clamp-contact-checklist.md`. Instrumentation only —
temporary hooks in scratch runners; no committed code change; anchors untouched
(no --refresh anywhere, per the branch-③ freeze rule).

## §1 Contact — everything published touches the block

Stencil hook (replicates `_bicubic`'s clamped 4×4 stencil exactly) over standalone
integrations at the printed/frozen convergence points:

| run | grad_ad reads | contact | contact region |
|---|---|---|---|
| anchor Uranus | 1226 | **148 (12.1 %)** | 22.2–30.9 GPa · 2512–2624 K |
| anchor Neptune | 1124 | **208 (18.5 %)** | 22.4–36.9 GPa · 2359–2532 K |
| rock end B U (corrected decl) | 815 | 169 (20.7 %) | 28.4–48.1 GPa · 2240–2395 K |
| rock end B N (corrected decl) | 743 | 195 (26.2 %) | 31.7–61.5 GPa · 2085–2258 K |
| ice end B (4 runs) | 1893–2177 | 13.2–20.2 % | ~14–100 GPa · 2239–3979 K |
| gradient grid (14 runs) | 1802–2578 | 13.6–20.1 % | ~22–125 GPa · 1927–3147 K |

(First rock-end-B attempt used a wrong declaration — ice layer dropped — printed 0
reads; corrected and rerun, the wrong rows discarded.) **Branch ① is out: the anchors,
C13's 26 %/41 %, and every Brief 26 grid point read stencils containing clamped nodes.**

## §2 Propagation — the answers do not move beyond our own jitter

The 72 pressed nodes were replaced (uncommitted hook) by isotherm-wise linear
interpolation between the nearest unclamped neighbours, and both anchors re-solved:

| | Δλ | ΔR | ΔT_c |
|---|---|---|---|
| Uranus | +9.29e-6 | +8.97e-6 | +3.41e-4 |
| Neptune | −4.32e-5 | +2.92e-5 | +1.43e-4 |

Against the anchor reproduction jitter (3.7–3.9e-4): **λ and R sit 10–40× below;
T_c sits at 0.87–0.92× of it — within, but flush against the boundary, said plainly.**
Branch ② fires: the answers stand, and the fact stands with them — **our integrations
do read clamped values**, over 12–26 % of their envelope grad_ad reads, and a body
whose adiabat lies deeper in the block could move more. The substitute values are OUR
linear interpolation, not truth: this bounds sensitivity to this substitution, not the
distance to the unpublished true gradient — the honest name for the experiment.

## §3 What stays open

The physics of the block (molecular-to-atomic transition band) is the parallel
session's figure reading; whether the source's clamp is conservative or wild there is
not answerable from our side. If a future body's converged adiabat runs deeper into
the block (colder starts, higher Z), rerunning this contact+propagation pair is the
check — both runners are preserved in the session scratchpad (clamp_contact.py,
clamp_propagate.py; ~3 min total).
