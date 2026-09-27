#!/usr/bin/env python3
"""Make Unreal color-grading LUT textures (walkthrough 07).

Unreal's Color Grading LUT is a 16x16x16 color table unwrapped into a
256x16 image: 16 slices side by side, blue increasing per slice, red
increasing left to right inside a slice, green increasing top to bottom.

Usage:
    python tools/art/lut_tool.py neutral LUT_Neutral.png
        Writes the identity LUT, the starting point for grading.

    python tools/art/lut_tool.py from-cube Grade.cube LUT_Grade.png
        Converts a 3D .cube LUT (for example one exported from
        DaVinci Resolve with "Generate LUT") into Unreal's layout.

Requires Pillow (pip install pillow).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is missing. Install it with: pip install pillow")

SIZE = 16  # Unreal's LUT is 16x16x16


def neutral_image() -> Image.Image:
    image = Image.new("RGB", (SIZE * SIZE, SIZE))
    pixels = image.load()
    for green in range(SIZE):
        for x in range(SIZE * SIZE):
            blue, red = divmod(x, SIZE)
            pixels[x, green] = tuple(round(v * 255 / (SIZE - 1)) for v in (red, green, blue))
    return image


def read_cube(path: Path) -> tuple[int, list[tuple[float, float, float]], tuple[float, ...], tuple[float, ...]]:
    """Parse a .cube file: returns size, table (red fastest), domain min, domain max."""
    size = 0
    table: list[tuple[float, float, float]] = []
    domain_min: tuple[float, ...] = (0.0, 0.0, 0.0)
    domain_max: tuple[float, ...] = (1.0, 1.0, 1.0)
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        keyword = line.split()[0].upper()
        if keyword == "TITLE":
            continue
        if keyword == "LUT_1D_SIZE":
            sys.exit(f"{path}: 1D LUTs are not supported; export a 3D LUT")
        if keyword == "LUT_3D_SIZE":
            size = int(line.split()[1])
            continue
        if keyword == "DOMAIN_MIN":
            domain_min = tuple(float(v) for v in line.split()[1:4])
            continue
        if keyword == "DOMAIN_MAX":
            domain_max = tuple(float(v) for v in line.split()[1:4])
            continue
        values = line.split()
        if len(values) == 3:
            table.append((float(values[0]), float(values[1]), float(values[2])))
    if size < 2:
        sys.exit(f"{path}: missing or invalid LUT_3D_SIZE")
    if len(table) != size ** 3:
        sys.exit(f"{path}: expected {size ** 3} entries for size {size}, found {len(table)}")
    return size, table, domain_min, domain_max


def sample(size: int, table: list[tuple[float, float, float]], rgb: tuple[float, float, float],
           domain_min: tuple[float, ...], domain_max: tuple[float, ...]) -> tuple[float, float, float]:
    """Trilinear lookup of an input color in the .cube table."""
    coords = []
    for channel in range(3):
        span = domain_max[channel] - domain_min[channel]
        position = (rgb[channel] - domain_min[channel]) / span * (size - 1)
        position = min(max(position, 0.0), size - 1.0)
        low = min(int(position), size - 2)
        coords.append((low, position - low))
    (r0, fr), (g0, fg), (b0, fb) = coords

    def entry(r: int, g: int, b: int) -> tuple[float, float, float]:
        return table[r + g * size + b * size * size]

    result = [0.0, 0.0, 0.0]
    for dr, wr in ((0, 1 - fr), (1, fr)):
        for dg, wg in ((0, 1 - fg), (1, fg)):
            for db, wb in ((0, 1 - fb), (1, fb)):
                weight = wr * wg * wb
                if weight == 0.0:
                    continue
                value = entry(r0 + dr, g0 + dg, b0 + db)
                for channel in range(3):
                    result[channel] += weight * value[channel]
    return result[0], result[1], result[2]


def cube_image(path: Path) -> Image.Image:
    size, table, domain_min, domain_max = read_cube(path)
    image = Image.new("RGB", (SIZE * SIZE, SIZE))
    pixels = image.load()
    for green in range(SIZE):
        for x in range(SIZE * SIZE):
            blue, red = divmod(x, SIZE)
            source = tuple(v / (SIZE - 1) for v in (red, green, blue))
            graded = sample(size, table, source, domain_min, domain_max)
            pixels[x, green] = tuple(round(min(max(v, 0.0), 1.0) * 255) for v in graded)
    return image


def main() -> int:
    parser = argparse.ArgumentParser(description="Make Unreal 256x16 color-grading LUT textures.")
    commands = parser.add_subparsers(dest="command", required=True)
    neutral = commands.add_parser("neutral", help="write the identity LUT")
    neutral.add_argument("output", type=Path)
    convert = commands.add_parser("from-cube", help="convert a 3D .cube LUT")
    convert.add_argument("cube", type=Path)
    convert.add_argument("output", type=Path)
    args = parser.parse_args()

    image = neutral_image() if args.command == "neutral" else cube_image(args.cube)
    image.save(args.output)
    print(f"wrote {args.output} ({image.size[0]}x{image.size[1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
