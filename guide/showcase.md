<!-- 자랑할 만한 결과 몇 가지와 정직한 실패 하나 -->
# Showcase

Three deep dives that show what "evidence-grounded" means once you push on it, including the place where the method openly hits its limit.

## The external-observer benchmark: curating our own solar system from 10 parsecs

The sharpest way to test a curation pipeline is to point it at the one planetary system where we already know every answer. So we ran the full NearStars Phase 2/3 process on the Solar System as it would look to an external observer 10 parsecs away, feeding it only the data such an observer could plausibly have.

The exercise calibrates every confidence grade in the database, and its headline result is a failure we are happy to report. **Venus is a greenhouse blind spot.** From outside, its equilibrium temperature computes to 227–299 K, and the pipeline has no way to see the actual 737 K surface. Wherever our confidence grades read "low", this benchmark is the reason: those grades map one-to-one onto what is genuinely observable from far away.

→ [Read the full benchmark](https://github.com/Vannadin/nearstars-db/blob/main/docs/reference/solar-system-external-observer.md)

## Heliospheres & the local interstellar medium

Every star in the mod plows through the local interstellar medium, and each carries its own astrosphere: a teardrop-shaped bubble of stellar wind whose shape and orientation depend on how fast the star moves relative to its local interstellar cloud.

To get those bubbles right, we built a dataset of the 15 local clouds (Redfield & Linsky 2008) and 27 observed astrospheres (Wood et al.), computed each star's relative wind vector, and checked the orientations against measured astrotail angles. The result renders in the 3D star map: toggle heliospheres on and every star's bubble points the way it should.

→ [Dataset & method](https://github.com/Vannadin/nearstars-db/blob/main/docs/reference/lism-kinematics.md) · [see it in the star map](https://vannadin.github.io/nearstars-db/starmap.html)

## Data comparison with REX (Real Exoplanets)

NearStars is the spiritual successor to the KSP 1.8-era REX concept, so it seemed only fair to audit ourselves against it, comparing five systems line by line against REX v0.9.6.

The findings, stated plainly: no coverage gaps on our side; one body REX carries that the literature has since retracted (Barnard b in its original 2018 form); one likely omission on REX's side (tau Ceti e); and the structural difference that motivates NearStars in the first place, which is genuine multiple-star-system handling (barycenters, Keplerian solutions, epoch propagation) rather than single-star placement.

→ [Full comparison](https://github.com/Vannadin/nearstars-db/blob/main/docs/reference/rex-data-comparison.md)
