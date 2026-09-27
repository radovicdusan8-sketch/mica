#!/usr/bin/env python3
"""Validate Wraith's dialogue sheet and export Unreal Data Table files.

The master sheet is a UTF-8 CSV downloaded from Google Sheets or saved from
LibreOffice Calc. See docs/walkthroughs/02-story-and-dialogue-pipeline.md.

Usage, from the repo root:
    python tools/dialogue/dialogue_tool.py validate
    python tools/dialogue/dialogue_tool.py export
    python tools/dialogue/dialogue_tool.py report

Options:
    --master PATH    master CSV (default docs/story/dialogue/dialogue_master.csv)
    --speakers PATH  speakers CSV (default docs/story/dialogue/speakers.csv)
    --out DIR        export folder (default docs/story/dialogue/build)

Exit code is 1 when validation finds errors. Only the Python standard
library is used, so any Python 3.9+ works.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DIALOGUE_DIR = REPO_ROOT / "docs" / "story" / "dialogue"
VOICE_DIR = REPO_ROOT / "audio" / "voice" / "ja"

MASTER_COLUMNS = ["LineID", "SceneID", "Order", "Speaker", "TextJA", "TextEN",
                  "Direction", "Context", "Status", "Tags"]
SPEAKER_COLUMNS = ["SpeakerID", "NameEN", "NameJA", "IsDead", "Notes"]

# Workflow order: a line only moves forward through these.
STATUSES = ["Draft", "Locked", "Recorded", "Implemented"]

SCENE_LINE_RE = re.compile(r"^(D\d{2})_S\d{3}_\d{4}$")    # D01_S020_0030
BARK_RE = re.compile(r"^B_[A-Z0-9]+_[A-Z0-9]+_\d{2}$")     # B_WRAITH_HURT_01
SPEAKER_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")

# Subtitle guidelines from walkthrough 02. Tune them to taste.
MAX_SUBTITLE_CHARS = 84        # about two lines of 42 characters
MAX_CHARS_PER_SECOND = 20.0    # reading-speed warning threshold

TRUE_WORDS = {"true", "yes", "1"}
FALSE_WORDS = {"false", "no", "0"}


@dataclass
class Findings:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


def read_csv(path: Path, required: list[str]) -> list[dict[str, str]]:
    """Read a UTF-8 CSV (with or without BOM) and check its header."""
    if not path.exists():
        sys.exit(f"Missing file: {path}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = [name.strip() for name in (reader.fieldnames or [])]
        missing = [name for name in required if name not in header]
        if missing:
            sys.exit(f"{path}: missing column(s): {', '.join(missing)}")
        rows = []
        for raw in reader:
            rows.append({(k or "").strip(): (v or "") for k, v in raw.items()})
        return rows


def shown(path: Path) -> str:
    """Path relative to the repo root when possible, for readable messages."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def audio_folder(line_id: str) -> str:
    """D01_S020_0030 -> D01; barks -> Barks."""
    match = SCENE_LINE_RE.match(line_id)
    return match.group(1) if match else "Barks"


def sound_asset_path(line_id: str) -> str:
    folder = audio_folder(line_id)
    return f"/Game/Wraith/Audio/VO/{folder}/VO_{line_id}.VO_{line_id}"


def wav_path(line_id: str) -> Path:
    return VOICE_DIR / audio_folder(line_id) / f"VO_{line_id}.wav"


def wav_duration(path: Path) -> float | None:
    """Duration in seconds from the RIFF header (PCM, float, or extensible)."""
    try:
        with path.open("rb") as handle:
            riff = handle.read(12)
            if len(riff) < 12 or riff[0:4] != b"RIFF" or riff[8:12] != b"WAVE":
                return None
            byte_rate = 0
            while True:
                header = handle.read(8)
                if len(header) < 8:
                    return None
                chunk_id = header[0:4]
                size = int.from_bytes(header[4:8], "little")
                if chunk_id == b"fmt ":
                    fmt = handle.read(size)
                    byte_rate = int.from_bytes(fmt[8:12], "little")
                    if size % 2:
                        handle.read(1)
                elif chunk_id == b"data":
                    return size / byte_rate if byte_rate else None
                else:
                    handle.seek(size + (size % 2), 1)
    except OSError:
        return None


def parse_bool(value: str) -> bool | None:
    word = value.strip().lower()
    if word in TRUE_WORDS:
        return True
    if word in FALSE_WORDS:
        return False
    return None


def check_speakers(rows: list[dict[str, str]], found: Findings) -> dict[str, dict[str, str]]:
    speakers: dict[str, dict[str, str]] = {}
    for number, row in enumerate(rows, start=2):
        where = f"speakers.csv row {number}"
        speaker_id = row["SpeakerID"].strip()
        if not SPEAKER_RE.match(speaker_id):
            found.error(where, f"SpeakerID '{speaker_id}' must be UPPER_CASE letters, digits, _")
            continue
        if speaker_id in speakers:
            found.error(where, f"duplicate SpeakerID '{speaker_id}'")
            continue
        if not row["NameEN"].strip():
            found.error(where, f"{speaker_id} has no NameEN")
        if parse_bool(row["IsDead"]) is None:
            found.warn(where, f"{speaker_id}: IsDead not set (true/false); treated as false")
        speakers[speaker_id] = row
    return speakers


def check_lines(rows: list[dict[str, str]], speakers: dict[str, dict[str, str]],
                found: Findings) -> None:
    seen: dict[str, int] = {}
    scene_orders: dict[tuple[str, str], str] = {}
    for number, row in enumerate(rows, start=2):
        line_id = row["LineID"].strip()
        where = f"row {number} ({line_id or 'no LineID'})"

        if not line_id:
            found.error(where, "empty LineID")
            continue
        if line_id in seen:
            found.error(where, f"duplicate LineID, first used on row {seen[line_id]}")
            continue
        seen[line_id] = number

        is_scene_line = bool(SCENE_LINE_RE.match(line_id))
        if not is_scene_line and not BARK_RE.match(line_id):
            found.error(where, "LineID must look like D01_S020_0030 or B_WRAITH_HURT_01")

        scene_id = row["SceneID"].strip()
        if is_scene_line and scene_id != line_id[:8]:
            found.error(where, f"SceneID '{scene_id}' should be '{line_id[:8]}'")

        order = row["Order"].strip()
        if is_scene_line:
            if not order.isdigit():
                found.error(where, "Order must be a whole number")
            elif (scene_id, order) in scene_orders:
                found.warn(where, f"same Order as {scene_orders[(scene_id, order)]}")
            else:
                scene_orders[(scene_id, order)] = line_id

        speaker = row["Speaker"].strip()
        if speaker not in speakers:
            found.error(where, f"unknown Speaker '{speaker}' (add it to speakers.csv)")

        status = row["Status"].strip()
        if status not in STATUSES:
            found.error(where, f"Status '{status}' must be one of {', '.join(STATUSES)}")
            continue
        stage = STATUSES.index(status)

        text_ja = row["TextJA"].strip()
        text_en = row["TextEN"].strip()
        if stage >= STATUSES.index("Locked"):
            if not text_ja:
                found.error(where, f"{status} line has no TextJA")
            if not text_en:
                found.error(where, f"{status} line has no TextEN")
        if "\n" in text_en or "\r" in text_en:
            found.error(where, "TextEN contains a line break; let the subtitle widget wrap")
        if len(text_en) > MAX_SUBTITLE_CHARS:
            found.warn(where, f"subtitle is {len(text_en)} characters "
                              f"(guideline {MAX_SUBTITLE_CHARS}); consider splitting the line")

        wav = wav_path(line_id)
        if wav.exists():
            if stage < STATUSES.index("Recorded"):
                found.warn(where, f"audio exists but Status is {status}")
            duration = wav_duration(wav)
            if duration is None:
                found.warn(where, f"could not read WAV header: {shown(wav)}")
            elif duration > 0 and text_en:
                speed = len(text_en) / duration
                if speed > MAX_CHARS_PER_SECOND:
                    found.warn(where, f"subtitle reading speed {speed:.1f} chars/s over "
                                      f"{duration:.2f}s of audio (guideline "
                                      f"{MAX_CHARS_PER_SECOND:.0f}); hold it longer or shorten it")
        elif stage >= STATUSES.index("Recorded"):
            found.error(where, f"Status is {status} but {shown(wav)} is missing")


def validate(master: Path, speakers_path: Path) -> tuple[Findings, list[dict[str, str]],
                                                         dict[str, dict[str, str]]]:
    found = Findings()
    speakers = check_speakers(read_csv(speakers_path, SPEAKER_COLUMNS), found)
    lines = read_csv(master, MASTER_COLUMNS)
    check_lines(lines, speakers, found)
    return found, lines, speakers


def print_findings(found: Findings) -> None:
    for message in found.errors:
        print(f"ERROR   {message}")
    for message in found.warnings:
        print(f"warning {message}")
    print(f"{len(found.errors)} error(s), {len(found.warnings)} warning(s)")


def export(lines: list[dict[str, str]], speakers: dict[str, dict[str, str]], out: Path) -> None:
    """Write JSON files that Unreal can import into Data Tables.

    Text columns are plain strings. On import, Unreal gives each FText a stable
    localization key built from the row name and property name (for example
    D01_S020_0030_Subtitle in namespace DT_Dialogue), so never rename rows or
    the Data Table assets once translation starts. JSON is written with ASCII
    escapes (\\uXXXX) for Japanese text, which keeps the file plain ASCII.
    """
    out.mkdir(parents=True, exist_ok=True)
    dialogue_rows = []
    # Scene lines first (in script order), then barks.
    def sort_key(row: dict[str, str]) -> tuple[bool, str]:
        line_id = row["LineID"].strip()
        return (not SCENE_LINE_RE.match(line_id), line_id)

    for row in sorted(lines, key=sort_key):
        line_id = row["LineID"].strip()
        order = row["Order"].strip()
        dialogue_rows.append({
            "Name": line_id,
            "SceneId": row["SceneID"].strip(),
            "Order": int(order) if order.isdigit() else 0,
            "Speaker": row["Speaker"].strip(),
            "SpokenJA": row["TextJA"].strip(),
            "Subtitle": row["TextEN"].strip(),
            "Audio": sound_asset_path(line_id) if wav_path(line_id).exists() else "",
        })
    speaker_rows = []
    for speaker_id, row in sorted(speakers.items()):
        speaker_rows.append({
            "Name": speaker_id,
            "DisplayName": row["NameEN"].strip(),
            "bIsDead": bool(parse_bool(row["IsDead"])),
        })
    for name, data in (("DT_Dialogue.json", dialogue_rows), ("DT_Speakers.json", speaker_rows)):
        target = out / name
        target.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {shown(target)} ({len(data)} rows)")


def report(lines: list[dict[str, str]]) -> None:
    """Counts that help with planning recording sessions."""
    by_status = Counter(row["Status"].strip() for row in lines)
    by_scene: dict[str, Counter] = defaultdict(Counter)
    ja_chars_by_speaker: Counter = Counter()
    lines_by_speaker: Counter = Counter()
    for row in lines:
        scene = row["SceneID"].strip() or "(barks)"
        by_scene[scene][row["Status"].strip()] += 1
        speaker = row["Speaker"].strip()
        lines_by_speaker[speaker] += 1
        ja_chars_by_speaker[speaker] += len(row["TextJA"].strip())
    print(f"{len(lines)} lines: " + ", ".join(f"{s} {by_status.get(s, 0)}" for s in STATUSES))
    print("\nBy scene:")
    for scene in sorted(by_scene):
        counts = by_scene[scene]
        print(f"  {scene:<10} " + "  ".join(f"{s} {counts.get(s, 0)}" for s in STATUSES))
    print("\nBy speaker (lines, Japanese characters):")
    for speaker, count in lines_by_speaker.most_common():
        print(f"  {speaker:<10} {count:>5} lines  {ja_chars_by_speaker[speaker]:>7} chars")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["validate", "export", "report"])
    parser.add_argument("--master", type=Path, default=DIALOGUE_DIR / "dialogue_master.csv")
    parser.add_argument("--speakers", type=Path, default=DIALOGUE_DIR / "speakers.csv")
    parser.add_argument("--out", type=Path, default=DIALOGUE_DIR / "build")
    args = parser.parse_args()

    found, lines, speakers = validate(args.master, args.speakers)
    if args.command == "report":
        report(lines)
        return 0
    print_findings(found)
    if found.errors:
        return 1
    if args.command == "export":
        export(lines, speakers, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
