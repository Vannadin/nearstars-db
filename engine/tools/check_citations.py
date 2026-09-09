# 논문 인용 규약 검사 — 절 단위로 "저자+연도" 만 있고 bibcode 가 없는 곳을 센다 (첫 판: 세기만)
"""Count paper citations that carry no bibcode, section by section.

    python3 engine/tools/check_citations.py            # 절별 표 + 합계
    python3 engine/tools/check_citations.py --quiet     # 합계만

⚠ **첫 판은 판정하지 않는다.** 이 저장소는 "저자+연도" 만으로 인용한 절이 규범이었고 bibcode 를 함께
적은 절이 예외였다 — 기존 절을 고치는 것은 이 검사의 몫이 아니다. 그래서 **카운트와 기준선만 인쇄**하고,
기준선이 0 이 된 뒤에 FAIL 로 승격한다(C45 (b) 클래스 ③ 과 같은 경로).

⚠ **기준선 숫자는 레포의 성질이 아니라 규칙의 성질이다.** 같은 파일에서 구현 셋이 160·193·185 로
갈렸다(감사석, 2026-09-09). 그래서 이 파일은 **숫자와 함께 규칙 본문과 알려진 오검출 종류를 적는다** —
숫자만 옮겨 적으면 다음 사람이 다른 규칙으로 재서 어긋난다.

규칙 A (여기 구현된 것)
-----------------------
* 문서를 `### ` 제목으로 자른다. **절 안에 bibcode 가 하나도 없을 때만** 그 절의 인용을 센다.
* bibcode 는 백틱 안의 `2004GeoJI.156..363N` 꼴이면 인정한다 — ⚠ **마크다운 링크로 감싼
  ``[`2004GeoJI...`](url)`` 도 같은 정규식에 걸린다**(감사석의 첫 구현이 이걸 놓쳐 수가 부풀었다).
* 인용은 `저자+ 2019` · `저자 & 저자 2002` · `저자 et al. 2013` 꼴.

알려진 오검출 종류
------------------
* **날짜 산문** — *"Corrected 2026-09-08"*, *"listed 2026-09-09"*. 연도 뒤 `-\\d` 를 거부해서 걸러낸다.
* **분사 + 연도** — 위 규칙으로 대부분 걸러지지만 `Measured 2026` 처럼 날짜가 잘린 형태는 남는다.
  그래서 분사·동사 목록을 따로 거부한다.
* **소유격** — *"Nimmo's 2004 Table 4"* 는 인용이므로 **세는 것이 맞다**; 연도 없는 *"Nimmo's"* 는
  애초에 안 걸린다.
* ⚠ **규칙을 설명하는 글 자체** — 이 규칙을 설명하는 절은 인용의 *예시* 를 적으므로 규칙에 걸린다.
  이 도구를 들여온 절(C33 (b))이 그래서 4건으로 세어졌다(27 절·124 건 → 28 절·128 건). 예시를
  따로 빼는 문법을 만들지 않았다 — **첫 판이 세기만 하는 이유 중 하나가 이것이다.**
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [ROOT / "interior-core.md"]

BIBCODE = re.compile(r"`(\d{4}[A-Za-z&][^`\s]{6,})`")
CITE = re.compile(
    r"\b([A-Z][A-Za-zÀ-ÿô’'-]{2,})"                    # 저자
    r"(?:\s*(?:&|and)\s*[A-Z][A-Za-zÀ-ÿô’'-]{2,})?"     # (& 공저자)
    r"(?:\+|\s+et\s+al\.)?"                             # (+ / et al.)
    r"\s+((?:19|20)\d{2})\b(?!-\d)")                    # 연도, 날짜 아님
#: 날짜 산문의 머리말 — 이 뒤의 연도는 인용이 아니다.
NOT_AUTHOR = {"Corrected", "Registered", "Revisited", "Measured", "Listed", "Built", "Closed",
              "Written", "Recorded", "Added", "Restated", "Withdrawn", "Found", "Since", "By",
              "Brief", "Table", "Figure", "Fig", "Section", "Until", "In", "On", "At", "The"}
#: 2026-09-09 첫 측정, 규칙 A — (bibcode 없는 절 수, 그 절들의 인용 수). ⚠ **FAIL 이 아니다**: 다르면
#: 그 사실만 찍는다. ⚠ 첫 판이 (27, 124) 가 아니라 (28, 128) 인 이유는 이 도구를 들여온 절(C33 (b))이
#: 인용 예시를 적어 스스로 4건 걸리기 때문이다 — 오검출 종류로 위에 적어 두었다.
BASELINE = (28, 128)


def scan(path: Path) -> tuple[list[tuple[str, int]], int, int]:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^### ", text, flags=re.M)
    rows: list[tuple[str, int]] = []
    for part in parts[1:]:
        head = part.split("\n", 1)[0].strip()
        if BIBCODE.search(part):
            continue
        cites = [m for m in CITE.finditer(part) if m.group(1) not in NOT_AUTHOR]
        if cites:
            rows.append((head[:70], len(cites)))
    return rows, len(rows), sum(n for _, n in rows)


def main() -> int:
    quiet = "--quiet" in sys.argv
    total_secs = total_cites = 0
    for path in TARGETS:
        rows, n_secs, n_cites = scan(path)
        total_secs += n_secs
        total_cites += n_cites
        if not quiet:
            print(f"  {path.name} — bibcode 없는 절 {n_secs}개 · 그 절들의 인용 {n_cites}건 (규칙 A)")
            for head, n in sorted(rows, key=lambda r: -r[1])[:12]:
                print(f"      {n:3d}  {head}")
    same = (total_secs, total_cites) == BASELINE
    print(f"  [기록] 인용 규약 (규칙 A): 절 {total_secs} · 인용 {total_cites} "
          f"(기준선 {BASELINE[0]} · {BASELINE[1]}) — "
          f"{'변화 없음' if same else '⚠ 기준선과 다르다'}. 판정 아님 — 규칙 본문과 오검출 종류는 "
          f"이 파일의 독스트링에 있다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
