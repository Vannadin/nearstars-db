# PrincipiaWarpBridge — warp-mod detection micro-bridge

A single-file KSP 1.12.5 plugin that lets **Blueshift** and **KSP Interstellar
Extended** warp drives work under the NearStars **Principia fork** without
modifying either mod.

## How it works

The fork ships a warp release channel: a `PrincipiaWarpStatus` VesselModule
(auto-attached to every vessel) whose `warpEngaged` flag, while asserted every
frame, makes Principia release the vessel; ~10 s after the last assertion the
flag decays and Principia re-adopts the vessel from its current stock orbit
(dead man's switch — see `warp_status.cs` in the fork).

The mods do not know that channel exists. This bridge closes the gap from our
side: each FixedUpdate it scans loaded vessels for an **engaged** warp drive
and asserts the flag on the vessel's behalf:

- **Blueshift** (`Blueshift.WBIWarpEngine`): engine ignited, throttled up, and
  the engine's own precondition census true (`isInSpace`,
  `meetsWarpAltitude`, `hasWarpCapacity`) — i.e. exactly when Blueshift moves
  the vessel.
- **KSPIE** (`FNPlugin.Propulsion.AlcubierreDrive`): `IsEnabled` true (engaged
  cruise; the charging phase deliberately does not release).

All three mods are reached **by reflection only** — no compile dependency in
either direction. Fail-soft by construction: an absent mod disables its
detector, an absent Principia fork leaves the bridge inert, and a bridge
failure mid-cruise merely lets the dead man's switch re-adopt the vessel.

The direct channel stays first-class: a warp mod that asserts `warpEngaged`
itself needs no bridge, and this plugin then simply re-asserts harmlessly.

## Build & install

```
dotnet build PrincipiaWarpBridge.csproj -c Release [-p:KSPManaged=<KSP>\KSP_x64_Data\Managed]
```

Copy `bin/Release/PrincipiaWarpBridge.dll` to
`GameData/PrincipiaWarpBridge/PrincipiaWarpBridge.dll`.

On load, `KSP.log` prints one summary line
(`[PrincipiaWarpBridge] Principia release channel found; Blueshift detected; …`)
and logs each warp engage/end transition per vessel.

## Scope

Only these two mods, by owner decision (2026-08-01): the generic path for any
other warp mod remains the channel itself (assert `warpEngaged` by name via
reflection, one line on the mod side). The old `plugins/NearStarsWarp/` draft
(own cruise layer) is a retired premise and is unrelated to this bridge.
