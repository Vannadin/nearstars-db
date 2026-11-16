# D2 읽기 독자 조사 도구 — 엔진 저장소의 .py 를 ast 로 훑어 silicate_records·d2_read 키·view 생성·_solid/s_path·boundaries·table_regardless 자리를 한 줄씩 적음(D2 읽기 등록 §7; S0 에서는 열쇠와 종류만 고정)
"""python3 -B -m solver.landing.d2_read_census      (D2-read rev 7 §7; S0 stub: the keys and kinds are frozen here, the
walker is written at S3/S4)

Writes solver/landing/d2_read_census.json: {"sites": [{path, line, kind, function}, …], "schema_keys": [...]}, one site
per row, sorted by (path, line, kind). `function` is the enclosing function's qualified name, or «<module>»."""
SITE_KEYS = ("path", "line", "kind", "function")
KINDS = ("option", "record_key", "view", "solid", "boundaries", "table_regardless")
OUT = "solver/landing/d2_read_census.json"
TOP_KEYS = ("sites", "schema_keys")


def census(root):
    raise NotImplementedError("read piece S3/S4: the walker (D2-read §7)")
