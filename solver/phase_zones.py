# 상 구간 행 수집 — 받아들인 패스의 층마다 노드의 상 이름과 착지 사건으로 구간 행을 만들어 Answer.zones 에 (zones-prereg, 물리 변화 없음)
"""Phase-zone rows of the accepted pass (`rewrite/layers/zones-prereg.frozen.md`, artifacts blob 244711f0).

`collect(body, views, acc)` runs once, on the accepted pass only, after every value of the answer is made (as
material_notes.collect does). It reads each entered layer's accepted nodes and that layer's landed events, and
returns a tuple of `PhaseZone`. It never calls `state()`, touches no counter, no warm start and no notes, so
it cannot change a value (§3.2). Every label read goes through `_read`, the one function §4.3 (e) spies on.

Labels (§2.2): a record view's `phase_read(p, t)` (a Stop reads `stop:<kind>`); a legacy view's
`mat.phase_at(p).name` (an empty name reads `<material>#<index>`); an assemblage-family view (AssemblageView, and
BasalView, which carries the overlying view's curves) gives one row per layer with its landed transition and
coexistence events as `crossings`, unchained (§2.2, 68 n4). T for a read is the node's y[3] (§2.1).

Ends (§2.3): a landed node is the shared end of the zones on its two sides, whatever its own read says; a zone's label
is the common read of the nodes strictly inside it; interior reads that disagree split the zone at the first change
(`between_nodes`); a zone with no interior node is `unread`; a landed event with no label change ends no zone.
"""
from __future__ import annotations

from dataclasses import dataclass

from solver import material_view as mv
from solver import result
from solver import stepper as st

#: what may end a phase zone (zones-prereg §2.1); `layer:` and `event:` carry a name after the colon
ZONE_END_KINDS = ("surface", "layer:", "event:", "centre", "r_floor", "between_nodes")
#: the label of a zone with no interior node (zones-prereg §2.3)
ZONE_UNREAD = "unread"


def _zone_end(name: str, by: str) -> None:
    if not any(by == k if not k.endswith(":") else (by.startswith(k) and len(by) > len(k)) for k in ZONE_END_KINDS):
        raise ValueError(f"PhaseZone.{name} {by!r} is not one of {ZONE_END_KINDS}")


@dataclass(frozen=True)
class PhaseZone:
    """One contiguous run of one phase label inside one entered layer of the accepted pass (zones-prereg §2.1).
    `top` / `base` are the pass's node values (m, r, p, t) at the zone's ends; `crossings` lists an assemblage layer's
    landed transition and coexistence events as (name, m, p, t), reported and not chained (§2.2)."""
    layer: str
    material: str
    label: str
    top: tuple
    base: tuple
    top_by: str
    base_by: str
    record_phases: int
    single_phase_why: str | None = None
    crossings: tuple = ()

    def __post_init__(self):
        for n in ("top", "base"):
            v = tuple(getattr(self, n))
            if len(v) != 4:
                raise ValueError(f"PhaseZone.{n} must be (m, r, p, t), got {v!r}")
            object.__setattr__(self, n, tuple(result.check_finite(f"PhaseZone.{n}", x) for x in v))
        _zone_end("top_by", self.top_by)
        _zone_end("base_by", self.base_by)
        if not self.label:
            raise ValueError("PhaseZone.label is empty")
        if int(self.record_phases) != self.record_phases or self.record_phases < 1:
            raise ValueError(f"PhaseZone.record_phases {self.record_phases!r} is not a positive int")
        cr = []
        for c in self.crossings:
            name, *nums = tuple(c)
            if not name or len(nums) != 3:
                raise ValueError(f"PhaseZone crossing {c!r} is not (name, m, p, t)")
            cr.append((str(name), *(result.check_finite("PhaseZone crossing", x) for x in nums)))
        object.__setattr__(self, "crossings", tuple(cr))


@dataclass(frozen=True)
class Answer(result.Answer):
    """`result.Answer` with the accepted pass's phase-zone rows (zones-prereg §2.4 Z1, post-freeze note 1).

    A subclass here, not a field in solver/result.py: result.py is in the shipped fall sets' read closure
    (fall_sets.closure(), pinned by blob at load), so editing it makes every set refuse until rebuilt — the same reason
    nodes/types.py subclasses Provenance. The class keeps the name «Answer», so result.plain's «type» is unchanged and
    its bytes are frozen Z1's: result.Answer's fields, then «zones». Readers use getattr(answer, "zones", ())."""
    zones: tuple = ()

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(self, "zones", tuple(self.zones))
        for z in self.zones:
            if not isinstance(z, PhaseZone):
                raise ValueError(f"Answer.zones holds {z!r}, not a PhaseZone")

#: event-name prefixes listed as an assemblage layer's crossings (transitions and walked coexistence segments)
CROSSING_PREFIXES = ("phase:", "coexist-")
FE_PREM_WHY = ("one structure phase in the record: no liquid/solid split and no inner-core step "
               "(inventory-phase1 §2; phase-plan row 3, owner 10-06)")
LEGACY_ONE_WHY = "one name read in this layer"
RECORD_ONE_WHY = "one structure phase in the record"
ASSEMBLAGE_WHY = "the table's one id; crossings not chained"


def _assemblage_family(view) -> bool:
    from solver import material_assemblage as ma
    return isinstance(view, (ma.AssemblageView, ma.BasalView))


def _read(view, material_id, p, t) -> str:
    """The phase label the view gives at (p, t): the one read function of this module (§4.3 (e))."""
    if isinstance(view, mv.RecordView):
        got = view.phase_read(p, t)
        return f"stop:{got.kind}" if isinstance(got, st.Stop) else str(got)
    mat = getattr(view, "mat", None)
    if mat is not None and hasattr(mat, "phase_at"):
        ph = mat.phase_at(p)
        name = getattr(ph, "name", None)
        if name:
            return str(name)
        phases = list(getattr(mat, "phases", ()) or ())
        return f"{material_id}#{phases.index(ph) if ph in phases else '?'}"
    raise TypeError(f"{material_id}: {type(view).__name__} has no phase read (phase_read or mat.phase_at)")


def _record_phases(view) -> int:
    if _assemblage_family(view):
        return 1
    if isinstance(view, mv.RecordView):
        return max(1, len(getattr(view, "phases", ()) or ()))
    mat = getattr(view, "mat", None)
    return max(1, len(getattr(mat, "phases", ()) or ()))


def _why(view, material_id, n_phases):
    if n_phases != 1:
        return None
    if _assemblage_family(view):
        return ASSEMBLAGE_WHY
    if isinstance(view, mv.RecordView):
        return FE_PREM_WHY if material_id.startswith("fe_prem") else RECORD_ONE_WHY
    return LEGACY_ONE_WHY


def _node(path_node) -> tuple:
    m, y, _k = path_node
    return (m, y[0], y[1], y[3])


def _ends(body, acc, j):
    """(top_by, base_by) of layer j (index into body.layers) on the accepted pass."""
    layers = body.layers
    names = {b[0] for b in acc.boundaries}
    top = "surface" if j == len(layers) - 1 else f"layer:{layers[j].id}/{layers[j + 1].id}"
    if j > 0 and f"{layers[j - 1].id}/{layers[j].id}" in names:
        base = f"layer:{layers[j - 1].id}/{layers[j].id}"
    else:
        base = "r_floor" if getattr(acc, "floor_end", False) else "centre"
    if top != "surface" and top[len("layer:"):] not in names:
        top = "surface"          # the pass started inside this layer (no boundary above was located)
    return top, base


def _segments(labels, cuts):
    """Zones of one layer: [(a, b, label, base_by_kind)] over node indices, from the read labels and the cut nodes
    (landed events strictly inside). base_by_kind is «cut» (an event node), «split» (between_nodes) or «end»."""
    n = len(labels)
    bounds = [0] + [c for c in sorted(set(cuts)) if 0 < c < n - 1] + [n - 1]
    raw = []
    for a, b in zip(bounds, bounds[1:]):
        inner = labels[a + 1:b]
        if not inner:
            raw.append([a, b, ZONE_UNREAD])
            continue
        start, cur = a, inner[0]
        for k in range(a + 1, b):
            if labels[k] != cur:                       # a change with no landed event: split, shared node k − 1
                raw.append([start, k - 1, cur, "split"])
                start, cur = k - 1, labels[k]
        raw.append([start, b, cur])
    out = []
    for i, z in enumerate(raw):
        kind = z[3] if len(z) > 3 else ("end" if z[1] == n - 1 else "cut")
        if out and out[-1][2] == z[2] and z[2] != ZONE_UNREAD and out[-1][3] == "cut":
            out[-1][1], out[-1][3] = z[1], kind        # a landed event with no label change ends no zone
        else:
            out.append([z[0], z[1], z[2], kind])
    return out


def collect(body, views, acc) -> tuple:
    rows = []
    events_at = getattr(acc, "events_at", ())
    for j in range(len(body.layers) - 1, -1, -1):
        layer = body.layers[j]
        path = acc.profiles.get(layer.id)
        if not path:
            continue
        view = views[layer.id]
        mid = getattr(view, "material_id", None) or layer.material
        mine = [(name, m) for lid, name, m, _y in events_at if lid == layer.id]
        node_of = {}
        for i, (m, _y, _k) in enumerate(path):
            node_of.setdefault(m, i)
        top_by, base_by = _ends(body, acc, j)
        n_ph = _record_phases(view)
        why = _why(view, mid, n_ph)
        # the nodes strictly inside the layer are read; its two end nodes are never a zone's interior (§2.3)
        labels = [None] + [_read(view, mid, y[1], y[3]) for _m, y, _k in path[1:-1]] + ([None] if len(path) > 1 else [])
        if _assemblage_family(view):
            segs = _segments(labels, [])
            crossings = [(name, m, y[1], y[3]) for lid, name, m, y in events_at
                         if lid == layer.id and name.startswith(CROSSING_PREFIXES)]
        else:
            segs = _segments(labels, [node_of[m] for _name, m in mine if m in node_of])
            crossings = []
        first_event = {}
        for name, m in mine:
            if m in node_of:
                first_event.setdefault(node_of[m], name)
        for k, (a, b, label, kind) in enumerate(segs):
            t_by = top_by if k == 0 else rows[-1].base_by
            if kind == "end":
                b_by = base_by
            elif kind == "split":
                b_by = "between_nodes"
            else:
                b_by = f"event:{first_event[b]}"
            rows.append(PhaseZone(layer.id, mid, label, _node(path[a]), _node(path[b]), t_by, b_by, n_ph,
                                         why, tuple(crossings) if k == 0 else ()))
    return tuple(rows)


def check_rows(answer) -> list:
    """§4.3 (a) tiling and (b) no between_nodes / unread, over an Answer's rows; [] when they hold."""
    bad = []
    by_layer = {}
    for z in answer.zones:
        by_layer.setdefault(z.layer, []).append(z)
    located = {b.name for b in answer.boundaries}
    for lid, zs in by_layer.items():
        for a, b in zip(zs, zs[1:]):
            if a.base != b.top or a.base_by != b.top_by:
                bad.append(f"(a) {lid}: {a.label} base {a.base_by} ≠ {b.label} top {b.top_by}")
        for z in zs:
            if z.base[2] < z.top[2]:
                bad.append(f"(a) {lid}: {z.label} P falls from {z.top[2]!r} to {z.base[2]!r}")
            for end in (z.top_by, z.base_by):
                if end.startswith("layer:") and end[len("layer:"):] not in located:
                    bad.append(f"(a) {lid}: {end} is not a located boundary")
            if z.base_by == "between_nodes" or z.label == ZONE_UNREAD:
                bad.append(f"(b) {lid}: {z.label} ends {z.base_by}")
        if zs[0].top_by.startswith("event:") or zs[-1].base_by.startswith("event:"):
            bad.append(f"(a) {lid}: the layer's own ends are events")
    for lid in answer.profiles:
        if lid not in by_layer:
            bad.append(f"(a) {lid}: a profiled layer has no row")
    return bad
