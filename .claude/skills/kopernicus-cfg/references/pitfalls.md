# Common Pitfalls

| Problem | Root Cause | Fix |
|---------|-----------|-----|
| Body doesn't appear in game | `flightGlobalsIndex` collision with another mod | Check all loaded mods; each body needs a globally unique index |
| Body appears at wrong position | Epoch mismatch | Set `epoch = 0` in `Sol-KopernicusSettings.cfg` via `@Kopernicus { @name = Sol }` |
| PQS terrain flickers when descending | `deactivateAltitude` ≤ `fadeEnd` | Set `deactivateAltitude` > `fadeEnd` (e.g., fadeEnd=117000 → deactivate=120000) |
| ScaledSpace mesh corrupted/blocky | Stale `.bin` cache from old mesh | Delete `GameData/Kopernicus/Cache/<BodyName>.bin` |
| Star has no light/shadows | Missing `Light {}` inside `ScaledVersion`, or `givesOffLight = False` | Add `Light {}` block with at least `givesOffLight = True` |
| Star light wrong color | `sunlightColor` vs `scaledSunlightColor` mismatch | Set both; `sunlightColor` = localspace, `scaledSunlightColor` = map view |
| Atmosphere visible but sky wrong color | Scatterer config missing | Create `[Body]-Scatterer.cfg` with `Scatterer_atmosphere` node |
| Parallax terrain invisible | `Parallax {}` mod missing from `PQS.Mods` | Add `Parallax { subdivisionLevel = 8 … }` to `PQS.Mods` |
| Biome map not working | Wrong color values — biomes use only the R channel (cyan spectrum) | Colors must be `RGBA(n,255,255,255)` where n varies per biome |
| Orbit icon missing | `iconTexture` path wrong or file missing | Verify `.png` exists at the exact path; Kopernicus is case-sensitive on Linux |
| Body loads but has no terrain | `Template.removeAllPQSMods = True` without a replacement `PQS {}` block | Add a `PQS {}` block or set `removeAllPQSMods = False` |
| `NEEDS[]` patch silently skipped | Mod name in `NEEDS[]` doesn't match MM's registered name | Check the mod's own `FOR[X]` pass name; it must match exactly |
| Planet too bright / too dark | `albedoBrightness` in PQS Material too high/low | Tune `albedoBrightness` (1.0 = neutral); also check `ScaledVersion.Material.color` |
| Body silently loses its atmosphere | `temperatureEccentricityBiasCurve` on a circular orbit → `(ApR−PeR)=0` → divide-by-zero | Only emit that curve when orbital eccentricity is above a threshold (e ≳ 0.02–0.05); never on default-circular bodies. See `atmosphere.md` "Temperature over the orbit" |
