# 엔진의 오늘 화성 구조 한 벌에서 P(r)·g(r) 를 뽑는 어댑터 — 열진화 v2-7 ②③, 적분기 기록 인자를 쓴다
"""The engine's present-day Mars structure as profiles, for the Samuel model (pre-registration v2-7 ②③).

The body file is run through the chain up to `interior_layers` and no further. Every `interior.integrate`
call on the way is made with the record on (`977dd2bd`, write-only); the profile kept is the call whose
structure is the answer — its normalised moment of inertia equals the one `interior_layers` reports.
Nothing is re-solved and no second structure is built (the directing seat's choice ⓐ over ⓑ).

`g(r) = G m(r) / r²` from the recorded enclosed mass. Pressure and gravity between rows are linear
interpolations in radius.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior                        # noqa: E402


class Profile:
    """Recorded rows (r, P, m, T, material), outward, with interpolation in radius."""

    def __init__(self, rows: list, structure, source: str):
        self.r = [row[0] for row in rows]
        self.p = [row[1] for row in rows]
        self.m = [row[2] for row in rows]
        self.material = [row[4] for row in rows]
        self.radius_m = structure.radius_m
        self.core_radius_m = structure.core_radius_m
        self.mass_kg = structure.mass_kg
        self.nmoi = structure.moi / (structure.mass_kg * structure.radius_m ** 2)
        self.source = source

    def _interp(self, ys: list, r: float) -> float:
        rs = self.r
        if r <= rs[0]:
            return ys[0]
        if r >= rs[-1]:
            return ys[-1]
        lo, hi = 0, len(rs) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if rs[mid] <= r:
                lo = mid
            else:
                hi = mid
        w = (r - rs[lo]) / (rs[hi] - rs[lo])
        return ys[lo] + w * (ys[hi] - ys[lo])

    def pressure(self, r: float) -> float:
        return self._interp(self.p, r)

    def gravity(self, r: float) -> float:
        return interior.G * self._interp(self.m, r) / (r * r)


def mars_profile(body_path: Path) -> Profile:
    """Run `body_path` up to `interior_layers` with the record on; return the answer's profile."""
    import run
    from state import Missing

    captured: list = []
    plain = interior.integrate

    def recording(*args, **kw):
        rows: list = []
        st = plain(*args, record=rows, **kw)
        captured.append((st, rows))
        return st

    body, _expected = run.load_body(body_path)
    g = run.load_chain()
    interior.integrate = recording
    try:
        for unit in run.order(g):
            for node in unit:
                if g["nodes"][node].get("kind") != "computed":
                    continue
                fn = run.registry.get(node)
                if fn is None:
                    continue
                body.current_node = node
                try:
                    body.record(node, fn(body))
                except Missing:
                    pass
                body.current_node = None
            if "interior_layers" in body.results:
                break
    finally:
        interior.integrate = plain
    res = body.results.get("interior_layers")
    if res is None or not res.applicable:
        raise RuntimeError(f"interior_layers did not produce a structure for {body_path.name}")
    nmoi = res.values["nmoi"]
    hits = [(st, rows) for st, rows in captured
            if abs(st.moi / (st.mass_kg * st.radius_m ** 2) - nmoi) <= 1e-12 * nmoi]
    if not hits:
        raise RuntimeError(f"no recorded integration has the answer's nmoi {nmoi!r} "
                           f"({len(captured)} calls recorded)")
    st, rows = hits[-1]
    return Profile(rows, st, f"{body_path.name} → interior_layers, call {captured.index((st, rows)) + 1} "
                             f"of {len(captured)}, {len(rows)} rows")


def save(profile: Profile, path: Path) -> None:
    """Keep the rows so a scan does not re-solve Mars each time (json, radius-ordered)."""
    import json
    path.write_text(json.dumps({"source": profile.source, "radius_m": profile.radius_m,
                                "core_radius_m": profile.core_radius_m, "mass_kg": profile.mass_kg,
                                "nmoi": profile.nmoi, "r": profile.r, "p": profile.p, "m": profile.m,
                                "material": profile.material}), encoding="utf-8")


def load(path: Path) -> Profile:
    import json
    d = json.loads(path.read_text(encoding="utf-8"))
    p = Profile.__new__(Profile)
    for k in ("r", "p", "m", "material", "radius_m", "core_radius_m", "mass_kg", "nmoi", "source"):
        setattr(p, k, d[k])
    return p
