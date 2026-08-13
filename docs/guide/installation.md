<!-- 설치 방법과 모드 호환성 -->
# Installation & Compatibility

> **NearStars is not released yet.** There is nothing to download today. This page describes the *planned* mod stack so you can see where it will fit, and details may still change before release.

## Target platform

NearStars targets **KSP 1.12.x on Windows**, running on a Real Solar System install based on [Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs). It adds star systems on top of the real Sol system; it does not replace the stock system on its own.

## Planned dependency stack

The mod leans on the established RSS visual and structural stack rather than reinventing it:

| Layer | Mod | Role |
|---|---|---|
| Core | [Kopernicus](https://github.com/Kopernicus/Kopernicus) | adds the stars, planets, and moons (~50 ly range) |
| Base | [Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs) | the real solar system NearStars extends |
| Visuals | Scatterer, EVE, [Firefly](https://forum.kerbalspaceprogram.com/topic/219890-firefly/) | atmospheres, clouds, physically-grounded re-entry plasma colors |

## Two physics profiles (planned)

Interstellar travel and n-body gravity pull in opposite directions, so NearStars plans to ship **two install profiles** instead of pretending one covers both:

- **Principia profile**, with full n-body gravity. Binary stars genuinely orbit their barycenters, and the mod's orbital solutions are built for exactly this. The catch is honest physics: travel between stars becomes a multi-generation undertaking.
- **Warp/endgame profile**, with stock gravity plus SigmaBinary for binary motion, compatible with warp-drive mods for practical interstellar gameplay.

You install one or the other, and configs are generated for both.

## Optional integrations (planned)

Beyond the core stack, several mods can deepen the experience if you run them:

- **Kerbalism** gets per-star radiation environments derived from measured X-ray luminosities and stellar activity.
- **ResearchBodies** maps discovery difficulty to each body's real detection history, so a telescopically-discovered planet has to be found before you can target it.
- **RP-1** support is planned once the upstream Sol-Configs RP-1 bridge lands; NearStars stays Sol-based and will ride that bridge rather than fork.

## License

CC-BY-NC-SA 4.0. Third-party data attributions ship in [NOTICE](https://github.com/Vannadin/nearstars-db/blob/main/NOTICE).
