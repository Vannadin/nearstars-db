# 원소·물질·프리셋 덩어리(bulk:)를 층 계획으로 나누는 순수 함수 — 상태 없음, 풀이 없음, validate 가 부른다 (layers S0·S1)
"""`partition(bulk, params) -> LayerPlan | Refusal` (layers S0 registration f298b628, S1 1346ffc6; design 7a5c34ab §3–§4).

Three forms of the `bulk:` block:
- (M) `{"materials": [{material, mass_fraction, composition?}]}`: ordered by role (bulk.yaml `material_roles`); the
  last role carries no extent, so earth_like written out equals presets.yaml's expansion.
- (E) `{"elements": {symbol: value | {value, sigma?}}, "source_kind", "grade", "source", "counter_evidence_searched"}`,
  mass fractions summing to 1. `params`: `fe_metal_fraction` (default 0.8625, Wang+ 2018) and `core_material`
  (`fe_prem` default, or `fe_core_light` with `core_light: {S, O, C}` as the core's mass fractions).
- (P) `{"preset": name}`: presets.yaml's layer list, as from_v1 expands it today.

(E) steps (registration §2.2):
1. The core is drawn from the bulk. core Fe = fe_metal_fraction × bulk Fe. With fe_prem the core composition is
   Wang Table 1's core column renormalised over the elements the bulk declares; the core mass = core Fe / x_Fe, and
   x_i × core mass is subtracted from the bulk for every i the core lists. A shortfall refuses
   `input.bulk_core_draw_short` (no clipping). 68 n1: the same x_Fe turns a fitted core mass back into core Fe at S1:
   implied core Fe = x_Fe × fitted core mass; the Fe-budget misfit = that − fe_metal_fraction × bulk Fe. The plan
   carries x_Fe for that.
2. The silicate is what the bulk keeps: the twelve MS95 oxides from each element's remainder (FeO from the remaining
   Fe), CFMASNa normalised as the records are; the other oxides are dropped, in wt %; every other element stays
   unoxidised in the dropped list with its mass (remaining S, C, …).
3. O: O_needed = the stoichiometric O of all mantle oxides. A declared O is checked against the remaining O:
   Δ = O_needed − O_remaining, σ_Δ from the stated ± of O and of Fe, Mg, Si, Ca, Al, Na (Δ is linear in each, so
   the derivative is a difference), |Δ| ≤ 3 σ_Δ, else `input.bulk_oxygen_short` (Δ > 0) or `…_excess`. No stated O
   ± → Wang's bulk-O relative 2.27 %, labelled. An undeclared O is computed (= O_needed, Δ = 0).
4. H2O > 0 → a volatile layer marked «refused at S1 (no ice/ocean integration)», with its mass.
5. The residual (68 n2): total − (core + mantle oxides + dropped + volatile − Δ), Δ signed as above.

68 n3: no closure is set here. (b2), boundary_mass on the core fitted to the radius, is S1's; Venus's row
(from_v1.py:165) is today's use of that closure kind, not earth_like's.

S1 (1346ffc6): the vocabulary is schema.yaml's `bulk:` section (S0's bulk.yaml, moved verbatim); every refusal goes
through `refusals.make` (the seven `input.bulk_*` ids are registered, §3); fe_core_light's core_light is range-checked
(`input.bulk_core_light`, LAYERS-S1-NOTES n2); `fe_budget_misfit` is the (b2) misfit run_oracle records (§2.5).
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from solver import refusals as rf
from solver.material_assemblage import CFMASNA, cfmasna
from solver.result import freeze
from solver.yamlio import load_data

BULK = load_data(Path(__file__).resolve().parent / "data" / "schema.yaml")["bulk"]
PRESETS_PATH = Path(__file__).resolve().parent / "data" / "presets.yaml"
UNIT_SCALE = freeze({"%": 1e-2, "ppm": 1e-6, "ppb": 1e-9})
TRIO = ("grade", "source", "counter_evidence_searched")
CORE_MATERIALS = ("fe_prem", "fe_core_light")


@dataclass(frozen=True)
class LayerPlan:
    """The partition's output. `layers` is a v2 layer list (S1 joins it to the solver); `ledger` holds every mass
    the residual sums; `disclosures` are sentences with their data; `o_check` and `volatile` are None when absent."""
    form: str
    layers: tuple
    core_mass_fraction: float | None
    ledger: Mapping
    disclosures: tuple
    o_check: Mapping | None
    volatile: Mapping | None
    residual: float

    def __post_init__(self):
        for f in ("layers", "ledger", "disclosures", "o_check", "volatile"):
            object.__setattr__(self, f, freeze(getattr(self, f)))


class _Refuse(Exception):
    def __init__(self, r):
        super().__init__(r.id)
        self.refusal = r


def _no(id_, where, _text, **ev):
    """A registered refusal (S1 §3). `_text` is S0's inline sentence, kept beside the call as a reading aid; the
    refusal's text is the registry's template."""
    raise _Refuse(rf.make(id_, where, **ev))


def _val(x):
    return x.get("value") if isinstance(x, Mapping) else x


def _sigma(x):
    return x.get("sigma") if isinstance(x, Mapping) else None


def _num(x, key, where):
    v = _val(x)
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        _no("input.not_number", where, f"키 '{key}' 의 값 {v!r} 이(가) 유한한 수가 아니다", key=key, got=repr(v))
    return float(v)


def _printed(s):
    v, unit = s.split()
    return float(v) * UNIT_SCALE[unit]


def partition(bulk, params=None, where: str = "<bulk>"):
    """A `bulk:` block → `LayerPlan`, or a `Refusal`. Pure: reads only bulk.yaml (at import) and presets.yaml."""
    try:
        return _partition(bulk, params or {}, where)
    except _Refuse as r:
        return r.refusal


def _partition(bulk, params, where):
    if not isinstance(bulk, Mapping):
        _no("input.not_mapping", where, f"bulk 블록이 사전이 아니라 {type(bulk).__name__} 이다", path=where,
            got_type=type(bulk).__name__)
    forms = [f for f in BULK["forms"] if f in bulk]
    if len(forms) != 1:
        _no("input.not_in_vocabulary", where, f"bulk 블록의 꼴은 {list(BULK['forms'])} 중 하나여야 한다 — {sorted(bulk)}",
            key="bulk", got=sorted(bulk), allowed=list(BULK["forms"]))
    return {"materials": _materials, "elements": _elements, "preset": _preset}[forms[0]](bulk, params, where)


# ── (M) and (P) ──────────────────────────────────────────────────────────────────────────────────────────────────
def _materials(bulk, params, where):
    items = bulk["materials"]
    roles = BULK["material_roles"]
    order = list(BULK["role_order"])
    fracs = []
    for i, it in enumerate(items):
        m = it.get("material") if isinstance(it, Mapping) else None
        if m not in roles:
            _no("input.not_in_vocabulary", f"{where}:materials[{i}]", f"물질 '{m}' 이(가) bulk 물질 목록 밖이다",
                key=f"materials[{i}].material", got=m, allowed=sorted(roles))
        f = _num(it.get("mass_fraction"), f"materials[{i}].mass_fraction", where)
        if not 0.0 <= f <= 1.0:
            _no("input.bulk_fractions", where, f"질량 몫 {f} 이(가) [0, 1] 밖이다", total=None, item=i, value=f)
        fracs.append(f)
    total = math.fsum(fracs)
    if abs(total - 1.0) > BULK["fractions_tol"]:
        _no("input.bulk_fractions", where, f"질량 몫의 합 {total!r} 이(가) 1 에서 {BULK['fractions_tol']} 보다 멀다",
            total=total, item=None, value=None)
    ranked = sorted(range(len(items)), key=lambda i: order.index(roles[items[i]["material"]]))
    last = ranked[-1]
    layers = []
    for i in ranked:
        it = items[i]
        role = roles[it["material"]]
        lay = {"id": role, "role": role, "material": it["material"]}
        if i != last:
            lay["extent"] = {"mass_fraction": fracs[i]}
        if "composition" in it:
            lay["composition"] = it["composition"]
        layers.append(lay)
    core = [fracs[i] for i in ranked if roles[items[i]["material"]] == "core"]
    return LayerPlan(form="materials", layers=layers, core_mass_fraction=math.fsum(core) if core else None,
                     ledger={"materials": {items[i]["material"]: fracs[i] for i in ranked}}, disclosures=(),
                     o_check=None, volatile=None, residual=1.0 - total)


def _preset(bulk, params, where):
    presets = load_data(PRESETS_PATH)
    name = bulk["preset"]
    if name not in presets or name == "not_expanded" or "layers" not in presets[name]:
        _no("input.not_in_vocabulary", where, f"프리셋 '{name}' 의 층 목록이 없다", key="preset", got=name,
            allowed=sorted(k for k in presets if k != "not_expanded"))
    layers = presets[name]["layers"]
    core = [l["extent"]["mass_fraction"] for l in layers if l["role"] == "core" and "extent" in l]
    return LayerPlan(form="preset", layers=layers, core_mass_fraction=math.fsum(core) if core else None,
                     ledger={"preset": name}, disclosures=(), o_check=None, volatile=None, residual=0.0)


# ── (E) ──────────────────────────────────────────────────────────────────────────────────────────────────────────
def _core_composition(bulk_el, params, where):
    """The core's mass fractions over the elements it holds, and the disclosures of the renormalisation."""
    mat = params.get("core_material", "fe_prem")
    if mat not in CORE_MATERIALS:
        _no("input.not_in_vocabulary", where, f"핵 물질 '{mat}' 은(는) {list(CORE_MATERIALS)} 밖이다",
            key="params.core_material", got=mat, allowed=list(CORE_MATERIALS))
    if mat == "fe_core_light":
        light = params.get("core_light") or {}
        x = {k: _num(v, f"params.core_light.{k}", where) for k, v in light.items()}
        for k in x:
            if k not in ("S", "O", "C"):
                _no("input.not_in_vocabulary", where, f"fe_core_light 의 가벼운 원소 '{k}' 는 S, O, C 밖이다",
                    key=f"params.core_light.{k}", got=k, allowed=["S", "O", "C"])
        tot = math.fsum(x.values())
        if tot >= 1.0 or any(v < 0.0 for v in x.values()):
            _no("input.bulk_core_light", where, "", S=x.get("S"), O=x.get("O"), C=x.get("C"), total=tot)
        x["Fe"] = 1.0 - tot
        return mat, x, [{"text": "core composition declared on fe_core_light: Fe = 1 − (S + O + C)",
                         "data": dict(x)}]
    printed = {k: _printed(v) for k, v in BULK["fe_prem_core_printed"].items()}
    held = {k: v for k, v in printed.items() if k in bulk_el}
    s_all, s_held = math.fsum(printed.values()), math.fsum(held.values())
    x = {k: v / s_held for k, v in held.items()}
    undeclared = sorted(set(printed) - set(held))
    return mat, x, [{"text": "fe_prem core composition: Wang+ 2018 Table 1 core column, renormalised over the declared "
                             "elements", "data": {"column_sum": s_all, "declared_sum": s_held,
                                                  "factor": s_all / s_held,
                                                  "undeclared": undeclared,
                                                  "undeclared_share_of_column": (s_all - s_held) / s_all}}]


def _mantle_oxygen(rem, mass):
    """O_needed and the oxide masses (g per unit bulk) of the remaining elements."""
    ox = {}
    for el, (name, n_cat, n_o) in BULK["oxides"].items():
        m = rem.get(el, 0.0)
        if m:
            ox[name] = (m, m / (n_cat * mass[el]) * n_o * mass["O"])
    return ox


def _elements(bulk, params, where):
    el = bulk["elements"]
    if not isinstance(el, Mapping) or not el:
        _no("input.not_mapping", where, "elements 가 비었거나 사전이 아니다", path=f"{where}:elements",
            got_type=type(el).__name__)
    vocab = set(BULK["elements"]) | set(BULK["volatiles"])
    for k in el:
        if k not in vocab:
            _no("input.not_in_vocabulary", f"{where}:elements", f"원소 '{k}' 이(가) bulk 어휘 밖이다",
                key=f"elements.{k}", got=k, allowed=list(BULK["elements"]) + list(BULK["volatiles"]))
    missing = [f for f in ("source_kind",) + TRIO if not bulk.get(f)]
    if missing:
        _no("input.provenance_missing", where, f"bulk 블록의 출처 칸 {missing} 이(가) 비었다", key="bulk",
            fields=missing)
    if "Fe" not in el:
        _no("input.missing_key", where, "필요한 키 'elements.Fe' 가 없다", key="elements.Fe")
    vals = {k: _num(v, f"elements.{k}", where) for k, v in el.items()}
    for k, v in vals.items():
        if v < 0.0:
            _no("input.bulk_fractions", where, f"원소 '{k}' 의 몫 {v} 이(가) 음수다", total=None, item=k, value=v)
    dflt = BULK["defaults"]
    f_metal = _num(params.get("fe_metal_fraction", dflt["fe_metal_fraction"]["value"]), "params.fe_metal_fraction",
                   where)
    disclosures = []
    if "fe_metal_fraction" not in params:
        disclosures.append({"text": "fe_metal_fraction default 0.8625 ± 0.042 — " + dflt["fe_metal_fraction"]["grade"],
                            "data": {"value": f_metal, "source": dflt["fe_metal_fraction"]["source"]}})

    def run(v, f):
        """Steps 1–3 on element values v: (core, rem, oxides, dropped, o_needed, o_rem, x)."""
        mat, x, disc = _core_composition(v, params, where)
        core_mass = f * v["Fe"] / x["Fe"]
        core = {k: xi * core_mass for k, xi in x.items()}
        rem = {}
        for k, m in v.items():
            d = m - core.get(k, 0.0)
            if d < 0.0:
                _no("input.bulk_core_draw_short", where,
                    f"핵이 원소 '{k}' 를 {core[k]!r} 만큼 가져가야 하는데 덩어리에 {m!r} 뿐이다 (핵 질량 {core_mass!r})",
                    element=k, bulk=m, core_draw=core[k], core_mass=core_mass)
            rem[k] = d
        for k in x:
            if k not in v:
                _no("input.bulk_core_draw_short", where, f"핵이 원소 '{k}' 를 가져가야 하는데 덩어리에 없다",
                    element=k, bulk=0.0, core_draw=core[k], core_mass=core_mass)
        mass = BULK["atomic_mass_g_mol"]
        ox = _mantle_oxygen(rem, mass)
        o_needed = math.fsum(o for _m, o in ox.values())
        return mat, x, disc, core_mass, core, rem, ox, o_needed

    mat, x, disc, core_mass, core, rem, ox, o_needed = run(vals, f_metal)
    disclosures += disc
    o_declared = "O" in vals
    o_rem = rem.get("O", 0.0) if o_declared else o_needed
    delta = o_needed - o_rem
    total = math.fsum(vals.values()) + (0.0 if o_declared else o_needed)
    if abs(total - 1.0) > BULK["fractions_tol"]:
        _no("input.bulk_fractions", where, f"원소 몫의 합 {total!r} 이(가) 1 에서 {BULK['fractions_tol']} 보다 멀다",
            total=total, item=None, value=None)
    o_check = None
    if o_declared:
        s_o = _sigma(el["O"])
        label = "stated"
        if s_o is None:
            s_o = vals["O"] * dflt["o_relative_sigma"]["value"]
            label = dflt["o_relative_sigma"]["grade"]
        terms = {"O": s_o}           # dΔ/dO_bulk = −1 (the core's O draw does not depend on bulk O)
        no_sigma = []
        for k in BULK["o_check_elements"]:
            if k not in vals:
                continue
            s = _sigma(el[k])
            if s is None:
                no_sigma.append(k)
                continue
            h = vals[k] * 1e-6 or 1e-12
            v2 = dict(vals)
            v2[k] = vals[k] + h
            _m, _x, _d, _cm, _c, rem2, _ox, need2 = run(v2, f_metal)
            d2 = need2 - (rem2.get("O", 0.0))
            terms[k] = (d2 - delta) / h * float(s)
        sigma_d = math.sqrt(math.fsum(t * t for t in terms.values()))
        o_check = {"o_needed": o_needed, "o_remaining": o_rem, "delta": delta, "sigma_delta": sigma_d,
                   "n_sigma": BULK["o_check_sigmas"], "sigma_o": s_o, "sigma_o_source": label, "terms": terms,
                   "no_stated_sigma": no_sigma}
        if abs(delta) > BULK["o_check_sigmas"] * sigma_d:
            rid = "input.bulk_oxygen_short" if delta > 0 else "input.bulk_oxygen_excess"
            _no(rid, where, f"선언 O {o_rem!r} 이(가) 산화물에 필요한 O {o_needed!r} 와 {delta!r} 차이 — "
                f"허용 {BULK['o_check_sigmas']}σ_Δ = {BULK['o_check_sigmas'] * sigma_d!r} (σ_O 출처: {label})",
                o_needed=o_needed, o_remaining=o_rem, delta=delta, sigma_delta=sigma_d, sigma_o_source=label)
        if label != "stated":
            disclosures.append({"text": f"O check width: {label}", "data": {"sigma_o": s_o}})
        if no_sigma:
            disclosures.append({"text": "no stated ± for these O-setting elements; they add nothing to σ_Δ",
                                "data": {"elements": no_sigma}})
    else:
        disclosures.append({"text": "O not declared: computed as the mantle oxides' stoichiometric O",
                            "data": {"o_needed": o_needed}})

    oxide_mass = {name: m + o for name, (m, o) in ox.items()}
    oxide_el = {name: el_ for el_, (name, _c, _o) in BULK["oxides"].items()}
    skip = {"O"} | {oxide_el[n] for n in oxide_mass} | set(BULK["volatiles"])
    elemental = {k: m for k, m in rem.items() if k not in skip and m}
    h2o = vals.get("H2O", 0.0)
    volatile = None
    if h2o > BULK["volatile_threshold"]:
        volatile = {"H2O": h2o, "status": "refused at S1 (no ice/ocean integration)"}
    mantle_mass = math.fsum(oxide_mass.values()) + math.fsum(elemental.values())
    oxides_wt = {n: 100.0 * m / mantle_mass for n, m in oxide_mass.items()}
    cf = cfmasna({k: oxides_wt.get(k, 0.0) for k in CFMASNA})
    dropped_wt = {n: w for n, w in oxides_wt.items() if n not in CFMASNA}
    dropped_wt.update({k: 100.0 * m / mantle_mass for k, m in elemental.items()})
    core_total = math.fsum(core.values())
    residual = total - math.fsum([core_total, math.fsum(oxide_mass.values()), math.fsum(elemental.values()), h2o,
                                  -delta])
    ni_share = core.get("Ni", 0.0) / vals["Ni"] if vals.get("Ni") else None
    if "Ni" in core:
        disclosures.append({"text": "Ni in the core is mass only: neither fe_prem nor iron_alloy has a Ni slot",
                            "data": {"core_Ni": core["Ni"], "core_share_of_bulk_Ni": ni_share}})
    layers = [{"id": "core", "role": "core", "material": mat, "extent": {"mass_fraction": core_total}},
              {"id": "mantle", "role": "mantle", "material": "silicate_decl", "system": "silicate",
               "composition": {"oxides_wt": cf, "dropped_wt": dropped_wt, "source_kind": bulk["source_kind"],
                               **{t: bulk[t] for t in TRIO}}}]
    if volatile:
        layers.append({"id": "volatile", "role": "volatile", "material": "h2o", "extent": {"mass_fraction": h2o},
                       "refused": volatile["status"]})
    ledger = {"total": total, "core": core, "core_mass": core_mass, "x_Fe": x["Fe"], "core_x": x, "bulk_Fe": vals["Fe"],
              "mantle_oxides": oxide_mass, "mantle_elemental": elemental, "mantle_mass": mantle_mass,
              "mantle_oxides_wt": oxides_wt, "volatile": h2o, "o_delta": delta, "fe_metal_fraction": f_metal,
              "ni_core_share": ni_share}
    return LayerPlan(form="elements", layers=layers, core_mass_fraction=core_total, ledger=ledger,
                     disclosures=disclosures, o_check=o_check, volatile=volatile, residual=residual)


def fe_budget_misfit(x_fe, bulk_fe, fe_metal_fraction, fitted_core_mass_fraction) -> dict:
    """(b2)'s disclosed Fe-budget misfit (design §4.6; S0 68 n1; S1 §2.5): the core Fe a fitted core mass implies,
    x_Fe × fitted CMF, against the declared fe_metal_fraction × bulk Fe."""
    implied = x_fe * fitted_core_mass_fraction
    declared = fe_metal_fraction * bulk_fe
    return {"implied_core_Fe": implied, "declared_core_Fe": declared, "misfit": implied - declared,
            "fitted_core_mass_fraction": fitted_core_mass_fraction, "x_Fe": x_fe, "bulk_Fe": bulk_fe,
            "fe_metal_fraction": fe_metal_fraction, "grade": "derived (partition plan × fitted core mass)"}
