# `IGNORELEVELS` — per-body start-visibility by difficulty

`IGNORELEVELS` is a **subnode of `RESEARCHBODIES`**. It decides, per
difficulty level, whether a body is **already visible at game start**
(`true`) or **hidden until discovered** via telescope/observatory
(`false`). This is the actual hide/show mechanic.

```
RESEARCHBODIES
{
    loadAs = mod
    IGNORELEVELS
    {
        // body = easy normal medium hard
        AlphaCentauriA = true true true true     // naked_eye star: always visible
        Polyphemus     = true false false false   // candidate planet: Easy shows, else discover (see db-mapping.md)
    }
}
```

## Schema (source-cited, v1.13.0.0)

| Fact | Value | Source |
|---|---|---|
| Node name | `IGNORELEVELS`, subnode of `RESEARCHBODIES` | `Database.cs:251` (master), `Database.cs:334` (mod node) |
| Value format | **exactly 4 space-separated booleans** `true`/`false` | `Database.cs:258-259` (`split " "`, `bool.Parse(args[0..3])`) |
| Order | **Easy, Normal, Medium, Hard** | ctor `BodyIgnoreData(bool easy, bool normal, bool medium, bool hard)` `BodyIgnoreData.cs:19-20` |
| Body-name match | **exact `==`** against `GetName()`/`bodyName` | `Database.cs:255`, `Database.cs:338` |
| Meaning of `true` | body is **pre-discovered / visible at start** for that difficulty (`isResearched=true, researchState=100`) | `Database.cs:362-367` |
| Meaning of `false` | body is **hidden**, must be discovered | same |
| Selection | only the column for the player's chosen difficulty is read | `BodyIgnoreData.GetLevel(Level)` `BodyIgnoreData.cs:36-55`; `Database.cs:362` |
| **Default if absent** | `(false,false,false,false)` → **hidden at every difficulty** | `CelestialBodyInfo.cs:40` |
| Difficulty enum | `Level { Easy=0, Normal=1, Medium=2, Hard=3 }` (stock "Moderate"→Medium) | `RBEnums.cs:17-23`, `SettingsParms.cs:64-93` |

## Hard rules (will crash/throw otherwise)

- **Exactly 4 tokens.** Fewer than 4 → `bool.Parse` on a missing index
  throws (`Database.cs:259`).
- **`true`/`false` only.** `1`/`0` are NOT valid — `bool.Parse` throws.
- **Silence = hidden.** If you want a body visible at any difficulty you
  MUST write an explicit `IGNORELEVELS` line; omitting it hides the body
  at all four levels.

## Typical grading

More `true`s on the left (Easy) → easier games start with more bodies
visible; harder games make you discover more. The stock pattern grades
outer/harder bodies off from the right (`database.cfg`: `Minmus =
true true true false`, `Duna = true true false false`, `Laythe =
true false false false`). NearStars grades by **real detection status**
— see `db-mapping.md`.
