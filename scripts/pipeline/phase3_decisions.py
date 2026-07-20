# Phase 3 리포트의 ## Decisions 표를 파싱하는 공용 모듈 — emitter/게이트/해석기가 공유하는 단일 파서.
# regenerable: library module, imported by check_pipeline_flow.py / resolve_emit_values.py
# (emitter 스킬 내 로컬 정규식 구현은 emit 재배선 시 이 모듈로 교체 — pipeline-contract.md §1/§3)
"""Shared parser for the `## Decisions` table in docs/phase3/<slug>.md.

The table is the machine interface of the 3→4 and 3→emit boundaries
(docs/reference/pipeline-contract.md §1). Columns are fixed:

    | Field | Value | Confidence | Basis |

Field cells are `backtick_name` optionally followed by a qualifier,
e.g. ``equilibrium_temp_k`` ``(A=0)``. The legacy emitter regex kept only
{name: value} and silently let qualified duplicates overwrite each other;
this parser preserves the qualifier so both rows survive.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

DECISIONS_HEADER = re.compile(r"^##\s+Decisions\s*$", re.MULTILINE)
# | `name` qualifier | value | confidence | basis |
ROW_RE = re.compile(
    r"^\|\s*`(?P<name>[^`]+)`\s*(?P<qualifier>[^|]*?)\s*\|"
    r"\s*(?P<value>[^|]*?)\s*\|"
    r"(?:\s*(?P<confidence>[^|]*?)\s*\|)?"
    r"(?:\s*(?P<basis>[^|]*?)\s*\|)?\s*$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Decision:
    name: str          # backtick field name, e.g. "equilibrium_temp_k"
    qualifier: str     # trailing cell text after the backticks ("(A=0)" or "")
    value: str
    confidence: str
    basis: str

    @property
    def label(self) -> str:
        """Full unique label: name + qualifier."""
        return f"{self.name} {self.qualifier}".strip()


def decisions_block(md: str) -> str | None:
    """Return the raw text between '## Decisions' and the next '## ' heading."""
    m = DECISIONS_HEADER.search(md)
    if not m:
        return None
    after = md[m.end():]
    nxt = re.search(r"^##\s+", after, re.MULTILINE)
    return after[: nxt.start()] if nxt else after


def parse_decisions(md: str) -> list[Decision] | None:
    """Parse all Decisions rows. None = no Decisions section at all."""
    block = decisions_block(md)
    if block is None:
        return None
    rows = []
    for m in ROW_RE.finditer(block):
        name = m.group("name").strip()
        if name.lower() == "field":  # header row guard (unbacktick'd headers don't match anyway)
            continue
        rows.append(
            Decision(
                name=name,
                qualifier=(m.group("qualifier") or "").strip(),
                value=(m.group("value") or "").strip(),
                confidence=(m.group("confidence") or "").strip(),
                basis=(m.group("basis") or "").strip(),
            )
        )
    return rows


def as_value_dict(rows: list[Decision]) -> dict[str, str]:
    """{full label: value} — qualified duplicates stay distinct."""
    return {r.label: r.value for r in rows}


def as_simple_dict(rows: list[Decision]) -> dict[str, str]:
    """Legacy emitter view: {name: value}, last qualified row wins."""
    return {r.name: r.value for r in rows}


def duplicate_labels(rows: list[Decision]) -> list[str]:
    seen, dups = set(), []
    for r in rows:
        if r.label in seen:
            dups.append(r.label)
        seen.add(r.label)
    return dups


def load_report(md_path: str | Path) -> list[Decision] | None:
    return parse_decisions(Path(md_path).read_text(encoding="utf-8"))
