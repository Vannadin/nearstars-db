# Context notes — magnetopause re-gate

Append-only. Every derivation and every choice, with the reasoning, so the next
session does not re-derive them.

Calculator: `scripts/refs/magnetopause_geometry.py` (run with no arguments to
reproduce every number below).

## 1. The ram-pressure convention was already consistent, and reproduces

Both Proxima boards scale the stellar wind as `p = 2.0 nPa × (Mdot/Mdot_sun) / a_AU²`.
That was never written down anywhere, but it back-solves exactly from the
recorded values: Proxima b's 170 nPa at 0.04848 AU and Proxima c's 0.178 nPa at
1.5 AU both come out to four figures. Adopted as the stated convention.

Chapman-Ferraro then reproduces the recorded standoffs to within a quarter of a
percent for both Proxima planets: b 1.542 against a recorded 1.54, c 11.942
against 11.905. Those two noses are sound and are carried forward unchanged.

## 2. Polyphemus's recorded nose does not reproduce

The board records 23.5 R_p. The same formula with the board's own inputs
(B_eq 170 uT, 0.5 Mdot_sun at 1.6 AU, so p_ram 0.391 nPa, f = 2) gives
**22.14 R_p**. Using the board's own stated ram figure of 0.38 nPa instead
gives 22.24. Neither reaches 23.5; recovering it would need f = 2.36 rather
than the documented 2. Treated as an arithmetic drift in the earlier pass.

## 3. But the vacuum-dipole formula is the wrong one for a magnetodisc giant

This is the substantive finding of the re-gate, and it is not specific to
NearStars — Part A of the methodology has the same gap.

Chapman-Ferraro assumes the planetary field is a vacuum dipole out to the
boundary. A giant with a rotating, plasma-loaded magnetodisc inflates well
beyond that. The size of the discrepancy is measurable at Jupiter, because
Rutala 2025 fits `r_SS = 38.0 · p_SW^−0.25` R_J to the observed crossings:

| p_SW (nPa) | Chapman-Ferraro | Rutala fit | ratio |
|---|---|---|---|
| 0.03 | 46.2 R_J | 91.3 R_J | 1.98 |
| 0.13 (high) | 36.2 R_J | 63.3 R_J | 1.75 |
| 0.39 (Polyphemus') | 30.1 R_J | 48.1 R_J | **1.60** |

The ratio is not constant: Chapman-Ferraro goes as p^−1/6 and the Rutala fit as
p^−1/4, so the inflation factor itself falls as p^−1/12. Physically that reads
correctly — a harder wind squeezes the disc out of the magnetosphere and drives
the boundary back toward the vacuum-dipole answer. Evaluated at Polyphemus'
own 0.391 nPa the factor is **1.60**.

Polyphemus is if anything more disc-dominated than Jupiter: a ~1200x Io plasma
source against Jupiter's 1x, at a comparable spin (10.35 h against 9.93 h). So
1.60 is a floor, not a ceiling, for its inflation.

- Vacuum-dipole reading: **22.1 R_p**
- Disc-inflated reading (Jupiter's factor at this pressure): **35.3 R_p**

This cascades. At 22.1 R_p, Chaos (21 R_p) rides right at the boundary and the
board's "a gust of stellar wind can briefly leave it exposed" narrative holds
and in fact strengthens. At 35.3 R_p, Chaos sits comfortably inside and that
narrative fails. The belts are bounded at 0.6-0.8 R_mp, so they move too.

## 4. Polyphemus's alpha is an extrapolation either way

Rutala 2025 also fits `alpha = 0.28 + 1.08 · p_SW` (nPa), calibrated across the
observed Jovian range p_SW 0.03-0.13 nPa. Polyphemus sits at 0.391 nPa —
three times beyond the top of the calibration.

- Evaluating the fit anyway: **alpha = 0.702**
- Clamping to Jupiter's fitted ceiling: **alpha = 0.42**

Evaluating it is not obviously wrong: 0.702 lands between Earth's 0.58 and
Saturn's 0.736, both of which are measured, so the value is not out of family.
What is unsupported is the *linear* extrapolation that produced it. Saturn is
the counterexample that kills any universal pressure law — it carries the
highest measured alpha at one of the lowest pressures.

## 5. The moons split into two regimes, and the split is derived

The Alfven Mach number decides whether an embedded moon gets a Shue boundary or
a Ganymede-style sphere. The clean way to state it is as the density each moon
would need for M_A to reach 1, since the torus density profile is the uncertain
input and the threshold is not:

| moon | L (R_p) | v_rel (km/s) | parent B (uT) | n for M_A = 1 | as a multiple of the Io torus peak |
|---|---|---|---|---|---|
| Dante | 1.54 | 2.28 | 46.5 | 1.0e10 cm⁻³ | 5.0e6 x |
| Hades | 2.07 | 6.98 | 19.2 | 1.8e8 cm⁻³ | 9.0e4 x |
| Pandora | 3.53 | 28.79 | 3.87 | 4.3e5 cm⁻³ | 216 x |
| Cassandra | 7.0 | 74.61 | 0.50 | 1.1e3 cm⁻³ | **0.53 x** |
| Chaos | 21.0 | 247.53 | 0.018 | 0.13 cm⁻³ | 6.6e-5 x |

Dante, Hades and Pandora are sub-Alfvenic by margins nothing plausible closes —
Pandora would need 216x the *peak* Io torus density at 2.3x the source's
distance, where the density has fallen by orders of magnitude. Alfven-wing
regime, so a sphere.

Cassandra is the interesting one: its threshold is *below* the Io torus peak, so
with a ~1200x Io source it is very likely super-Alfvenic and does own a real bow
shock and swept tail. Chaos is unambiguously super-Alfvenic but has no field, so
nothing is owed either way.

Note Polyphemus's synchronous orbit is 1.663 R_p: Dante at 1.54 orbits *faster*
than the plasma corotates, so its relative flow is both tiny and reversed.

## 6. An embedded moon's standoff is set by magnetic pressure, not ram

At Pandora the parent's magnetic pressure is 5.943 uPa against 0.001 uPa of ram
— a factor of six thousand. Computing an embedded standoff from ram alone, the
way a planet's is computed, is simply the wrong balance.

Redone against total confining pressure:

- Pandora: **3.39 R_moon** (board records 2.6)
- Cassandra: **1.16 R_moon** (board records ~1.1 — this one holds)

Pandora's standoff is insensitive to the torus density precisely because ram is
negligible, so 3.39 is robust in a way the old 2.6 was not.

## 7. Proxima c's alpha moves on policy, not on new data

The board carries alpha 0.5 borrowed from Shue's Earth fit with a note that no
ice-giant fit exists. The methodology has since settled the ice-giant fallback
at Earth's **0.58**, justified by Voyager 2 finding Uranus and Neptune the
emptiest magnetospheres measured (Bridge 1986, Belcher 1989), which puts their
loading nearer Earth's than the gas giants'. Same reasoning, updated number.

The tail moves much further: the board's 125 R_c was a judgement call, and the
convention is now L = 150 x nose = **1791 R_c**.

## 8. Proxima b is on a template that contradicts its own field row

The board sets `radiation_model = irregular`, the stock template built for Mars'
crustal remanent magnetism — a body with *no* dynamo. Proxima b's own field row
says the opposite: an active, if weak, multipolar dynamo. Its standoff of 1.54
R_p is nearly Mercury's 1.45, and Mercury has a *fitted* Shue alpha of 0.5
(Winslow 2013), which makes it the right class analog rather than Mars.

Open question carried to the owner: `pause_deform 0.1`. It was removed from
Proxima c on the owner's judgement that multipolar fine structure reaching the
magnetopause is implausible. The same argument applies here, but b's board
treats the deformation as the point of the choice, so it is not mine to drop.
