
## Open item found while wiring Kerbalism (2026-08-04)

Pandora's inner belt carves out to 1.098 R (563 km above the surface), which the owner
confirmed is the wanted behaviour: the empty zone should sit well above the atmosphere,
not at it. The physical reason is the loss cone, not the atmosphere height — particles
mirroring down into the upper atmosphere are absorbed, so a belt's inner edge stands
hundreds of km above the air. Earth's is the anchor at ~1000 km, and `earth_phys` already
notes it.

What is missing is the derivation: nothing on the board says why 563 km rather than
Earth's 1000 km scaled to Pandora. Left as-is by owner decision; if it is ever revisited,
derive the inner edge from the loss cone and re-fit the border torus to it.
