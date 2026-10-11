# 받아들인 패스의 물질 설명 문구 수집 — 노드마다 기록 뷰를 다시 읽어 답의 Note 로 묶음 (switch-over registration §4)
"""Switch-over registration §4 (N16, D3(c)): the material facts an answer rests on reach `Answer.notes`.

`collect(body, views, acc)` runs once, on the accepted pass only, after every value of the answer is made. It walks
that pass's accepted nodes per layer and asks each record view what it read there: `state(p, t)`'s notes and
`phase_read(p, t)`. Trial passes, rejected stages and probe passes never reach it, so trace separation (A6) holds by
construction, and since it runs after the values, it cannot change one (§4.3).

Kinds (compare.NOTE_KINDS, comparator note 15):
- `material_band`: one per (layer, material, edge), with the largest error met, where, and the P range;
- `material_declared_note`: one per (layer, material, phase, text), with the P range met;
- `material_source_seam`: one per source seam the layer's temperature crossed (from below t to t or above; the
  upper side owns t), with its measured step (material_joins.seam_delta);
- `material_disclosure`: the cross-check disclosures of every phase read; a disclosed formula-check fail of every
  record read (the schema does not tie a check to a boundary, so the record is the unit read);
- `material_grade`: a record with a user-declared source anywhere (impl note 3 B2).
Wording comes from the record's fields only.
"""
from solver import material_joins as mj, material_registry as mr, material_view as mv, result, stepper as st


def _reads(path):
    """(P, T) pairs the pass's rhs read at each accepted node: T_ad, and the lid's local T where it differs."""
    for _m, y, _k in path:
        yield y[1], y[2]
        if y[3] != y[2]:
            yield y[1], y[3]


def _span(d, p, t):
    d["p_min"] = min(d.get("p_min", p), p)
    d["p_max"] = max(d.get("p_max", p), p)


def collect(body, views, acc) -> tuple:
    out = []
    for layer in reversed(body.layers):
        view = views.get(layer.id)
        path = acc.profiles.get(layer.id)
        if not isinstance(view, mv.RecordView) or not path:
            continue
        mid = view.material_id
        bands, declared, phases_read, ts = {}, {}, [], []
        for p, t in _reads(path):
            got = view.state(p, t, None)
            if isinstance(got, st.Stop):                  # an accepted node answered in the pass; nothing to add
                continue
            ts.append(t)
            ph = view.phase_read(p, t)
            if not isinstance(ph, st.Stop) and ph not in phases_read:
                phases_read.append(ph)
            for n in got[2]:
                if isinstance(n, mv.BandNote):
                    d = bands.setdefault(n.edge, {"note": n, "error": n.error, "p": p, "t": t})
                    if n.error is not None and (d["error"] is None or n.error > d["error"]):
                        d.update(note=n, error=n.error, p=p, t=t)
                    if n.dtdp_error is not None:
                        d["dtdp_error"] = max(d.get("dtdp_error") or 0.0, n.dtdp_error)
                    _span(d, p, t)
                elif isinstance(n, mv.DeclaredNote):
                    _span(declared.setdefault((n.phase, n.text), {}), p, t)
        for edge, d in bands.items():
            n = d["note"]
            out.append(result.Note("material_band", f"{mid} {edge}: {n.form} error {d['error']} ({n.grade}; "
                                   f"{n.origin})", {
                                       "layer": layer.id, "material": mid, "edge": edge, "form": n.form,
                                       "error": d["error"], "method": n.method, "grade": n.grade, "origin": n.origin,
                                       "dtdp_error": d.get("dtdp_error"), "dtdp_origin": n.dtdp_origin,
                                       "p_at_max": d["p"], "t_at_max": d["t"], "p_min": d["p_min"],
                                       "p_max": d["p_max"]}))
        for (phase, text), d in declared.items():
            out.append(result.Note("material_declared_note", f"{mid} {phase}: {text}", {
                "layer": layer.id, "material": mid, "phase": phase, "text": text, "p_min": d["p_min"],
                "p_max": d["p_max"]}))
        if ts:
            t_lo, t_hi = min(ts), max(ts)
            for sm in view.record.get("source_seams", ()):
                t_s = mv._v(sm["t"])
                if t_lo < t_s <= t_hi:
                    step = mj.seam_delta(view, sm)
                    out.append(result.Note("material_source_seam", f"{mid} source seam at {t_s:g} K between "
                                           f"{sm['between'][0]} and {sm['between'][1]}", {
                                               "layer": layer.id, "material": mid, "t": t_s,
                                               "between": list(sm["between"]), "band": dict(sm["band"]),
                                               "step": None if isinstance(step, st.Stop) else step,
                                               "step_stop": step.kind if isinstance(step, st.Stop) else None,
                                               "source": sm["source"]}))
        for pi, ph in enumerate(view.record["phases"]):
            if ph["id"] not in phases_read:
                continue
            for j in ph.get("joins_within", ()):
                for text in j.get("disclosures", ()):
                    out.append(result.Note("material_disclosure", f"{mid} {ph['id']}: {text}", {
                        "layer": layer.id, "material": mid, "phase": ph["id"], "of": "cross_check",
                        "between": list(j["between"]), "text": text}))
        for fc in view.record.get("formula_checks", ()):
            df = fc.get("disclosed_fail")
            if df is not None:
                out.append(result.Note("material_disclosure", f"{mid} {fc['quantity']}: {df['why']}", {
                    "layer": layer.id, "material": mid, "of": "formula_check", "quantity": fc["quantity"],
                    "why": df["why"], "bound": df["bound"], "source": df["source"]}))
        if mr._has_user_declared(view.record):
            out.append(result.Note("material_grade", f"{mid} carries a user-declared source (grade «declared»)", {
                "layer": layer.id, "material": mid, "grade": "declared"}))
    return tuple(out)
