# `ONDISCOVERY` — per-body discovery message

`ONDISCOVERY` is a **subnode of `RESEARCHBODIES`**. It maps a body name to
the screen message shown the moment the player discovers that body.

```
RESEARCHBODIES
{
    loadAs = mod          // MANDATORY for a third-party pack (see global-settings.md)
    ONDISCOVERY
    {
        Polyphemus = JWST/MIRI 15.5 um direct imaging picks out a faint companion to Alpha Centauri A — the candidate "S1". (Sanghi & Beichman 2025)
    }
}
```

## Schema (source-cited, JPLRepo/ResearchBodies v1.13.0.0)

| Fact | Value | Source |
|---|---|---|
| Node name | `ONDISCOVERY`, subnode of `RESEARCHBODIES` | `Database.cs:242` (master), `Database.cs:297` (mod node) |
| Key format | `<bodyName> = <message string>` | `Database.cs:242-245` |
| Body-name match | **substring `Contains`** against `CelestialBody.bodyName` | `Database.cs:244`, `Database.cs:299` |
| Value stored as | `CelestialBodyInfo.discoveryMessage` | field `CelestialBodyInfo.cs:25` |
| Default if absent | `"Now tracking <body> !"` | `CelestialBodyInfo.cs:39` |

## Authoring rules

- **Use the exact internal Kopernicus body name** (`CelestialBody.bodyName`
  / `GetName()`), NOT the in-game `displayName`. Match is case-sensitive.
- Because the match is substring `Contains`, avoid names that are
  substrings of another body's name (`Kerbin` ⊂ `Kerbinish` would mis-fire).
  NearStars in-game names are distinct, so this is normally fine — but do
  not, e.g., name a moon `Pan` if a planet `Pandora` exists.
- The message is **English here**; RB overwrites it via Localizer for
  other locales (`Database.cs:241`). NearStars ships English messages.
- A body with no `ONDISCOVERY` entry still works — it just gets the
  generic default message. So this node is **flavor**, not required for
  the hide/show mechanic (that is `IGNORELEVELS`).

## NearStars convention: cite the real detection

The discovery message is where NearStars' "real observation evidence"
identity lives. For a **candidate** body, the message should paraphrase
the actual detection and name the paper — e.g. Polyphemus
(= Alpha Centauri A b) cites Sanghi & Beichman 2025 (the JWST/MIRI
direct-imaging candidate). Pull the citation from the body's Phase 4
`discoverability` note / DB `sources[]` bibcode. Do not invent a paper.
For a **fictional** body (synthetic moon), the message is in-universe
flavor with no paper claim.
