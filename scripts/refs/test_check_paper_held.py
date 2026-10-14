# check_paper_held.py 의 판정(HELD·ABSTRACT-ONLY·SIDECAR-ONLY·ABSENT)과 이름 규칙을 가짜 캐시로 확인하는 오프라인 시험
"""Offline tests for check_paper_held.py, against a synthetic cache in a temp dir.

The ADS lookup is replaced by a fixed table, so no token and no network are needed. Each case is one of
the naming rules or states the tool's docstring records as having once produced a false verdict.

    python3 scripts/refs/test_check_paper_held.py      (or pytest)
"""
import contextlib
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_paper_held as cph  # noqa: E402

FULL_MD = "x" * (cph.BODY_MIN_BYTES + 1)
STUB_MD = "x" * 50


def _write(root, rel, text="", binary=False):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if binary else "w") as fh:
        fh.write(text.encode() if binary else text)


def _cache(root):
    _write(root, "2016ApJ...833L...4G.pdf", "%PDF", binary=True)            # bibcode name, pdf body
    _write(root, "2001E_PSL.185...49A.pdf", "%PDF", binary=True)            # '&' written as '_'
    _write(root, "1301.6674.md", FULL_MD)                                   # arXiv name, md body
    _write(root, "1004.1091.md", STUB_MD)                                   # abstract page only
    _write(root, "1209.5323.html", "<html>abstract</html>")                 # html without ltx_document
    _write(root, "astro-ph_0011153.html", "<div class='ltx_document'></div>")   # old-style arXiv
    _write(root, "summers_2014_limiting_spectrum.pdf", "%PDF", binary=True)  # descriptive name …
    _write(root, "summers_2014_limiting_spectrum.PROVENANCE.txt",
           "bibcode  2014JGRA..119.6313S\narXiv    NONE\n")                  # … mapped by its sidecar
    _write(root, "only_sidecar.PROVENANCE.txt", "bibcode  2099XXXX....1....1Z\n")   # sidecar, no body
    _write(root, "sub/2010Natur.468..123B.pdf", "%PDF", binary=True)        # subfolder


ADS = {  # bibcode -> arXiv ids, as ADS would list them
    "2013ApJ...765..131K": ["1301.6674"],
    "2010ApJ...714..321X": ["1004.1091"],
    "2001ApJ...547L..49W": ["astro-ph_0011153"],
}


def _run(args, root):
    old_cache, old_ads = cph.CACHE, cph.ads_identifiers
    cph.CACHE = root
    cph.cache_names.__defaults__ = (root,)
    cph.sidecar_index.__defaults__ = (root,)
    cph.ads_identifiers = lambda bibs: {b: ADS.get(b, []) for b in bibs}
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            rc = cph.main(["check_paper_held.py", *args])
    finally:
        cph.CACHE, cph.ads_identifiers = old_cache, old_ads
        cph.cache_names.__defaults__ = (old_cache,)
        cph.sidecar_index.__defaults__ = (old_cache,)
    return rc, out.getvalue()


def _verdict(text, bib):
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == bib:
            return parts[0]
    raise AssertionError(f"no verdict line for {bib}:\n{text}")


def test_verdicts():
    with tempfile.TemporaryDirectory() as root:
        _cache(root)
        cases = {
            "2016ApJ...833L...4G": "HELD",            # by bibcode
            "2001E&PSL.185...49A": "HELD",            # '&' -> '_'
            "2013ApJ...765..131K": "HELD",            # via the arXiv id ADS lists
            "2001ApJ...547L..49W": "HELD",            # old-style arXiv id
            "2014JGRA..119.6313S": "HELD",            # via the PROVENANCE sidecar
            "2010Natur.468..123B": "HELD",            # in a subfolder
            "2010ApJ...714..321X": "ABSTRACT-ONLY",   # 50-byte md under its arXiv id
            "2099XXXX....1....1Z": "SIDECAR-ONLY",    # sidecar with no body
            "2020ApJ...900....1Q": "ABSENT",
        }
        rc, text = _run(list(cases), root)
        for bib, want in cases.items():
            assert _verdict(text, bib) == want, (bib, want, text)
        assert rc == 1                                 # any non-held paper fails the run
        assert "6/9 held" in text


def test_all_held_exits_zero():
    with tempfile.TemporaryDirectory() as root:
        _cache(root)
        rc, text = _run(["2016ApJ...833L...4G", "2013ApJ...765..131K"], root)
        assert rc == 0 and "2/2 held" in text


def test_absent_lists_what_was_checked():
    """The ABSENT line prints every name tried: the self-check the docstring says must not change."""
    with tempfile.TemporaryDirectory() as root:
        _cache(root)
        _rc, text = _run(["2020A&A...600A...1Q"], root)
        line = next(l for l in text.splitlines() if l.startswith("ABSENT"))
        assert "2020A&A...600A...1Q" in line and "2020A_A...600A...1Q" in line


def test_contradictions_flags_held_paper_called_unobtainable():
    with tempfile.TemporaryDirectory() as root:
        _cache(root)
        doc = os.path.join(root, "doc.md")
        _write(root, "doc.md", "Garraffo 2016ApJ...833L...4G is paywalled, not obtained.\n"
                               "Unheld 2020ApJ...900....1Q is paywalled.\n")
        cph.cache_names.__defaults__ = (root,)
        cph.sidecar_index.__defaults__ = (root,)
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                rc = cph.contradictions([doc])
        finally:
            cph.cache_names.__defaults__ = (cph.CACHE,)
            cph.sidecar_index.__defaults__ = (cph.CACHE,)
        assert rc == 1 and "1 place(s)" in out.getvalue()


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("ok", name)
