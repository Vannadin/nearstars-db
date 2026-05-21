---
title: <Short descriptive title>
status: active   # active | promoted | archived
created: 2026-MM-DD
---

# <Title>

**NearStars connection.** One paragraph: why does this research matter
for NearStars? What downstream decision does it inform? Without this,
the document does not belong in this repo.

**Scope.** What is in, what is out. Be explicit if no code changes are
expected from this work.

**External references.** Repo URLs, paper bibcodes/DOIs, dataset
endpoints. Use full URLs — no local paths.

---

## 1. Executive summary

A short table or 3–5 bullets answering the core questions this note
exists to settle.

| Question | Answer |
|----------|--------|
| … | … |

---

## 2. Findings

Body of the research. Structure freely (sections, tables, diagrams) as
the material requires.

When you cite source code, use this format for upstream repos:

> [`pile_up.cpp`](https://github.com/mockingbirdnest/Principia/blob/master/ksp_plugin/pile_up.cpp#L575-L618)

When citing files in this repo, use a repo-relative path:

> [`scripts/pipeline/build_systems.py`](../scripts/pipeline/build_systems.py)

---

## 3. Implications for NearStars

The "so what" section. What does this research recommend NearStars do
(or not do)? If a follow-up implementation is warranted, name the next
step and where it would live (`phase2/<topic>/`).

---

## 4. Open questions

What remains unresolved. Future readers can pick these up.
