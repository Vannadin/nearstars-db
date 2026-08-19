# J2 섭동의 C 구현 로더 — 파이썬 콜백(j2.py)과 같은 식을, 매 스텝 파이썬을 거치지 않고.
"""Load the compiled J2 force and hand REBOUND its function pointer.

`j2.py` installs the same force as a Python callable, which REBOUND then calls once per
timestep: at a 10-minute step a 10^5 yr run is 5.26e9 crossings of the Python boundary,
and that costs about 69x the integration itself (measured on the α Cen moon system:
2.7 yr/s with the callback against 186 yr/s without). The formula is unchanged — this is
the same expression compiled.

Robustness note: C is given the ADDRESS OF the simulation's particles pointer, not the
pointer itself, so a reallocation (init_megno adds variational particles after the force
is installed) cannot leave it reading freed memory.

Falls back to the Python implementation when the library is missing or will not build,
so a machine without a compiler still runs — slowly, but with identical physics.

STATUS — NOT ENABLED. Opt in with STAB_J2_C=1; `j2.py` uses the Python callback
otherwise. One bug is known and located: `struct particle_head` in j2force.c declares
only the leading 10 doubles (80 bytes) while rebound's `reb_particle` is 112, so
indexing `ps[i]` walks with the wrong stride and segfaults. The fix is to stop
hardcoding the layout — pass `ctypes.sizeof(rebound.Particle)` into ns_j2_setup and
index by bytes — which also keeps it correct if the struct grows in a later rebound.
After that, cross-check against the Python force before trusting it: integrate both a
couple of years from the same state and compare a/e/inc per moon.
"""
from __future__ import annotations

import ctypes
import math
import subprocess
import sys
from pathlib import Path

import rebound

HERE = Path(__file__).resolve().parent
SRC = HERE / "j2force.c"
LIB = HERE / ("libnsj2.dylib" if sys.platform == "darwin" else "libnsj2.so")


def _load():
    if not LIB.exists() or LIB.stat().st_mtime < SRC.stat().st_mtime:
        try:
            subprocess.run(["cc", "-O3", "-fPIC", "-shared", "-o", str(LIB), str(SRC)],
                           check=True, capture_output=True)
        except Exception as e:                       # no compiler, or it refused
            print(f"[warn] J2 C force unavailable ({e}); using the Python callback",
                  file=sys.stderr)
            return None
    lib = ctypes.CDLL(str(LIB))
    lib.ns_j2_setup.argtypes = [ctypes.c_double] * 6 + [
        ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_int]
    lib.ns_j2_bind.argtypes = [ctypes.c_void_p]
    return lib


def install(sim: rebound.Simulation, body_index: int, moon_idx: list[int],
            axis: tuple[float, float, float], j2: float, r_eq_au: float):
    """Set sim.additional_forces to the compiled force. Returns False to fall back."""
    lib = _load()
    if lib is None:
        return False
    arr = (ctypes.c_int * len(moon_idx))(*moon_idx)
    lib.ns_j2_setup(ctypes.c_double(axis[0]), ctypes.c_double(axis[1]),
                    ctypes.c_double(axis[2]), ctypes.c_double(j2),
                    ctypes.c_double(r_eq_au), ctypes.c_double(sim.G),
                    ctypes.c_int(body_index), arr, ctypes.c_int(len(moon_idx)))
    lib.ns_j2_bind(ctypes.c_void_p(
        ctypes.addressof(sim) + rebound.Simulation._particles.offset))
    # rebound casts whatever it is given through AFF = CFUNCTYPE(None, POINTER(Simulation));
    # handing it the raw symbol keeps the call entirely inside C.
    sim.additional_forces = ctypes.cast(lib.ns_j2_force, rebound.simulation.AFF)
    sim.force_is_velocity_dependent = 0
    return True
