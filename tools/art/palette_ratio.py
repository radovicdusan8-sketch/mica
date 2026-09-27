#!/usr/bin/env python3
"""Measure an image against Wraith's palette ratio (README, section 3).

Targets: about 70% darkness and stone, 20% warm lantern light, 10% violet.
Use it on concept art (walkthrough 03) and in-game screenshots (walkthrough 07).

Each pixel is put in one bucket:
  dark     low-value or low-saturation colors: night, stone, fog
  bright   bright low-saturation colors: lit snow, porcelain, highlights
  warm     saturated lantern-gold hues (the living)
  violet   saturated spirit-violet hues (the dead)
"dark" + "bright" together make the ~70% base.

Usage:
    python tools/art/palette_ratio.py shot.png
    python tools/art/palette_ratio.py shot.png --mask shot_mask.png

Requires Pillow (pip install pillow). The thresholds below are starting
points; adjust them if the buckets don't match what your eye sees.
"""

from __future__ import annotations

import argparse
import colorsys
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is missing. Install it with: pip install pillow")

WARM_HUE = (15.0, 55.0)       # degrees; Lantern gold #E0A24A is about 35
VIOLET_HUE = (245.0, 300.0)   # degrees; Spirit violet #9B6BFF is about 260
WARM_MIN_SAT, WARM_MIN_VALUE = 0.35, 0.25
VIOLET_MIN_SAT, VIOLET_MIN_VALUE = 0.25, 0.15
BRIGHT_MIN_VALUE = 0.60        # snow and porcelain; Porcelain #D8CCB8 is about 0.85

TARGETS = {"base": 70.0, "warm": 20.0, "violet": 10.0}
MASK_COLORS = {
    "dark": (40, 40, 48),
    "bright": (200, 200, 200),
    "warm": (224, 162, 74),     # Lantern gold
    "violet": (155, 107, 255),  # Spirit violet
}


def classify(rgb: tuple[int, int, int]) -> str:
    hue, sat, value = colorsys.rgb_to_hsv(*(channel / 255.0 for channel in rgb))
    degrees = hue * 360.0
    if sat >= WARM_MIN_SAT and value >= WARM_MIN_VALUE and WARM_HUE[0] <= degrees <= WARM_HUE[1]:
        return "warm"
    if (sat >= VIOLET_MIN_SAT and value >= VIOLET_MIN_VALUE
            and VIOLET_HUE[0] <= degrees <= VIOLET_HUE[1]):
        return "violet"
    if value >= BRIGHT_MIN_VALUE and sat < WARM_MIN_SAT:
        return "bright"
    return "dark"


def load(path: Path, max_size: int) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size))
    return image


def measure(image: Image.Image) -> tuple[dict[str, float], dict[tuple[int, int, int], str]]:
    width, height = image.size
    buckets = {name: 0 for name in MASK_COLORS}
    lookup: dict[tuple[int, int, int], str] = {}
    # getcolors returns (count, color) pairs, so each distinct color is classified once.
    for count, color in image.getcolors(maxcolors=width * height):
        bucket = classify(color)
        lookup[color] = bucket
        buckets[bucket] += count
    total = float(width * height)
    return {name: 100.0 * count / total for name, count in buckets.items()}, lookup


def write_mask(image: Image.Image, lookup: dict[tuple[int, int, int], str], target: Path) -> None:
    mask = Image.new("RGB", image.size)
    # get_flattened_data replaces getdata in newer Pillow; fall back for older versions.
    pixels = image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()
    mask.putdata([MASK_COLORS[lookup[pixel]] for pixel in pixels])
    mask.save(target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check an image against Wraith's 70/20/10 palette ratio.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--mask", type=Path, help="also save a false-color image of the buckets")
    parser.add_argument("--max-size", type=int, default=960,
                        help="downscale so the longest side is at most this (default 960)")
    parser.add_argument("--tolerance", type=float, default=5.0,
                        help="percentage points allowed either side of a target (default 5)")
    args = parser.parse_args()

    image = load(args.image, args.max_size)
    shares, lookup = measure(image)
    base = shares["dark"] + shares["bright"]
    results = {"base": base, "warm": shares["warm"], "violet": shares["violet"]}

    print(f"{args.image.name} ({image.size[0]}x{image.size[1]} analysed)")
    labels = {
        "base": "Base: darkness, stone, snow",
        "warm": "Warm lantern light",
        "violet": "Spirit violet",
    }
    for key in ("base", "warm", "violet"):
        value, target = results[key], TARGETS[key]
        verdict = "ok" if abs(value - target) <= args.tolerance else "check"
        print(f"  {labels[key]:<30} {value:5.1f}%   target ~{target:.0f}%   {verdict}")
        if key == "base":
            print(f"    dark and stone               {shares['dark']:5.1f}%")
            print(f"    bright neutrals (snow)       {shares['bright']:5.1f}%")

    if args.mask:
        write_mask(image, lookup, args.mask)
        print(f"mask written to {args.mask}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
