---
name: nearstars-seat-protocol
description: >-
  How the NearStars engine seats (directing, work, parallel, audit, remote PC) hand work to each
  other: prereg → audit clear → freeze, git-blob hashes, post-freeze notes, the gate, pushes and
  killing jobs. Use when drafting or auditing a registration, freezing or appending to a prereg,
  citing a hash, running or reading the gate, pushing engine/prototype, or messaging another seat.
---

# NearStars seat protocol

Engine work on `engine/*` branches is split across seats. The owner talks to the directing seat
only. Everything that changes a frozen fact goes through one loop.

## The loop

1. **Prereg first.** Before code or a measurement, the work seat drafts a registration in the
   artifacts tree (`~/Desktop/NearStars-artifacts/<date>-*/`, or `pc/<item>/` for the PC) with its
   acceptance lines, a negative control, and for derived values the machine-read fields
   `grade` / `source` / `counter_evidence_searched`. Post-result registrations are allowed if labelled.
2. **Audit clears a blob, not a file.** The audit seat hashes the draft (`git hash-object -w`),
   reads that blob, and sends one message: HOLD *or* clear `<blob>`. Clear messages always cc the
   directing seat.
3. **Directing freezes.** `tools/freeze.py` in the artifacts repo does the hash check, the copy or
   append, the Frozen/Appended line, and a commit of only that file in one step:
   ```
   python3 ~/Desktop/NearStars-artifacts/tools/freeze.py freeze --src DRAFT --dest prereg-x.md \
     --blob CLEAR --seat "directing <addr>" --label "C150 registration" --source "audit <addr> clear blob"
   python3 ~/Desktop/NearStars-artifacts/tools/freeze.py append --src NOTE --dest prereg-x.md \
     --blob CLEAR --dest-blob CURRENT --seat ... --label "C150 post-freeze note 1" --source 'remote-PC `pc/c150/note-1.md`'
   ```
   Frozen bodies never change. Corrections are new notes that name what they void and why.
4. **Code lands after the gate.** Seats send `branch + tip`. Only the directing seat pushes
   `engine/prototype` (fast-forward, no main, no PR), after a gate whose only red is the expected
   one (`scripts/gate_expected_red.yaml`) and an audit clear. A new red or a HOLD goes to the owner.

## Messages

- Seat-to-seat and PC messages are English; result · evidence · next. Long content lives in a file;
  the message carries path + blob. Answer every question; send no bare "received".
- Hash at the edition boundary, once. Quote only hashes you computed yourself at that moment.
- Cite text by a unique phrase anchor (`git grep -c` = 1), not a line number.
- When a seat is waiting on another, check nobody idles: hand out anything without a dependency.

## Gotchas (each one happened)

- Python's `csv` writer emits CRLF on every OS. Write with `lineterminator='\n'`; cite the blob after commit. `freeze.py` refuses CRLF sources.
- A number relayed from another seat's message is not evidence. Re-read it from the origin blob and carry the unrounded value with its source.
- A hash check and the write it guards must be one command; a file reverted between them once got a wrong Frozen line.
- Counting only the side you looked at: before stating a total, name what was not checked (paths, nets, conditions).
- A new required input or state key breaks callers outside the diff (hand-written fixtures, key-set fingerprints). Grep for every caller.
- Stop jobs only by your own pgid (`kill -TERM -<pgid>`, or SIGSTOP/SIGCONT to pause), then confirm with `pgrep '[p]attern'`. `pkill -f` once killed another seat's run.
- Long jobs: detach (`setsid` / double fork, or `nohup … & disown`), redirect `> file 2>&1`, never pipe into `tail`. Resumed sessions kill task-bound children after ~13 min.
- Report what the commit holds, not what you meant to do: an edit can fail silently (unread-file refusal). Check `git show <commit>` before saying «wired» or «fixed». 2026-10-03: a validator was reported wired that wasn't.
- Before a push, re-read the landing registration's own acceptance list yourself (e.g. «owner report sent before the landing commit»). An audit clear's «not blocking» is not a substitute. 2026-10-03: the switch was pushed before its owner report.
- Noise-level differences are not findings. Precision is already well past need; speed wins.
- Fix the class, not the instance: when one site is wrong, find every site on the same code path.
