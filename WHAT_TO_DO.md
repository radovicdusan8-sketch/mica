# WHAT TO DO

Instructions for Claude Code. Read `README.md` first for the full project context.

---

## Your Task

Build a complete, serious set of **step-by-step production walkthroughs** for *Wraith: The Black Hour*, one per production area, written specifically for this project, this developer, and this hardware.

These are not generic tutorials. They are the developer's personal manual for making this game well, from an empty folder to a shipped Steam release. The running example throughout is the **vertical slice: the Lantern Market district and the Sister Vesper boss fight.**

**This task produces documentation only.** Don't build game systems yet. Small test or verification scripts are fine when a walkthrough needs them.

---

## Ground Rules

1. **Accuracy over confidence.** Check current official documentation (Epic, Blender, AMD, and each tool's own docs) before writing instructions. State which version each walkthrough was written for. If you're unsure of a menu path, setting, or feature, say so and link the official page instead of guessing.
2. **Hardware-aware.** The developer has an AMD RX 9060 XT (16 GB) on Windows 11 with no CUDA. Flag anything NVIDIA-only and give the AMD alternative.
3. **Beginner to game dev, not to code.** Assume programming knowledge. Explain game-dev concepts the first time they appear, briefly, then move on.
4. **Solo and part-time.** Always prefer the simplest approach that gets a good result. Say when something is optional, when to buy an asset instead of making it, and when "good enough" is the right call.
5. **Costs.** For every tool, state whether it's free, paid (with approximate price or license type), and whether its license allows commercial use.
6. **Honest about Claude.** In every walkthrough, say exactly which steps Claude Code (with Blender MCP and Unreal MCP) can do or assist with, and which the developer must do by hand.
7. **No invented facts.** Don't invent tool features, plugin names, or numbers. If something needs checking, mark it `VERIFY:` with what to check.

---

## Required Structure for Every Walkthrough

Each walkthrough file follows this template:

```
# [Number]. [Area Name]

## What this covers
One short paragraph.

## Why it matters for Wraith
How this area affects this specific game.

## Tools
Table: tool, what it's for, cost, commercial license OK?, AMD notes.

## Before you start
Prerequisites, installs, and which earlier walkthroughs must be done first.

## Steps
Numbered steps. Each step has:
- Goal: what this step achieves
- Do this: exact actions (menus, settings, commands)
- Done when: how to check it worked
- Common mistakes: what usually goes wrong and how to fix it
- Claude can help: what Claude Code / MCP can do here, or "manual"
- Time: rough estimate for a beginner

## Vertical slice checklist
Concrete checkboxes for applying this area to the Lantern Market + Vesper slice.

## Going further
What to learn next once the basics work.

## References
Official docs and recommended tutorial channels, with links.
```

---

## The Walkthroughs to Write

Put them in `docs/walkthroughs/`, numbered in the order the developer should read them.

**00-index.md**
An index of all walkthroughs with one-line summaries and a recommended learning order.

**01-project-setup.md**
Installing Unreal Engine 5 and Visual Studio for C++, creating the C++ project, folder structure from the README, version control (compare Perforce and Git LFS and recommend one for a solo dev), connecting Claude Code, and setting up Blender MCP and an Unreal MCP. Include a test task to confirm each MCP works.

**02-story-and-dialogue-pipeline.md**
Organizing the story bible and scene scripts, a dialogue spreadsheet format (ID, speaker, Japanese line, English subtitle, audio file, scene), importing it into Unreal as a Data Table, and linking lines to audio and subtitles.

**03-concept-art.md**
Generating consistent concept art with AI tools, keeping characters consistent with reference images, paintovers in Krita, character turnaround sheets for modeling, and organizing a reference library.

**04-characters.md**
Modeling in Blender, starting from a base mesh vs. from scratch, Wraith's tattered cloak in Marvelous Designer, retopology for game use, UVs, texturing in Substance Painter or ArmorPaint, polygon and texture budgets for a game character, exporting to Unreal, and cloth physics in Unreal (Chaos Cloth) so cloaks move during combat.

**05-rigging-and-animation.md**
Rigging with AccuRig or Rigify, phone mocap with Rokoko Video or Move.ai (how to record good takes at home, including combat moves), cleanup in Blender, combat animation in Cascadeur, retargeting in Unreal with the IK Retargeter, Animation Blueprints, and root motion vs. in-place animation for melee combat.

**06-environments.md**
Blocking out a level with basic shapes first, building a modular gothic kit in Blender (walls, arches, stairs, lanterns) with consistent grid sizes, using Fab and Megascans, snow materials, frost and icicles, snowfall with Niagara, deformable snow only where it matters, building the distant city with PCG, and fog and atmosphere.

**07-lighting-and-rendering.md**
Lumen setup for night scenes, lantern lights, the violet accent lighting, volumetric fog, post-processing and color grading to match the art direction palette, TSR or FSR instead of DLSS, and scalability settings.

**08-core-combat.md**
Character movement, Enhanced Input, light and heavy attack chains, launchers and air combos, dodge, grab, hit detection, hit-stop, screen shake, hit reactions, Motion Warping for snapping to targets, combo meter and style rank, and how to tune "game feel." Reference Masahiro Sakurai's Creating Games videos where relevant.

**09-gameplay-ability-system-and-spirit-switching.md**
GAS explained for a beginner, setting up abilities, attributes, and effects in C++, then the spirit switching system: swapping character and moveset mid-combo, cooldowns, and carrying combo state across a switch.

**10-lantern-system.md**
The light/dark mechanic: lantern actors, lit and dark zones, enemies spawning and getting stronger in darkness, relighting, and how snuffer enemies and Sister Vesper interact with it.

**11-enemy-ai-and-bosses.md**
Behavior Trees vs. StateTree, crowd combat so enemies take turns attacking instead of swarming (in the style of Batman: Arkham), the four enemy archetypes (shielded cultist, Choir singer, snuffer, heavy), telegraphing attacks, and the Sister Vesper boss with phases.

**12-cutscenes.md**
Sequencer basics, camera work (long takes, holding shots, camera shake for a handheld feel), animating characters in sequences, facial animation for unmasked characters with MetaHuman tools, letterboxing, triggering cutscenes from gameplay and returning to gameplay with no loading, and building the cold open scene from `docs/story/`.

**13-ui-and-hud.md**
UMG basics, building the HUD from the existing mockup (health, shadow energy, lantern counter, boss bar, combo and rank, spirit switch slots, subtitles), menus, controller and keyboard support, and subtitle display for Japanese audio with English text.

**14-vfx.md**
Niagara basics, shadow energy, hit sparks, violet cracks, spirit release effects, snowfall, and performance budgets for effects.

**15-audio-and-voice.md**
Sound effect sourcing, recording and editing Japanese voice lines in Reaper, the processing chain for Wraith's voice, dialogue audio in Unreal, MetaSounds vs. FMOD for a solo dev, music implementation, and mixing.

**16-localization-and-subtitles.md**
Unreal's localization tools, string tables, supporting English subtitles now and more languages later, and Japanese font support.

**17-performance.md**
Profiling in Unreal, frame-rate targets, optimization for the RX 9060 XT and weaker PCs, scalability presets, and common performance traps in snowy, foggy night scenes.

**18-testing-and-playtesting.md**
Testing your own game without bias, running playtests with friends and on Steam Playtest, what to watch for, collecting feedback, and bug tracking.

**19-project-management.md**
Planning around part-time hours, milestone planning, a task board setup, estimating tasks, avoiding scope creep, and a weekly routine.

**20-release-and-marketing.md**
Steam page timing, capsule art, trailer editing in DaVinci Resolve, devlogs on YouTube and short clips, building wishlists, demo and Steam Next Fest, and release checklist.

---

## Also Create

**docs/ROADMAP.md**
Milestones from setup to release, each with a checklist and which walkthroughs it relies on:
1. Setup
2. Gray-box combat prototype (combat must be fun with cubes before any art)
3. Vertical slice (Lantern Market + Vesper + cold open)
4. Playtest and scope decision
5. Production, district by district
6. Polish and launch

**CLAUDE.md** (project root)
A short file of standing rules for future Claude Code sessions: summarize the README's hardware, stack, conventions, and working rules, and tell future sessions to read `README.md`, `docs/ROADMAP.md`, and the relevant walkthrough before starting any task.

---

## How to Work Through This

Work in batches and **stop after each batch** so the developer can review:

1. **Batch 1:** `00-index.md`, `CLAUDE.md`, `docs/ROADMAP.md`, `01-project-setup.md`
2. **Batch 2:** walkthroughs 02–07 (content creation)
3. **Batch 3:** walkthroughs 08–11 (gameplay systems)
4. **Batch 4:** walkthroughs 12–16 (cutscenes, UI, VFX, audio, localization)
5. **Batch 5:** walkthroughs 17–20 (performance, testing, management, release)

After each batch:
- Summarize what you wrote.
- List every `VERIFY:` item the developer should check.
- Ask whether to adjust the level of detail before continuing.

---

## Done When

- Every walkthrough file exists and follows the template.
- Every tool has cost, license, and AMD notes.
- Every walkthrough includes a vertical slice checklist.
- The roadmap links milestones to walkthroughs.
- `CLAUDE.md` exists with standing rules.
- The developer has approved every batch.
