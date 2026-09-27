# 00. Index

These walkthroughs are your production manual for *Wraith: The Black Hour*, from an empty folder to a Steam release. They're written for this game, this developer (experienced programmer, new to game development, solo, part-time), and this PC (Windows 11, AMD Radeon RX 9060 XT 16 GB, no NVIDIA, no CUDA).

The running example throughout is the **vertical slice**: the cold open, the Lantern Market district, and the Sister Vesper boss fight. The milestone plan lives in [`../ROADMAP.md`](../ROADMAP.md), and project context lives in [`../../README.md`](../../README.md).

**Written:** September 2026, for Unreal Engine 5.8 (5.8.3 hotfix). Each walkthrough states the tool versions it was written for. Check those against what you have installed.

---

## All walkthroughs

| # | Walkthrough | What it covers | Status |
|---|---|---|---|
| 00 | [Index](00-index.md) | This page: the list, the learning order, and the conventions | Written (batch 1) |
| 01 | [Project setup](01-project-setup.md) | Unreal and Visual Studio, the `WraithGame` C++ project, folders, version control (Perforce vs. Git LFS), Claude Code, and the Blender and Unreal MCPs, each with a test task | Written (batch 1) |
| 02 | [Story and dialogue pipeline](02-story-and-dialogue-pipeline.md) | Organizing the story bible and scene scripts, the dialogue spreadsheet, importing it as a Data Table, and linking lines to audio and subtitles | Written (batch 2) |
| 03 | [Concept art](03-concept-art.md) | Consistent AI-assisted concept art, character reference sheets, Krita paintovers, turnarounds for modeling, and a reference library | Written (batch 2) |
| 04 | [Characters](04-characters.md) | Modeling in Blender, Wraith's cloak in Marvelous Designer, retopology, UVs, texturing, budgets, export to Unreal, and Chaos Cloth | Written (batch 2) |
| 05 | [Rigging and animation](05-rigging-and-animation.md) | AccuRig or Rigify, phone mocap at home, Blender cleanup, Cascadeur combat animation, the IK Retargeter, Animation Blueprints, and root motion | Written (batch 2) |
| 06 | [Environments](06-environments.md) | Blockout, a modular gothic kit on a grid, Fab and Megascans, snow, frost, icicles, snowfall, deformable snow, a PCG distant city, and fog | Written (batch 2) |
| 07 | [Lighting and rendering](07-lighting-and-rendering.md) | Lumen at night, lantern lights, violet accents, volumetric fog, grading to the palette, TSR or FSR instead of DLSS, and scalability | Written (batch 2) |
| 08 | [Core combat](08-core-combat.md) | Movement, Enhanced Input, attack chains, launchers and air combos, dodge, grab, hit detection, hit-stop, Motion Warping, style rank, and game feel | Planned (batch 3) |
| 09 | [GAS and spirit switching](09-gameplay-ability-system-and-spirit-switching.md) | The Gameplay Ability System in C++, then swapping Warden spirits mid-combo while keeping combo state | Planned (batch 3) |
| 10 | [Lantern system](10-lantern-system.md) | Lit and dark zones, enemies that grow stronger in darkness, relighting, snuffers, and Sister Vesper | Planned (batch 3) |
| 11 | [Enemy AI and bosses](11-enemy-ai-and-bosses.md) | Behavior Trees vs. StateTree, Arkham-style turn-taking, the four archetypes, telegraphs, and Vesper's phases | Planned (batch 3) |
| 12 | [Cutscenes](12-cutscenes.md) | Sequencer, camera language, MetaHuman facial animation, letterboxing, seamless gameplay transitions, and building the cold open | Planned (batch 4) |
| 13 | [UI and HUD](13-ui-and-hud.md) | UMG, the HUD from the mockup, menus, controller and keyboard support, and subtitles | Planned (batch 4) |
| 14 | [VFX](14-vfx.md) | Niagara: shadow energy, hit sparks, violet cracks, spirit release, snowfall, and effect budgets | Planned (batch 4) |
| 15 | [Audio and voice](15-audio-and-voice.md) | SFX sourcing, Japanese voice lines in Reaper, Wraith's voice chain, MetaSounds vs. FMOD, music, and mixing | Planned (batch 4) |
| 16 | [Localization and subtitles](16-localization-and-subtitles.md) | Unreal's localization tools, string tables, English now and more languages later, and Japanese fonts | Planned (batch 4) |
| 17 | [Performance](17-performance.md) | Profiling, frame-rate targets, tuning for the RX 9060 XT and weaker PCs, and snow and fog performance traps | Planned (batch 5) |
| 18 | [Testing and playtesting](18-testing-and-playtesting.md) | Testing your own game without bias, friend and Steam playtests, what to watch for, feedback, and bug tracking | Planned (batch 5) |
| 19 | [Project management](19-project-management.md) | Part-time planning, milestones, a task board, estimating, scope creep, and a weekly routine | Planned (batch 5) |
| 20 | [Release and marketing](20-release-and-marketing.md) | Steam page timing, capsule art, trailers in DaVinci Resolve, devlogs, wishlists, demos, Next Fest, and a release checklist | Planned (batch 5) |

Links to planned walkthroughs stay broken until their batch is written.

---

## Recommended learning order

The numbers group walkthroughs by production area, so you can read them front to back like a book. The order you **work** through them is different, because the roadmap requires combat to be fun with gray boxes before any art exists. Use this order:

### Milestone 1: Setup
1. **01 Project setup**, all of it.
2. **19 Project management**, only the task board, hours log, and weekly routine. It's about an evening's work and it pays off for years.
3. **02 Story and dialogue pipeline**, first step only: put the story bible and scene scripts into `docs/story/`.

### Milestone 2: Gray-box combat prototype
4. **08 Core combat**: movement, input, attacks, and feel.
5. **05 Rigging and animation**: only the Animation Blueprint, root motion, and retargeting sections, since combat needs them with placeholder animations.
6. **09 GAS and spirit switching**.
7. **11 Enemy AI and bosses**: attack tokens and two archetypes only.
8. **10 Lantern system**: the prototype steps.
9. **06 Environments**: only the blockout section, for a gray-box arena.
10. **13 UI and HUD**: only a debug HUD.
11. **18 Testing and playtesting**: your first outside playtest.

### Milestone 3: Vertical slice
12. **02** Story and dialogue, the full pipeline
13. **03** Concept art
14. **06** Environments: blockout of the Lantern Market, played before any art
15. **04** Characters, then **05** Rigging and animation in full
16. **06** Environments (art pass), then **07** Lighting and rendering
17. **11** (all four archetypes and Vesper) and **10** (snuffers and Vesper)
18. **12** Cutscenes, then **13** UI and HUD in full
19. **14** VFX, **15** Audio and voice, **16** Localization and subtitles
20. **17** Performance, then **18** playtests
21. Start reading **20** Release and marketing here, since devlogs and a Steam page come before you feel ready.

### Milestone 4: Playtest and scope decision
22. **18**, **19**, and **20** together: playtest data, hours data, and Steam page timing.

### Milestones 5 and 6: Production, polish, and launch
23. Repeat the per-district loop in the roadmap, going back to each area's walkthrough as needed.
24. For launch: **17**, **18**, **16**, **13**, **15**, and **20**.

---

## How to read a walkthrough

Every walkthrough uses the same template:

| Section | What it gives you |
|---|---|
| What this covers | One paragraph of scope |
| Why it matters for Wraith | How this area affects this particular game |
| Tools | Each tool's purpose, cost, whether its license allows commercial use, and AMD notes |
| Before you start | Installs, prerequisites, and which walkthroughs come first |
| Steps | Numbered steps, each with **Goal**, **Do this**, **Done when**, **Common mistakes**, **Claude can help**, and **Time** |
| Vertical slice checklist | Checkboxes that apply this area to the Lantern Market and Vesper |
| Going further | What to learn once the basics work |
| References | Official docs and recommended tutorial channels |

### Markers and conventions

- **`VERIFY:`** marks something that couldn't be confirmed against official documentation when the walkthrough was written, or something likely to change, such as a price, a menu path, or a plugin's compatibility. The marker says what to check. When you've checked one, fix the text and delete the marker, or ask Claude to.
- **Claude can help** says what Claude Code can do in that step, with the Blender MCP and Unreal MCP from walkthrough 01. "Manual" means you do it by hand, usually because it happens in a GUI that Claude can't see or click, or because it involves your accounts or money.
- **Time** is a rough estimate for a beginner, not a promise. Log your real hours; after a month, your own numbers beat these.
- **Costs** were checked on the date at the top of each walkthrough. Prices and license terms change, so check before you pay.
- **Paths:** `WraithGame/` is the Unreal project folder at the repo root. `/Game/Wraith/...` is a folder in Unreal's Content Browser; Unreal calls the project's `Content` folder `/Game`, so on disk it's `WraithGame/Content/Wraith/...`.
- **Menu paths** are written as **Edit > Project Settings > Engine > Input**. Unreal moves things between versions, so if a path doesn't match, search the settings panel for the setting name.
- **Naming** follows the README: `SM_`, `SK_`, `M_`, `MI_`, `T_`, `A_`, `ABP_`, `BP_`, `NS_`, `WBP_`, `LS_`, `DT_` for assets, and the `W` prefix after Unreal's class prefix for C++ classes (`AWCharacter`, `UWLanternComponent`). Walkthroughs 02–07 **suggest** a few prefixes the README doesn't have yet:
  - `L_` for levels;
  - `VO_` for voice Sound Waves;
  - `AM_` for montages;
  - `BS_` for blend spaces;
  - `IKR_` for IK Rigs and `RTG_` for IK Retargeters;
  - `MF_` for material functions and `MPC_` for material parameter collections.

  Add the ones you agree with to the README so they become official.

---

## Quick glossary

These are Unreal terms that show up in almost every walkthrough. Each walkthrough explains its own terms the first time they appear; this list is only for quick reference.

| Term | Meaning |
|---|---|
| Actor | Anything that can be placed in a level: a lantern, an enemy, a light, a camera |
| Component | A reusable piece attached to an actor, such as a mesh, a collision shape, or Wraith's own `UWLanternComponent` |
| Pawn / Character | A Pawn is an actor that can be controlled. A Character is a Pawn with a capsule, a skeletal mesh, and walking movement built in |
| Controller | The "brain" that possesses a Pawn: a PlayerController for the player, an AIController for enemies |
| GameMode | The rules object for a level. It decides, among other things, which Pawn and Controller classes to spawn |
| Level / Map | A playable space, saved as a `.umap` file |
| Blueprint | Unreal's visual scripting, and also a kind of asset that can subclass a C++ class. Wraith keeps systems in C++ and uses Blueprints for thin glue and tuning |
| Data Asset / Data Table | Assets that hold tunable data. A Data Table (`DT_`) is a table of rows that can be imported from CSV or JSON |
| `UCLASS` / `UPROPERTY` / `UFUNCTION` | C++ macros that register classes, variables, and functions with Unreal's reflection system, so the editor and Blueprints can see them |
| Module / Plugin | A unit of C++ code. The game itself is the `WraithGame` module. Plugins are optional modules you can switch on and off |
| Tick | The per-frame update function. Keep heavy work out of it |
| PIE | Play In Editor: running the game inside the editor window |
| Cooking / Packaging | Turning the project into a standalone game build. Cooking converts assets into their shipping format, and packaging bundles everything into a folder you can run or upload |
| Shaders / shader compilation | Small GPU programs that materials compile into. The first time you open a project or a new material, compiling them can take a long time |

---

## Batches and changelog

The walkthroughs are written in batches, and the developer reviews each batch before the next one starts:

1. Batch 1: `00-index.md`, `CLAUDE.md`, `docs/ROADMAP.md`, `01-project-setup.md`
2. Batch 2: 02–07 (content creation)
3. Batch 3: 08–11 (gameplay systems)
4. Batch 4: 12–16 (cutscenes, UI, VFX, audio, localization)
5. Batch 5: 17–20 (performance, testing, management, release)

| Date | Change |
|---|---|
| 2026-09-27 | Batch 1 written |
| 2026-09-27 | Batch 2 written (02–07), at the "deeper" level of detail. Added repo tools: `tools/dialogue/dialogue_tool.py`, `tools/unreal/import_dialogue.py`, `tools/art/palette_ratio.py`, `tools/art/lut_tool.py`, and `docs/art/wraith-palette.gpl` |
