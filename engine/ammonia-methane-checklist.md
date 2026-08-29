# Checklist: ammonia and methane — closing C4 unbuilt

Plan in one line: the water–ammonia–methane tables cannot be reached except by author
request; record the three routes and why each fails, fix the two sentences the list got
wrong (the price is not bounded; the sign is three-tiered), and close the row.

## Search
- [x] Bethkenhagen+ 2017 full text (cache 1709.04133.md): grid described, no data-availability statement, no URL
- [x] Bethkenhagen+ 2013 (2013JChPh.138w4504B): AIP paywall, 330 GPa · 500–10 000 K
- [x] FPEOS / Militzer+ 2021 (2021PhRvE.103a3203M): CH₄ present, no NH₃, 10⁴–10⁹ K above the adiabat
- [x] every bibcode/DOI checked by title against an ADS response (five queries, 2026-08-30)

## The two sentences
- [x] no bounded price anywhere: row, methodology (EN + KO), `eos.py` already correct
- [x] sign in three tiers — composition (+, derived numbers marked), thermal (mechanism, no sign), net (needs tables)

## Landing
- [x] C4 row closed, dated, with the three routes, the tiers, the C5 attribution, and the request-list line
- [x] domain prose that mentions the substitution updated, Korean mirror
- [x] citations: Bethkenhagen 2013, Militzer 2021, Nettelmann 2016, Helled 2020 (EN + KO)
- [x] `bash scripts/check.sh` FAIL 0
- [x] report to `nearstars-cb`
