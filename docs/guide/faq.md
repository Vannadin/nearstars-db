<!-- 자주 묻는 질문 -->
# FAQ

**When does it release?**
No date yet. The project deliberately finishes the data and design work before generating any KSP configs, because that config-generation step is deterministic once the database freezes. "Data complete" is the milestone that matters, so watch the repo for news.

**Is the astronomy real?**
Yes, and that is the founding rule. Every measurement in the database cites the paper or catalog it came from, and synthesized values (a surface color no telescope has seen, for instance) are documented decision by decision against published constraints. See [Data & Methodology](data-and-methodology.md) for the full picture.

**Then what are the "(fiction)" bodies?**
A handful of filler bodies added for gameplay variety where reality left a gap. Each has to clear a plausibility gate (would published observations have ruled it out, and is the orbit dynamically stable?) and stays flagged as fictional in-game. The real/fiction boundary is never blurred.

**Is this REX (Real Exoplanets)?**
No, but it chases the same dream. NearStars is a from-scratch spiritual successor to the KSP 1.8-era REX concept of flying from a real Sol system to real nearby stars, rebuilt around a curated evidence database and full Principia compatibility.

**Do I need Principia?**
No. Two profiles are planned: a Principia n-body profile where binaries truly orbit (the flagship experience), and a stock-gravity profile (SigmaBinary plus warp-mod friendly) for practical interstellar play. See [Installation & Compatibility](installation.md).

**Will it work with RP-1?**
Planned, eventually. RP-1 currently targets classic RSS, and a Sol-Configs-compatible RP-1 build is in progress upstream. NearStars will provide its career layer on top of that bridge once it lands.

**Why are some planets marked "(disputed)"?**
Because the papers dispute them. Where a detection is debated (40 Eridani A b, or some tau Ceti candidates), the mod keeps it for variety and says so plainly, rather than silently including or excluding it. Fully retracted detections are excluded.

**Can I use the data?**
Yes, under **CC-BY-NC-SA 4.0**: attribution, non-commercial, share-alike. The per-measurement citations also make it a decent starting bibliography for any nearby-stars project.

**How were the 7 systems chosen?**
From the 145-system research database, by distance, planet inventory, cultural recognition, and stellar variety. The roster deliberately spans G/K/M dwarfs, a white dwarf, an A star with a debris ring, and a brown-dwarf binary.

**Where can I see the data now?**
The [live viewer](https://vannadin.github.io/nearstars-db/) (full database plus 3D star map) and the [curation reports](https://vannadin.github.io/nearstars-db/reports.html) are already public.
