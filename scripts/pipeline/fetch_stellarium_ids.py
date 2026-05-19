#!/usr/bin/env python3
# noctuasky API로 별 이름 → Stellarium Web skysource ID 조회. target_list.json 의
# 각 시스템에 stellarium_ids 필드 in-place 추가.
"""
docs/index.html 의 Stellarium 버튼이 사용하는 skysource ID를 별 추가 시점에
미리 조회해 두는 사전계산기. 런타임에 noctuasky를 두드리는 fallback 도 유지하지만,
DB 에 박혀 있으면 (a) 더 빠르고 (b) noctuasky 가 다운돼도 작동한다.

Usage:
    python3 scripts/pipeline/fetch_stellarium_ids.py            # 모든 시스템
    python3 scripts/pipeline/fetch_stellarium_ids.py --only "Barnard's Star,Sirius"
    python3 scripts/pipeline/fetch_stellarium_ids.py --new-only # 아직 stellarium_ids 없는 시스템만
    python3 scripts/pipeline/fetch_stellarium_ids.py --dry-run  # 출력만, 파일 미수정

조회 규칙
  1) 컴포넌트 이름 그대로 시도
  2) 실패하면 SIMBAD canonical 이름으로 한번 더 시도
  3) 둘 다 실패면 null

이름 → skysource ID 변환 (Stellarium Web 와 동일):
  "NAME Barnard's Star"  → "Barnard'sStar"
  "* alf CMa"            → "alfCMa"
  prefix 'NAME '/'*' 제거, 모든 공백 제거
"""
import argparse, json, os, re, time, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOCTUA = "https://api.noctuasky.com/api/v1/skysources/name/"
SIMBAD = "https://simbad.u-strasbg.fr/simbad/sim-tap/sync"

PREFIX_RE = re.compile(r"^(?:NAME|\*)\s+")
WS_RE     = re.compile(r"\s+")


def noctuasky_lookup(name, timeout=5):
    """이름 → skysource ID. 못 찾으면 None."""
    try:
        url = NOCTUA + urllib.parse.quote(name)
        with urllib.request.urlopen(url, timeout=timeout) as r:
            d = json.load(r)
    except Exception:
        return None
    names = d.get("names") or []
    if not names or names[0] in ("?", ""):
        return None
    raw = names[0]
    raw = PREFIX_RE.sub("", raw)
    raw = WS_RE.sub("", raw)
    return raw or None


def simbad_idents(name, timeout=15):
    """SIMBAD ident 테이블 전체 alias 목록 (main_id 포함). 가장 그럴듯한 순서.

    NAME/V*/* 같은 prefix 가 붙은 alias 는 prefix 제거한 버전을 별도로 추가해서
    noctuasky 와의 매칭 확률을 높임.
    """
    safe = name.replace("'", "''")
    # 1) name → oid 1차 조회
    q1 = f"SELECT TOP 1 oidref FROM ident WHERE id='{safe}'"
    data = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL",
                                    "FORMAT": "json", "QUERY": q1}).encode()
    req = urllib.request.Request(SIMBAD, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            res = json.load(r)
    except Exception:
        return []
    rows = res.get("data") or []
    if not rows:
        return []
    oid = rows[0][0]
    # 2) oid 의 모든 alias
    q = f"SELECT id FROM ident WHERE oidref={oid}"
    data = urllib.parse.urlencode({"REQUEST": "doQuery", "LANG": "ADQL",
                                    "FORMAT": "json", "QUERY": q}).encode()
    req = urllib.request.Request(SIMBAD, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            res = json.load(r)
    except Exception:
        return []
    rows = res.get("data") or []
    out = []
    seen = set()
    for row in rows:
        raw = (row[0] or "").strip()
        if not raw:
            continue
        # 그대로 한 번
        norm = re.sub(r"\s+", " ", raw).strip()
        if norm and norm not in seen:
            seen.add(norm); out.append(norm)
        # prefix 제거 ('NAME ', 'V* ', '* ', 'HD ' 같은 catalog prefix는 유지)
        stripped = re.sub(r"^(?:NAME|V\*|\*)\s+", "", raw)
        stripped = re.sub(r"\s+", " ", stripped).strip()
        if stripped and stripped != norm and stripped not in seen:
            seen.add(stripped); out.append(stripped)
    return out


def lookup_for_component(name):
    """1차: 직접 / 2차: SIMBAD ident 목록 순회 / 실패: None."""
    sid = noctuasky_lookup(name)
    if sid:
        return sid, "direct"
    for alias in simbad_idents(name):
        if alias.lower() == name.lower():
            continue
        sid = noctuasky_lookup(alias)
        if sid:
            return sid, f"via_simbad:{alias}"
        time.sleep(0.05)
    return None, "not_found"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated system names; default = all")
    ap.add_argument("--new-only", action="store_true",
                    help="skip systems that already have stellarium_ids")
    ap.add_argument("--retry-failed", action="store_true",
                    help="re-query components whose stored value is null")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    tl_path = f"{BASE}/db/target_list.json"
    with open(tl_path) as f:
        target_list = json.load(f)

    only = None
    if args.only:
        only = {s.strip() for s in args.only.split(",")}

    # 대상 시스템 사전 집계
    to_process = []
    for entry in target_list:
        sys_name = entry["system"]
        if only and sys_name not in only:
            continue
        if args.new_only and "stellarium_ids" in entry:
            continue
        existing = entry.get("stellarium_ids") or {}
        # comp 가 dict 에 아직 없거나 (--retry-failed 시) 값이 None 인 경우 큐잉
        pending = []
        for c in entry["components"]:
            if c not in existing:
                pending.append(c)
            elif args.retry_failed and existing[c] is None:
                pending.append(c)
        if pending:
            to_process.append((entry, pending))

    total_comps = sum(len(p) for _, p in to_process)
    print(f"대상 시스템: {len(to_process)}, 대상 컴포넌트: {total_comps}")
    print()

    n_resolved = n_failed = 0
    done_comps = 0
    save_every = 15  # N 컴포넌트마다 중간 저장

    for entry, pending_comps in to_process:
        sys_name = entry["system"]
        sids = entry.get("stellarium_ids") or {}
        for comp in pending_comps:
            sid, how = lookup_for_component(comp)
            sids[comp] = sid
            done_comps += 1
            pct = 100.0 * done_comps / total_comps if total_comps else 0
            tag = sid or "(없음)"
            print(f"  [{done_comps:3d}/{total_comps}  {pct:5.1f}%] {sys_name}/{comp}: {tag}  [{how}]",
                  flush=True)
            if sid: n_resolved += 1
            else:   n_failed += 1
            time.sleep(0.1)
            # 중간 저장
            if not args.dry_run and done_comps % save_every == 0:
                entry["stellarium_ids"] = sids  # in-memory 반영
                with open(tl_path, "w") as f:
                    json.dump(target_list, f, indent=2, ensure_ascii=False)
                print(f"  ── 중간 저장 ({done_comps}/{total_comps}) ──", flush=True)
        entry["stellarium_ids"] = sids

    print()
    print(f"resolved: {n_resolved}, failed: {n_failed}")

    if args.dry_run:
        print("[DRY RUN] target_list.json 미수정")
        return
    with open(tl_path, "w") as f:
        json.dump(target_list, f, indent=2, ensure_ascii=False)
    print(f"저장: {tl_path}")


if __name__ == "__main__":
    main()
