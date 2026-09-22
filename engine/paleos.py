# PALEOS 표를 우리 상자 **바깥**에서만 이름 붙은 둘째 의견으로 읽어 오는 조회기 (ㄱ, 사전등록 a610ae6d)
"""Read the PALEOS lookup tables as a **named second extrapolation**, beside our own value.

This module never replaces a shipped number. It answers a question our fits have no grounds for —
*«outside our declared box, what does somebody else's table say?»* — and every answer it gives
carries a grade that travels with it.

**Three answers, and they are different cells.**

| grade | meaning |
|---|---|
| `PALEOS 외삽` | the table has this node; the value is theirs, outside our box |
| `PALEOS 없음` | the request is inside their grid, but that node is **an absent row** |
| `PALEOS 범위 밖` | the request is outside their grid's own P/T ends |

⚠ **«없음» and «범위 밖» must not be folded together.** MgSiO₃ omits **176 782 of 513 380** rows, and
they are absent lines rather than `NaN` — a reader who greps for `NaN` finds the header's own
instructions and concludes the table is complete (P40 Amendment 3).

⚠ **The iron table's phase column is never read.** It carries `liquid` and `unknown` only — 236 651
rows of `unknown`, fully populated, names missing. A label we cannot read must not decorate a value
we print.

⚠ **Each axis's step is derived from that axis's own endpoints, never typed.** Three of the four axes
are exactly 150.00000 nodes per decade; the **T axis of Fe and MgSiO₃** is **150.2252**. A hard-coded
1/150 drifts 0.876 % on that one axis — 100 876 K in place of 100 000 K, a whole row.

Access is **streamed**: a binary search over byte offsets, because the rows are sorted ascending by
(P, T). Nothing loads the surface; the largest file is 192 MB and we read a few kilobytes of it.
"""
from __future__ import annotations

import math
import pathlib
from typing import NamedTuple
import re
import time

# 읽기 전용 논문 캐시. ⚠ 이 경로에 **쓰지 않는다** — 워크트리 밖이다.
PAPERS = pathlib.Path("/Users/vana/Desktop/NearStars/docs/phase3/_papers")

class Table(NamedTuple):
    """한 표의 파일명과 판본. ⚠ **둘을 한 자리에 둔다** — 따로 두면 갈라지고, 이 항목이 고치는
    것이 바로 그 갈라짐이다 (2026-09-22: v1.3.0 표를 읽은 실행이 자기 출력에 «v1.2.1» 이라 적었다)."""
    file: str
    version: str


#: ⚠ **판본은 표에서 못 읽는다 — 우리 선언이다.** 머리말에 판본 문자열이 **셋 다 0 건**이고
#:   `Generated:` 타임스탬프뿐이라, v1.2.1 과 v1.3.0 의 머리 세 줄이 **글자까지 같다.**
#:   그러므로 **표를 갈아 끼울 때 판본을 같이 바꾸는 것은 사람의 일**이다 — 기계가 못 잡는다.
#:   우리가 줄 수 있는 것은 **사유 줄에 파일명과 판본을 나란히 찍는 것**뿐이고(아래 `why`),
#:   그러면 어긋남이 로그에서 읽힌다.
#: ⚠ **판본은 표마다 다르다.** Fe 만 1.3.0 이고 MgSiO₃·H₂O 는 1.2.1 그대로다 — 저자가 그 둘은
#:   양쪽 해상도에서 깨끗하다고 했고 v1.3.0 레코드가 **같은 md5·같은 크기**로 인쇄한다.
#: ⚠ **Fe 는 파일명에 판본이 들어 있다** (`…v130.dat`). 같은 이름으로 몰래 갈아 끼우는 일이
#:   그 표에서는 저절로 닫힌다. 나머지 둘은 안 그렇다.
TABLES = {"Fe": Table("paleos_iron_eos_table_pt.v130.dat", "1.3.0"),
          "MgSiO3": Table("paleos_mgsio3_eos_table_pt.dat", "1.2.1"),
          "H2O": Table("paleos_water_eos_table_pt.dat", "1.2.1")}

# ⚠ 상은 마지막 필드가 아니다 — 물 표는 열이 13 이고 마지막은 `x_d` 라, 마지막 필드를 읽는
#   코드는 세 파일 중 둘에서만 맞는다 (§6 C). 그리고 **자리도 우리가 적지 않는다**: 머리말이
#   `#  10. phase  - Phase identifier` 로 열 이름을 인쇄하므로 거기서 읽는다. 타이핑해 두면
#   표가 v1.3 에서 열을 옮기는 날 **다른 열의 문자열이 상 이름 자리에 조용히 앉는다** (감사석).
PHASE_COLUMN = "phase"

GRADE_HIT = "PALEOS 외삽"
GRADE_ABSENT = "PALEOS 없음"
GRADE_OUT = "PALEOS 범위 밖"

# 풀이당 비용. ⚠ 값을 만드는 커밋에서 값을 센다 — 나중에 발견하지 않는다 (C82-2 규칙).
PALEOS_COST = {"lookups": 0, "seconds": 0.0, "seeks": 0,
               GRADE_HIT: 0, GRADE_ABSENT: 0, GRADE_OUT: 0}

_FACTS: dict[str, "TableFacts"] = {}


class TableFacts:
    """한 표의 격자 사실 — **전부 그 파일의 머리말에서 읽는다**, 타이핑하지 않는다."""

    __slots__ = ("name", "path", "p_lo", "p_hi", "t_lo", "t_hi", "n_p", "n_t",
                 "dlog_p", "dlog_t", "comment_lines", "data_start", "columns", "sorted_note")

    def __init__(self, name: str, path: pathlib.Path):
        self.name = name
        self.path = path
        dom_p = dom_t = grid = None
        columns: list[str] = []
        comments = 0
        offset = 0
        with path.open("rb") as fh:
            while True:
                here = fh.tell()
                raw = fh.readline()
                if not raw or not raw.startswith(b"#"):
                    offset = here
                    break
                comments += 1
                line = raw.decode("utf-8", "replace")
                if "Pressure:" in line:
                    dom_p = [float(x) for x in re.findall(r"[\d.]+e[+-]\d+", line)]
                elif "Temperature:" in line:
                    dom_t = [float(x) for x in re.findall(r"[\d.]+e[+-]\d+", line)]
                col = re.match(r"#\s+(\d+)\.\s+(\S+)\s+-", line)
                if col:
                    idx = int(col.group(1)) - 1
                    while len(columns) <= idx:
                        columns.append("")
                    columns[idx] = col.group(2)
                if "Grid size:" in line and grid is None:
                    g = re.findall(r"(\d+) x (\d+)", line)
                    if g:
                        grid = (int(g[0][0]), int(g[0][1]))
        if not (dom_p and dom_t and grid):
            raise ValueError(f"{path.name}: 머리말에서 격자 사실을 못 읽었다 "
                             f"(P {dom_p} · T {dom_t} · grid {grid})")
        self.p_lo, self.p_hi = dom_p
        self.t_lo, self.t_hi = dom_t
        self.n_p, self.n_t = grid
        # ⚠ 축마다 **자기 끝점에서** 스텝을 낸다. 한 축의 수를 다른 축에 옮기면 행 하나가 밀린다.
        self.dlog_p = (math.log10(self.p_hi) - math.log10(self.p_lo)) / (self.n_p - 1)
        self.dlog_t = (math.log10(self.t_hi) - math.log10(self.t_lo)) / (self.n_t - 1)
        self.comment_lines = comments
        self.data_start = offset
        if PHASE_COLUMN not in columns:
            raise ValueError(f"{path.name}: 머리말의 열 목록에 `{PHASE_COLUMN}` 이 없다 "
                             f"(읽은 열 {len(columns)} 개)")
        self.columns = columns
        # ⚠ **정렬 가정을 산문에 두지 않는다** — 이진 탐색이 옳은 것은 줄이 (P, T) 오름차순일
        #   때뿐이고, 거짓이면 틀린 줄을 집거나 「없음」을 돌려준다. **잘못된 답이 정당한 라벨을
        #   쓰고 나온다.** 그래서 같은 실행에서 세 점을 읽어 단조인지 확인한다 (감사석).
        self.sorted_note = self._check_sorted()

    def phase_field(self) -> int:
        """상 열의 자리 — **머리말이 인쇄한 순서에서** 읽는다."""
        return self.columns.index(PHASE_COLUMN)

    def _check_sorted(self) -> str:
        """첫·중간·마지막 줄의 색인 쌍이 오름차순인가. 아니면 여기서 멈춘다."""
        size = self.path.stat().st_size
        keys = []
        with self.path.open("r", encoding="utf-8") as fh:
            for pos in (self.data_start, (self.data_start + size) // 2, max(size - 4096, 0)):
                fh.seek(_seek_line_start(fh, pos, self.data_start))
                line = fh.readline()
                if pos == max(size - 4096, 0):
                    for nxt in fh:            # 마지막 데이터 줄까지
                        if nxt.strip():
                            line = nxt
                if line.strip():
                    keys.append(_row_key(line, self))
        if not (len(keys) == 3 and keys[0] < keys[1] < keys[2]):
            raise ValueError(f"{self.path.name}: 줄이 (P, T) 오름차순이 아니다 — 읽은 색인 {keys}. "
                             "이진 탐색을 쓸 수 없다")
        return f"첫 {keys[0]} < 중간 {keys[1]} < 마지막 {keys[2]}"

    def nodes_per_decade(self) -> tuple[float, float]:
        """축별 «십진 한 자리에 몇 칸» — 인쇄용. 세 축은 150.0, Fe·MgSiO₃ 의 T 만 150.2252 다."""
        return 1.0 / self.dlog_p, 1.0 / self.dlog_t

    def index_p(self, p: float) -> int:
        return int(round((math.log10(p) - math.log10(self.p_lo)) / self.dlog_p))

    def index_t(self, t: float) -> int:
        return int(round((math.log10(t) - math.log10(self.t_lo)) / self.dlog_t))

    def inside(self, p: float, t: float) -> bool:
        return self.p_lo <= p <= self.p_hi and self.t_lo <= t <= self.t_hi


def facts(table: str) -> TableFacts:
    if table not in _FACTS:
        _FACTS[table] = TableFacts(table, PAPERS / TABLES[table].file)
    return _FACTS[table]


def _row_key(line: str, f: TableFacts) -> tuple[int, int]:
    """그 줄이 앉은 격자 칸 (i_p, j_t). ⚠ 부동소수 동치가 아니라 **색인**으로 비교한다."""
    parts = line.split(None, 2)
    return f.index_p(float(parts[0])), f.index_t(float(parts[1]))


def _seek_line_start(fh, pos: int, floor: int) -> int:
    """`pos` 를 품은 줄의 시작 오프셋. 줄 한복판에 떨어지는 이분법을 줄 경계로 되돌린다."""
    if pos <= floor:
        return floor
    fh.seek(pos)
    fh.readline()                      # 잘린 줄 버리기
    return fh.tell()


def _find(f: TableFacts, key: tuple[int, int]) -> str | None:
    """(i_p, j_t) 칸의 줄을 바이트 이분법으로 찾는다. 없으면 `None` — **빠진 줄이다**.

    ⚠ 줄은 (P, T) 오름차순으로 정렬돼 있고 P 가 바깥이다. 그래서 색인 쌍의 사전식 비교가
    파일 순서와 같다."""
    lo, hi = f.data_start, f.path.stat().st_size
    with f.path.open("r", encoding="utf-8") as fh:
        while lo < hi:
            mid = (lo + hi) // 2
            start = _seek_line_start(fh, mid, f.data_start)
            PALEOS_COST["seeks"] += 1
            if start >= hi:
                hi = mid
                continue
            fh.seek(start)
            line = fh.readline()
            if not line.strip():
                hi = mid
                continue
            here = _row_key(line, f)
            if here == key:
                return line
            if here < key:
                lo = start + len(line.encode("utf-8"))
            else:
                hi = start
        # 이분법이 닫힌 자리의 줄 하나를 마지막으로 본다 — 경계에서 한 칸 빗나가는 경우.
        fh.seek(_seek_line_start(fh, lo, f.data_start))
        line = fh.readline()
        if line.strip() and _row_key(line, f) == key:
            return line
    return None


def lookup(table: str, p: float, t: float) -> dict:
    """그 (P, T) 에서 PALEOS 가 말하는 것. **답은 언제나 등급을 달고 나온다.**

    돌려주는 것 — `grade` · `density`(kg/m³, 없으면 `None`) · `phase`(문자열 또는 `None`) ·
    `p_node`/`t_node`(실제로 읽은 격자 칸) · `why`(사람이 읽는 한 문장).

    ⚠ `table == "Fe"` 이면 `phase` 는 **언제나 `None`** 이다 — 그 열은 이 모듈이 안 읽는다."""
    t0 = time.perf_counter()
    f = facts(table)
    PALEOS_COST["lookups"] += 1
    try:
        if not f.inside(p, t):
            PALEOS_COST[GRADE_OUT] += 1
            return {"grade": GRADE_OUT, "density": None, "phase": None,
                    "p_node": None, "t_node": None,
                    "why": (f"{p:.6g} Pa · {t:.6g} K 는 {table} 표 자신의 격자 밖이다 "
                            f"(P {f.p_lo:.6g}–{f.p_hi:.6g} Pa · T {f.t_lo:.6g}–{f.t_hi:.6g} K)")}
        i, j = f.index_p(p), f.index_t(t)
        p_node = 10.0 ** (math.log10(f.p_lo) + i * f.dlog_p)
        t_node = 10.0 ** (math.log10(f.t_lo) + j * f.dlog_t)
        line = _find(f, (i, j))
        if line is None:
            PALEOS_COST[GRADE_ABSENT] += 1
            return {"grade": GRADE_ABSENT, "density": None, "phase": None,
                    "p_node": p_node, "t_node": t_node,
                    "why": (f"{table} 표에 그 칸의 줄이 없다 (i_p {i} · j_t {j}) — "
                            "NaN 이 아니라 **빠진 줄**이다")}
        parts = line.split()
        phase = None if table == "Fe" else parts[f.phase_field()]
        PALEOS_COST[GRADE_HIT] += 1
        return {"grade": GRADE_HIT, "density": float(parts[2]), "phase": phase,
                "p_node": p_node, "t_node": t_node,
                "why": (f"{table} 표 v{TABLES[table].version} "
                        f"(`{TABLES[table].file}`) 의 격자 칸 (i_p {i} · j_t {j}) — "
                        f"우리 상자 밖이라 이 값은 **남의 표의 외삽**이다")}
    finally:
        PALEOS_COST["seconds"] += time.perf_counter() - t0


def cost_line() -> str:
    """풀이당 비용 한 줄 — 조회 수·seek 수·벽시계, 그리고 등급별 건수."""
    c = PALEOS_COST
    return (f"PALEOS 조회 {c['lookups']} 회 · seek {c['seeks']} 회 · {c['seconds']:.3f} s · "
            f"{GRADE_HIT} {c[GRADE_HIT]} · {GRADE_ABSENT} {c[GRADE_ABSENT]} · "
            f"{GRADE_OUT} {c[GRADE_OUT]}")


def reset_cost() -> None:
    for k in PALEOS_COST:
        PALEOS_COST[k] = 0 if isinstance(PALEOS_COST[k], int) else 0.0
