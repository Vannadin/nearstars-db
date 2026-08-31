# Queyroux melting line — does any phase verdict actually flip? — checklist

Task from the directing session, 2026-08-31 (owner chose "measure before adopting"). F4
showed our two melting curves are 210–300 K colder than Queyroux+ 2020's in-band
measurements. Question: if a Queyroux-based line replaced ours, would any icy-roster phase
verdict flip? **An uncommitted experiment in a throwaway worktree**
(`git worktree add --detach`, per the standing rule born from the 2026-08-30 window).
Measure, don't judge.

- [x] Detached worktree at HEAD (`NearStars-wt/queyroux-melt-exp`, 73cac7b2)
- [x] Baseline sweep: 5 icy anchors (two-layer + three-layer with published C/MR²) +
      Uranus/Neptune full solves → JSON
- [x] Patch (worktree only): water_t_melt / water_liquid_at return a linear interpolation
      through Queyroux Table S1's 12 measured points over 8.4–44.7 GPa (the two 16.6 GPa
      points averaged to 937 K); outside the window the dispatch is untouched
- [x] Experiment sweep: same runner, same bodies → JSON; diff the two files
- [x] Write the note section: which verdicts flip, which don't, and how far each body's
      water column sits from the swapped window
- [x] Remove the worktree; nothing committed from it
- [x] Report to the directing session
