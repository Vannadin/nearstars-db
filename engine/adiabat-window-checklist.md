# Checklist: the adiabat's validated window (C8)

Plan in one line: transcribe Noack & Lasbleis 2020 eq. (22) and its supports from the PDF,
run the engine against it and against Unterborn eq. 7 across 0.8–2 M⊕, and restate the grade
above 1.05 R⊕ on the measured spread.

- [x] bibcode/DOI checked by title (ADS); PDF in the cache, text extracted with pdftotext
- [x] eqs. (8), (9), (13)–(15), (18), (19), (22) and their constants read from the PDF; (20)–(21) excluded on purpose
- [x] engine vs eq. (22) (engine geometry and paper geometry) vs eq. 7, 0.8–2 M⊕ — table
- [x] Earth point reproduces the reported 2562 K (2563 K)
- [x] anchor-choice caveat measured (T at 250 km, rise ratio), not hidden
- [x] bands frozen in `test_interior.py`; `--adiabat` prints the table
- [x] grade note in `solve` restated on the spread (path function: `--refresh`, values identical)
- [x] domain row + validation section + citation, EN and KO
- [x] C8 row closed with the 2 M⊕ ceiling; anchors bit-identical; gate FAIL 0; report
