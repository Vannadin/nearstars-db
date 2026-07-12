# 테스트 빌드용 placeholder 항성 텍스처(sunspot/corona DDS)를 생성하는 스크립트
"""Generate placeholder star textures referenced by Kopernicus star bodies.

`emit_kopernicus_cfg.py` writes Material/Coronas texture paths of the form
`NearStars-Textures/PluginData/<Body>/Kopernicus/<Body>_{Sunspots,Corona}.dds`.
Until real art exists, a test build still needs *some* file at those paths or
Kopernicus' star shader gets a null noiseMap. This writes uncompressed
A8R8G8B8 DDS stand-ins:

  * `<Body>_Sunspots.dds` — flat white, opaque (a spotless photosphere)
  * `<Body>_Corona.dds`   — white with a radial alpha falloff

Body names are read from the emitted `stars.cfg`, so the two stay in sync.
"""

import argparse
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STARS_CFG = ROOT / "dist/NearStars-Configs/Patches/Kopernicus/stars.cfg"
TEX_ROOT = ROOT / "dist/NearStars-Textures/PluginData"
SIZE = 64


def dds_bytes(pixels: bytes, width: int, height: int) -> bytes:
    """Uncompressed 32-bit DDS (DDPF_RGB | DDPF_ALPHAPIXELS, BGRA byte order)."""
    header = struct.pack(
        "<4sIIIIIII44sIIIIIIIIIIIII",
        b"DDS ",
        124,  # dwSize
        0x0000100F,  # CAPS | HEIGHT | WIDTH | PITCH | PIXELFORMAT
        height,
        width,
        width * 4,  # pitch
        0,  # depth
        0,  # mipmap count
        b"\0" * 44,  # reserved
        32,  # pixelformat dwSize
        0x41,  # DDPF_RGB | DDPF_ALPHAPIXELS
        0,  # fourCC
        32,  # RGB bit count
        0x00FF0000,  # R mask
        0x0000FF00,  # G mask
        0x000000FF,  # B mask
        0xFF000000,  # A mask
        0x1000,  # caps: DDSCAPS_TEXTURE
        0,
        0,
        0,
        0,  # caps2-4 + reserved2
    )
    return header + pixels


def solid_white(size: int) -> bytes:
    return bytes([255, 255, 255, 255]) * (size * size)


def radial_corona(size: int) -> bytes:
    """White RGB, alpha fading from centre to edge."""
    out = bytearray()
    c = (size - 1) / 2
    for y in range(size):
        for x in range(size):
            r = ((x - c) ** 2 + (y - c) ** 2) ** 0.5 / c
            a = max(0.0, 1.0 - r)
            out += bytes([255, 255, 255, int(255 * a * a)])
    return bytes(out)


def body_names(cfg: Path) -> list[str]:
    text = cfg.read_text()
    return re.findall(r"^\s+identifier = NearStars/(\w+)$", text, re.M)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--stars-cfg", type=Path, default=STARS_CFG)
    ap.add_argument("--output", type=Path, default=TEX_ROOT)
    args = ap.parse_args()

    if not args.stars_cfg.exists():
        raise SystemExit(f"missing {args.stars_cfg} — run emit_kopernicus_cfg.py first")

    names = body_names(args.stars_cfg)
    if not names:
        raise SystemExit(f"no star bodies found in {args.stars_cfg}")

    sunspots = dds_bytes(solid_white(SIZE), SIZE, SIZE)
    corona = dds_bytes(radial_corona(SIZE), SIZE, SIZE)

    for name in names:
        d = args.output / name / "Kopernicus"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{name}_Sunspots.dds").write_bytes(sunspots)
        (d / f"{name}_Corona.dds").write_bytes(corona)
        print(f"  {name}: Sunspots.dds + Corona.dds")

    print(f"wrote {2 * len(names)} placeholder textures under {args.output}")


if __name__ == "__main__":
    main()
