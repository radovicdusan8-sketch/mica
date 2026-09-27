# Story folder

How the story documents are organized and how every spoken line gets a permanent ID. The step-by-step pipeline, from script to a line playing in Unreal, is in [walkthrough 02](../walkthroughs/02-story-and-dialogue-pipeline.md).

## Layout

```text
docs/story/
  README.md                      this file
  wraith-story-bible-v2.md       the story bible: world, characters, districts, timeline
  scene-index.md                 one row per scene: ID, district, type, status
  scenes/                        one Markdown file per scene, named <SceneID>_<slug>.md
  dialogue/
    speakers.csv                 speaker IDs, display names, living or dead
    dialogue_master.csv          every spoken line, downloaded from the dialogue sheet
    dialogue_master.example.csv  format example; delete the EXAMPLE rows once real lines exist
    build/                       JSON written by tools/dialogue/dialogue_tool.py; don't edit by hand
```

## IDs

| What | Format | Example |
|---|---|---|
| District | `D` + 2 digits. `D00` is the cold open and prologue. | `D01` |
| Scene | district + `_S` + 3 digits, numbered in steps of 10 | `D01_S020` |
| Scene line | scene + `_` + 4 digits, numbered in steps of 10 | `D01_S020_0030` |
| Bark (short combat or ambient line) | `B_` + speaker + `_` + event + `_` + 2 digits | `B_WRAITH_HURT_01` |
| Speaker | UPPER_CASE, listed in `dialogue/speakers.csv` | `VESPER` |

Rules:

- **IDs are permanent.** Never renumber or reuse one. If a line is cut, delete its row and leave the gap.
- Number in steps of 10 so new lines fit between old ones (`0015` goes between `0010` and `0020`).
- The line ID is also the name of the voice file (`VO_D01_S020_0030.wav`), the Data Table row, and the subtitle's localization key. That's why it must never change.

## Scene script format

One file per scene. Every spoken line starts with its ID in square brackets, then the speaker, then the Japanese line, with the English subtitle on the next line:

```markdown
# D00_S010: Cold open

**Where:** ...  **When:** ...  **Who:** WRAITH

> Stage direction in a quote block.

[D00_S010_0010] WRAITH: 灯りが消えた。
EN: The lantern has gone out.
DIRECTION: Quiet, flat.
```

The lines above are a format example, not script. Walkthrough 02 explains each field and how the lines get into the dialogue sheet.
