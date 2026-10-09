# 천체 꼴 — 층 목록 · 표면 상태 · 닫힘 미지수 하나 · 역할로 찾는 경계 (phase1-design D-A2-1..4, D-A2-8).
"""Body types of the phase-1 solver (`rewrite/phase1-design.frozen.md` D-A2-1..4, D-A2-8, §X1–§X2).

A `Body` is built only by `validate` (or by tests). It is frozen, finite and in SI units. The solver reads
`layers`, `boundaries`, `surface` and `closure` and nothing else (§X2); body-wide declarations and later-tools keys
ride along for the history and the old nodes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

import yaml

from solver.result import check_finite, check_in

EXTENT_KINDS = ("mass_fraction", "radius_from_centre", "depth_from_surface", "phase", "thickness_above")  # §A1.3
THERMAL_KINDS = ("adiabatic", "conductive", "isothermal")      # D-A2-2
CLOSURE_KINDS = ("R", "boundary_mass", "composition")          # D-A2-8, §A1.2
P_S_SOURCES = ("material_floor", "declared")                   # §A1.2 (r2 H2)
UNCERTAINTY_BASES = ("±", "1σ", "min–max")                     # D-A2-2 declared input bands

ROLES_PATH = Path(__file__).resolve().parent / "data" / "roles.yaml"


def _ro(m) -> Mapping:
    return MappingProxyType(dict(m or {}))


def _load_roles(path: Path) -> Mapping:
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    fams = tuple(doc["families"])
    roles = {}
    for name, entry in doc["roles"].items():
        check_in(f"role {name} family", entry["family"], fams)
        roles[name] = MappingProxyType(dict(entry))
    return MappingProxyType({"families": fams, "roles": MappingProxyType(roles),
                             "order": MappingProxyType({k: tuple(tuple(x) if isinstance(x, list) else x for x in v)
                                                        for k, v in doc["order"].items()}),
                             "interfaces": MappingProxyType({k: MappingProxyType(v)
                                                             for k, v in doc["interfaces"].items()})})


#: The role registry, read once at import and immutable afterwards (D-A2-3).
ROLES = _load_roles(ROLES_PATH)


def family(role: str) -> str:
    return ROLES["roles"][role]["family"]


@dataclass(frozen=True)
class Declared:
    """A declared value with its provenance (D-A7-3 shapes). `value` is a float, a bool, a string, or — for a
    component record — a read-only mapping. `band` (lo, hi) or `uncertainty` + `uncertainty_basis` feed the
    parameter band (R-STEP0-12)."""
    value: object
    unit: str | None = None
    grade: str | None = None
    source: str | None = None
    counter_evidence_searched: str | None = None
    note: str | None = None
    band: tuple | None = None
    uncertainty: float | None = None
    uncertainty_basis: str | None = None

    def __post_init__(self):
        if isinstance(self.value, Mapping):
            object.__setattr__(self, "value", _ro(self.value))
        elif isinstance(self.value, float):
            check_finite("Declared.value", self.value)
        if self.band is not None:
            lo, hi = self.band
            check_finite("Declared.band lo", lo)
            check_finite("Declared.band hi", hi)
            if lo > hi:
                raise ValueError(f"Declared.band lo {lo!r} > hi {hi!r}")
        if self.uncertainty is not None:
            check_finite("Declared.uncertainty", self.uncertainty)
            check_in("Declared.uncertainty_basis", self.uncertainty_basis, UNCERTAINTY_BASES)


@dataclass(frozen=True)
class Extent:
    """A layer's boundary rule (§A1.3). `value` is a mass fraction or a radius/depth in m; `ref` is the event name
    for `phase` and the lower layer's id for `thickness_above`."""
    kind: str
    value: float | None = None
    ref: str | None = None

    def __post_init__(self):
        check_in("Extent.kind", self.kind, EXTENT_KINDS)
        if self.kind == "phase":
            if not self.ref:
                raise ValueError("Extent(phase) needs the event name in ref")
        else:
            check_finite(f"Extent({self.kind}).value", self.value)
            if self.value < 0:
                raise ValueError(f"Extent({self.kind}).value {self.value!r} < 0")
        if self.kind == "thickness_above" and not self.ref:
            raise ValueError("Extent(thickness_above) needs the lower layer id in ref")


@dataclass(frozen=True)
class Layer:
    """One layer (D-A2-2). Field names follow R-LAYERGEN-1 where it named them (`name` → `id`, `size` → `extent`)."""
    id: str
    role: str
    material: str
    extent: Extent | None = None          # None: the one layer that takes the rest of the mass
    thermal: str = "adiabatic"
    t_declared: float | None = None       # for `isothermal`
    system: str | None = None             # composition system (R-LAYERGEN-1); required with `composition`
    composition: Declared | None = None
    params: Mapping = field(default_factory=dict)   # name → Declared

    def __post_init__(self):
        if not self.id:
            raise ValueError("Layer.id is empty")
        if self.role not in ROLES["roles"]:
            raise ValueError(f"Layer({self.id}).role {self.role!r} is not in the role registry")
        check_in(f"Layer({self.id}).thermal", self.thermal, THERMAL_KINDS)
        if (self.thermal == "isothermal") != (self.t_declared is not None):
            raise ValueError(f"Layer({self.id}): t_declared goes with thermal 'isothermal' and only with it")
        if self.t_declared is not None:
            check_finite(f"Layer({self.id}).t_declared", self.t_declared)
        if self.composition is not None and not self.system:
            raise ValueError(f"Layer({self.id}): composition needs a system")
        object.__setattr__(self, "params", _ro(self.params))


@dataclass(frozen=True)
class SurfaceState:
    """§A1.2. `p_s` is None while `p_s_source` is «material_floor»: the solve reads the outer material's p_floor."""
    m: float                      # kg
    p_s: float | None = None      # Pa
    p_s_source: str = "material_floor"
    t_s: float | None = None      # K; read only by a conductive layer
    t_pot: float | None = None    # K

    def __post_init__(self):
        check_finite("SurfaceState.m", self.m)
        if self.m <= 0:
            raise ValueError(f"SurfaceState.m {self.m!r} <= 0")
        check_in("SurfaceState.p_s_source", self.p_s_source, P_S_SOURCES)
        if (self.p_s_source == "declared") != (self.p_s is not None):
            raise ValueError("SurfaceState.p_s is given exactly when p_s_source is 'declared'")
        for k in ("p_s", "t_s", "t_pot"):
            v = getattr(self, k)
            if v is not None:
                check_finite(f"SurfaceState.{k}", v)


@dataclass(frozen=True)
class Closure:
    """The body's one free scalar (D-A2-8, §X2): `kind`, the layer it acts on, the axis name, and the scan range."""
    kind: str
    lo: float
    hi: float
    layer: str | None = None
    name: str | None = None

    def __post_init__(self):
        check_in("Closure.kind", self.kind, CLOSURE_KINDS)
        check_finite("Closure.lo", self.lo)
        check_finite("Closure.hi", self.hi)
        if not self.lo < self.hi:
            raise ValueError(f"Closure range [{self.lo!r}, {self.hi!r}] is empty")
        if self.kind == "R" and (self.layer or self.name):
            raise ValueError("Closure(R) takes no layer and no name")
        if self.kind == "boundary_mass" and (not self.layer or self.name):
            raise ValueError("Closure(boundary_mass) takes a layer and no name")
        if self.kind == "composition" and not (self.layer and self.name):
            raise ValueError("Closure(composition) takes a layer and an axis name")


@dataclass(frozen=True)
class Boundary:
    """A boundary derived from the list (D-A2-3): `name` is «lower id/upper id» (R-LAYERGEN-5); `interface` is a
    named interface (`cmb`, `icb`) when the role registry gives one."""
    lower: str
    upper: str
    roles: tuple
    name: str
    interface: str | None = None


def derive_boundaries(layers: tuple) -> tuple:
    """Boundaries between neighbours, with named interfaces found by role (never by stack index)."""
    rules = ROLES["interfaces"]
    out = []
    for a, b in zip(layers, layers[1:]):
        named = None
        for iname, rule in rules.items():
            if "below_role" in rule and a.role == rule["below_role"] and b.role == rule["above_role"]:
                named = iname
            elif "below_family" in rule and family(a.role) == rule["below_family"] \
                    and family(b.role) != rule["above_not_family"]:
                named = iname
        out.append(Boundary(a.id, b.id, (a.role, b.role), f"{a.id}/{b.id}", named))
    return tuple(out)


def order_violations(layers: tuple) -> list:
    """Each (pair text, rule text) the list breaks under the role registry's order rules (D-A2-3, R-LAYERGEN-2).
    Empty when the order is valid; `validate` turns each into a named refusal."""
    order = ROLES["order"]
    fams = [family(l.role) for l in layers]
    bad = []
    for fam in order.get("centre_contiguous", ()):
        idx = [i for i, f in enumerate(fams) if f == fam]
        if idx and idx != list(range(len(idx))):
            bad.append((", ".join(layers[i].id for i in idx), f"'{fam}' layers are contiguous at the centre"))
    for fam in order.get("outermost", ()):
        first = next((i for i, f in enumerate(fams) if f == fam), None)
        if first is not None:
            for i in range(first, len(fams)):
                if fams[i] != fam:
                    bad.append((f"{layers[first].id} < {layers[i].id}",
                                f"only '{fam}' layers may follow a '{fam}' layer"))
    for lo_role, hi_role in order.get("below", ()):
        lo = [i for i, l in enumerate(layers) if l.role == lo_role]
        hi = [i for i, l in enumerate(layers) if l.role == hi_role]
        if lo and hi and max(lo) > min(hi):
            bad.append((f"{layers[max(lo)].id} / {layers[min(hi)].id}", f"'{lo_role}' lies below '{hi_role}'"))
    return bad


@dataclass(frozen=True)
class Body:
    """A validated body (D-A2-1). SI units throughout; `radius` is an observation, never a forward-mode input."""
    name: str
    kind: str
    surface: SurfaceState
    layers: tuple
    closure: Closure
    parent: str | None = None
    radius: Declared | None = None                  # m
    jumps: Mapping = field(default_factory=dict)    # boundary name → Declared (K, inner side hotter)
    declarations: Mapping = field(default_factory=dict)   # body-wide: age, regime, radiogenic, thermal block, …
    solver_flags: Mapping = field(default_factory=dict)   # solver keys outside the layer list, e.g. tidal_heating
    later_tools: Mapping = field(default_factory=dict)    # carried through, never read by the solver (D-A2-7)
    notes: tuple = ()                               # typed notes, e.g. from_v1 normalisations
    boundaries: tuple = field(init=False)

    def __post_init__(self):
        if not self.layers:
            raise ValueError(f"Body({self.name}) has no layers")
        ids = [l.id for l in self.layers]
        if len(set(ids)) != len(ids):
            raise ValueError(f"Body({self.name}) repeats a layer id: {ids}")
        if sum(l.extent is None for l in self.layers) > 1:
            raise ValueError(f"Body({self.name}) has more than one layer without an extent")
        bad = order_violations(self.layers)
        if bad:
            raise ValueError(f"Body({self.name}) layer order: {bad}")
        if self.closure.layer is not None and self.closure.layer not in ids:
            raise ValueError(f"Body({self.name}) closure names unknown layer {self.closure.layer!r}")
        object.__setattr__(self, "layers", tuple(self.layers))
        object.__setattr__(self, "boundaries", derive_boundaries(self.layers))
        names = {b.name for b in self.boundaries} | {b.interface for b in self.boundaries if b.interface}
        for j in self.jumps:
            if j not in names:
                raise ValueError(f"Body({self.name}) jump at unknown boundary {j!r}")
        for k in ("jumps", "declarations", "solver_flags", "later_tools"):
            object.__setattr__(self, k, _ro(getattr(self, k)))

    def interface(self, name: str) -> Boundary | None:
        """The named interface (`cmb`, `icb`), looked up by role (W-L15-02)."""
        hits = [b for b in self.boundaries if b.interface == name]
        return hits[0] if hits else None

    @property
    def mass(self) -> float:
        return self.surface.m
