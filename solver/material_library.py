# 라이브러리 형식 어댑터 — 설치된 SeaFreeze 를 고정(버전 · 트리 해시)으로 확인하고 상태를 SI 로 돌려준다 (phase-2 impl note 1 §6, P3)
"""The library-form adapter (rewrite/phase2-impl.frozen.md note 1 §6, owner db20e171 (b): call the pinned installed
library at runtime; no SeaFreeze code or derived tables in the repo).

Pin, checked at load for a record with a library-form phase (a mismatch makes that record unavailable, not the
registry):
- `library.version` equals the installed distribution's version (importlib.metadata);
- `library.sha256` equals `tree_sha256(name)`: sha256 over every file under the installed package directory except
  __pycache__, in sorted order of the POSIX relative path; per file the bytes fed are
  relpath (UTF-8) · b"\\0" · file bytes · b"\\0". The whole tree is hashed (all splines, used or not): the pin is the
  package. The PyPI sdist sha256 stays in the record as the cite; it is enforced at install time.

`SeaFreezePhase(submodel)` evaluates one SeaFreeze phase at (P [Pa], T [K]): ρ [kg/m³], α [1/K], c_P [J/kg/K],
K_T [Pa], and (dT/dP)_S = αT/(ρ c_P) [K/Pa]. getProp takes P in MPa and returns K in MPa; the conversion is here,
and (dT/dP)_S is checked against SeaFreeze's own Js [K/MPa] at every evaluation. A (P, T) outside the submodel's knot
box (seafreeze.phaselines.phase_range) is out of range before getProp is called: SeaFreeze silences its own
«outside the knot sequence» warning, so that warning is not relied on (68 N34).
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

#: Submodels a record may name (impl P6: liquid and Ih/II/III/V/VI). VII_X_French is not a record submodel
#: (directing, 2026-10-11); a test reaches it through `SeaFreezePhase(…, test_only=True)`.
RECORD_SUBMODELS = ("water1", "Ih", "II", "III", "V", "VI")
TEST_ONLY_SUBMODELS = ("VII_X_French",)
PACKAGES = MappingProxyType({"SeaFreeze": "seafreeze"})       # distribution name → import package


@dataclass(frozen=True)
class PinStop:
    why: str


def tree_sha256(distribution: str) -> str | PinStop:
    """The installed package tree's sha256 (framing in the module docstring)."""
    pkg = PACKAGES.get(distribution)
    spec = importlib.util.find_spec(pkg) if pkg else None
    if spec is None or spec.origin is None:
        return PinStop(f"{distribution} is not installed")
    root = Path(spec.origin).parent
    h = hashlib.sha256()
    for f in sorted((p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts),
                    key=lambda p: p.relative_to(root).as_posix()):
        h.update(f.relative_to(root).as_posix().encode("utf-8"))
        h.update(b"\0")
        h.update(f.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def check_pin(library, tree_sha: str | PinStop | None = None) -> PinStop | None:
    """None when the installed library matches the record's pin; else why not. `tree_sha` may be passed in when the
    caller has computed it already (the registry does it once per load)."""
    name = library["name"]
    if name not in PACKAGES:
        return PinStop(f"library {name!r} has no adapter ({sorted(PACKAGES)})")
    if library["submodel"] not in RECORD_SUBMODELS:
        return PinStop(f"submodel {library['submodel']!r} is not one a record may name {list(RECORD_SUBMODELS)}")
    try:
        got = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return PinStop(f"{name} is not installed")
    if got != library["version"]:
        return PinStop(f"{name} {got} installed, the record pins {library['version']}")
    sha = tree_sha256(name) if tree_sha is None else tree_sha
    if isinstance(sha, PinStop):
        return sha
    if sha != library["sha256"]:
        return PinStop(f"{name} tree sha256 {sha[:12]}… differs from the pinned {library['sha256'][:12]}…")
    return None


class LibraryOutOfRange(Exception):
    """The library could not answer at (P, T): it raised, or returned a non-finite value (68 N28)."""


class SeaFreezePhase:
    """One SeaFreeze phase at (P [Pa], T [K]), in SI."""

    JS_RTOL = 1e-9          # αT/(ρc_P) against SeaFreeze's Js: the same quantity, so only float rounding separates them

    def __init__(self, submodel: str, test_only: bool = False):
        allowed = RECORD_SUBMODELS + (TEST_ONLY_SUBMODELS if test_only else ())
        if submodel not in allowed:
            raise ValueError(f"submodel {submodel!r} not in {list(allowed)}")
        self.submodel = submodel

    def at(self, p: float, t: float) -> dict:
        import numpy as np
        from seafreeze.phaselines import phase_range  # 68 N34: the spline's knot box, checked before evaluation
        from seafreeze.seafreeze import getProp       # 68 N33: an ImportError is its own error, never «out of data»
        rng = phase_range(self.submodel)
        if not (rng.P[0] <= p / 1e6 <= rng.P[1] and rng.T[0] <= t <= rng.T[1]):
            raise LibraryOutOfRange(f"{self.submodel} at ({p:g} Pa, {t:g} K): outside the spline's knot box "
                                    f"P {rng.P} MPa × T {rng.T} K")
        pt = np.empty((1,), dtype=object)
        pt[0] = (p / 1e6, t)
        try:
            o = getProp(pt, self.submodel)

            def one(name):
                x = float(np.ravel(getattr(o, name))[0])
                if not np.isfinite(x):
                    raise ValueError(f"{name} is not finite")
                return x
            rho, alpha, cp = one("rho"), one("alpha"), one("Cp")
            kt, js, gibbs = one("Kt"), one("Js"), one("G")
        except (ImportError, ModuleNotFoundError):
            raise
        except Exception as e:                      # 68 N28: whatever SeaFreeze raises becomes one named outcome
            raise LibraryOutOfRange(f"{self.submodel} at ({p:g} Pa, {t:g} K): {type(e).__name__}: {e}") from e
        dtdp = alpha * t / (rho * cp)
        js = js * 1e-6
        if abs(dtdp - js) > self.JS_RTOL * abs(js):
            raise ValueError(f"{self.submodel} at ({p:g} Pa, {t:g} K): αT/(ρc_P) {dtdp:.6e} vs Js {js:.6e}")
        return {"rho": rho, "alpha": alpha, "c_p": cp, "k_t": kt * 1e6, "dtdp": dtdp, "g": gibbs}
