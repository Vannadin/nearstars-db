# 노드 결과 타입 — 솔버 Provenance 를 넓힌 NodeProvenance(출처 칸)와 SourceRef, 계약 공통 노트 종류 (계약 §3)
"""Types the chain nodes add on top of `solver.result` (contract `node-contract.frozen.md` §3).

`NodeProvenance` subclasses `solver.result.Provenance` instead of adding a field to it: `result.plain()` serialises
every dataclass field, so a new field on `Provenance` would change every existing solver Answer's canonical bytes
(registration prereg-t-eq-stellar.frozen.md §1, accepted by directing and audit 68). Node quantities carry it;
solver quantities keep the plain `Provenance`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from solver.result import Provenance, freeze

#: Note kinds every node may emit without declaring them (contract §3).
CONTRACT_NOTE_KINDS = ("placeholder", "owner_override", "owner_selection", "owner_widening", "cite_not_cached",
                       "window_stale")
#: Exactly one of these names what a SourceRef is (the material `source` shape, plus `record`).
SOURCE_KINDS = ("cache", "library", "doi", "formula", "user_declared", "record")


@dataclass(frozen=True)
class SourceRef:
    """Where a value was actually read (od 10-10 citation rule). `record` = {file, key, sha256} of a DB entry."""
    kind: str
    ref: object
    page: str | None = None
    where: str | None = None
    sha256: str | None = None
    cites: str | None = None
    abstract_only: bool = False
    identity: bool = False

    def __post_init__(self):
        if self.kind not in SOURCE_KINDS:
            raise ValueError(f"SourceRef.kind must be one of {SOURCE_KINDS}, got {self.kind!r}")
        if self.kind == "record":
            if not isinstance(self.ref, Mapping) or set(self.ref) != {"file", "key", "sha256"}:
                raise ValueError("SourceRef(record).ref must be {file, key, sha256}")
        elif not self.ref:
            raise ValueError(f"SourceRef({self.kind}) needs a ref")
        object.__setattr__(self, "ref", freeze(self.ref))


@dataclass(frozen=True)
class NodeProvenance(Provenance):
    """A node quantity's provenance: the solver's fields, plus the sources read and, for a node's own authored
    step, where counter-evidence was searched (contract §4.3)."""
    sources: tuple = ()
    counter_evidence_searched: tuple = ()

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(self, "sources", tuple(self.sources))
        object.__setattr__(self, "counter_evidence_searched", freeze(tuple(self.counter_evidence_searched)))
        for s in self.sources:
            if not isinstance(s, SourceRef):
                raise ValueError(f"NodeProvenance.sources holds {s!r}, not a SourceRef")


#: Result grade -> input grade word for `Provenance.inputs_read` (contract §4.1 table).
RESULT_TO_INPUT_GRADE = {"measured": "measured", "calibrated": "derived", "analog": "analog",
                         "judgment": "judgment", "authored": "authored"}
