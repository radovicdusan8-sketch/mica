# Roadmap: Wraith: The Black Hour

This file takes the project from an empty folder to a Steam release in six milestones. Each milestone has a goal, a checklist, a "done when" test, and the walkthroughs it depends on. Work on one milestone at a time. Tick boxes as you go and commit this file along with the work.

The walkthroughs live in [`walkthroughs/`](walkthroughs/00-index.md). Links to walkthroughs that haven't been written yet will stay broken until their batch is done.

---

## How to use this roadmap

- **Milestones are sequential.** Two walkthroughs are the exception and run the whole time: project management ([19](walkthroughs/19-project-management.md)) from day one, and marketing ([20](walkthroughs/20-release-and-marketing.md)) from the vertical slice onward.
- **Close every milestone with a checkpoint.** Tag the repo (for example `git tag m2-graybox`, or a label in Perforce). Write a five-line retrospective in `docs/retros/` covering what worked, what didn't, and what to change. Then update your hours log.
- **Log your hours from day one.** A spreadsheet with date, task, milestone, area, and hours is enough. Milestone 4's scope decision is only as good as this data.
- **Pin the engine version.** Stay on the Unreal version you install in Milestone 1 through the whole vertical slice, and only upgrade between milestones, after a backup. Engine upgrades in the middle of a milestone are a common way to lose weeks. Walkthrough 01 installs Unreal Engine 5.8. Epic has said 5.8 is the last planned major UE5 release and has targeted Unreal Engine 6 Early Access for the end of 2027 (`VERIFY:` in Epic's announcements). Treat any move to UE6 as a Milestone 4 or later decision, never a mid-milestone one.
- **Time ranges are rough guesses, not facts.** They assume about 10–15 hours a week from someone who is new to Unreal but not to programming. Replace them with your own numbers once Milestone 2 has given you real data.

### Planning inputs (fill these in)

| Input | Your value |
|---|---|
| Hours per week you can reliably give | ___ |
| Engine version pinned in Milestone 1 | UE 5.8.__ |
| Budget for assets, tools, and plugins | ___ |
| Budget for voice actors and music (if any) | ___ |
| Target release window | ___ |

---

## Overview

| # | Milestone | What you have at the end | Main walkthroughs | Rough guess at part-time pace |
|---|---|---|---|---|
| 1 | Setup | A working toolchain: C++ project, version control with an off-site copy, Claude Code, Blender MCP, Unreal MCP | 01, 19 | 2–4 weekends |
| 2 | Gray-box combat prototype | A 5–10 minute fight with mannequins and cubes that other people enjoy | 08, 09, 10, 11, 13, 18, plus parts of 05 and 06 | 3–6 months |
| 3 | Vertical slice | Cold open → Lantern Market level → Sister Vesper, at final quality, in a packaged build | 02–07, 10–17 | 6–12 months |
| 4 | Playtest and scope decision | A written, dated scope for the full game that fits your measured pace | 18, 19, 20 | 2–6 weeks |
| 5 | Production | Every district built, district by district, to alpha and then beta | All, per district | Depends on Milestone 4 |
| 6 | Polish and launch | The game released on Steam | 16, 17, 18, 20 | 3–6 months |

### Which walkthroughs each milestone uses

● = main use, ○ = partial use or a reference.

| Walkthrough | M1 | M2 | M3 | M4 | M5 | M6 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| [01 Project setup](walkthroughs/01-project-setup.md) | ● | | | | | |
| [02 Story and dialogue pipeline](walkthroughs/02-story-and-dialogue-pipeline.md) | ○ | | ● | | ● | |
| [03 Concept art](walkthroughs/03-concept-art.md) | | | ● | | ● | |
| [04 Characters](walkthroughs/04-characters.md) | | | ● | | ● | |
| [05 Rigging and animation](walkthroughs/05-rigging-and-animation.md) | | ○ | ● | | ● | |
| [06 Environments](walkthroughs/06-environments.md) | | ○ | ● | | ● | |
| [07 Lighting and rendering](walkthroughs/07-lighting-and-rendering.md) | | | ● | | ● | ○ |
| [08 Core combat](walkthroughs/08-core-combat.md) | | ● | ○ | | ○ | ○ |
| [09 GAS and spirit switching](walkthroughs/09-gameplay-ability-system-and-spirit-switching.md) | | ● | ○ | | ○ | |
| [10 Lantern system](walkthroughs/10-lantern-system.md) | | ● | ● | | ○ | |
| [11 Enemy AI and bosses](walkthroughs/11-enemy-ai-and-bosses.md) | | ● | ● | | ● | |
| [12 Cutscenes](walkthroughs/12-cutscenes.md) | | | ● | | ● | |
| [13 UI and HUD](walkthroughs/13-ui-and-hud.md) | | ○ | ● | | ○ | ● |
| [14 VFX](walkthroughs/14-vfx.md) | | | ● | | ● | ○ |
| [15 Audio and voice](walkthroughs/15-audio-and-voice.md) | | | ● | | ● | ● |
| [16 Localization and subtitles](walkthroughs/16-localization-and-subtitles.md) | | | ● | | ○ | ● |
| [17 Performance](walkthroughs/17-performance.md) | | | ● | | ○ | ● |
| [18 Testing and playtesting](walkthroughs/18-testing-and-playtesting.md) | | ● | ● | ● | ● | ● |
| [19 Project management](walkthroughs/19-project-management.md) | ● | ● | ● | ● | ● | ● |
| [20 Release and marketing](walkthroughs/20-release-and-marketing.md) | | | ○ | ● | ● | ● |

---

## Milestone 1: Setup

**Goal:** every tool is installed and connected, and a clean clone of the repo can be built and played.

**Relies on:** [01 Project setup](walkthroughs/01-project-setup.md), [19 Project management](walkthroughs/19-project-management.md) (board and weekly routine only).

### Checklist

- [ ] AMD graphics driver updated; enough free SSD space for the engine, Visual Studio, and the project (01 lists the sizes)
- [ ] Unreal Engine installed, and the exact version written into the table above and into `CLAUDE.md`
- [ ] Visual Studio installed with the components Epic lists for your engine version
- [ ] `WraithGame` C++ project created, compiled from Visual Studio, opened in the editor, and played (Play In Editor)
- [ ] Live Coding tested: a one-line C++ change shows up in the editor without restarting
- [ ] README folder structure created (`docs/`, `source-art/`, `audio/`, `WraithGame/`, `tools/`)
- [ ] Version control chosen and set up, first commit pushed to an off-site host
- [ ] Restore test: clone into a new folder, build, open, and press Play
- [ ] Claude Code installed, running in the repo root, and reading `CLAUDE.md`
- [ ] Blender MCP test task passed
- [ ] Unreal MCP test task passed
- [ ] Story bible and scene scripts copied into `docs/story/` (02 covers how to organize them)
- [ ] Task board and hours log created; weekly routine written down (19)
- [ ] Tag `m1-setup`

### Done when

You can delete your working folder, clone the repo, build it, and press Play in under an hour, and both MCP test tasks pass.

---

## Milestone 2: Gray-box combat prototype

**Goal:** prove that combat is fun **before any art exists**. Use Unreal's default mannequin, placeholder animations, and cubes or capsules as enemies. If it isn't fun with cubes, no amount of art will fix it.

**Relies on:** [08 Core combat](walkthroughs/08-core-combat.md), [09 GAS and spirit switching](walkthroughs/09-gameplay-ability-system-and-spirit-switching.md), [11 Enemy AI and bosses](walkthroughs/11-enemy-ai-and-bosses.md), [10 Lantern system](walkthroughs/10-lantern-system.md), [05 Rigging and animation](walkthroughs/05-rigging-and-animation.md) (Animation Blueprint, root motion, and retargeting sections only), [06 Environments](walkthroughs/06-environments.md) (blockout section only), [13 UI and HUD](walkthroughs/13-ui-and-hud.md) (debug HUD only), [18 Testing and playtesting](walkthroughs/18-testing-and-playtesting.md).

Write a short design doc in `docs/design/` before building each system, as the README requires.

### Checklist

**2A. Feel (one player, one training dummy)**
- [ ] Gray-box arena built from simple shapes
- [ ] Third-person movement and camera with Enhanced Input, working on controller and keyboard
- [ ] Light attack chain (3–4 hits) and a heavy attack or finisher
- [ ] Hit detection, hit-stop, camera shake, and a hit reaction on the dummy
- [ ] Dodge with invulnerability frames
- [ ] Input buffering, so attacks pressed slightly early still come out
- [ ] Soft targeting with Motion Warping, so attacks snap to the nearest sensible enemy
- [ ] All tuning numbers (damage, timings, hit-stop length) live in data assets or data tables, not hard-coded

**2B. Depth**
- [ ] Launcher, a short air combo, and a slam
- [ ] Grab and throw
- [ ] Combo counter and a placeholder style rank on a debug HUD

**2C. Enemies**
- [ ] Two enemy archetypes as cubes or capsules (start with a basic cultist and the heavy)
- [ ] Attack tokens, so only a few enemies attack at once and the rest circle (Arkham-style)
- [ ] Readable telegraphs before every enemy attack
- [ ] Decision made: Behavior Trees or StateTree (11)

**2D. Wraith's identity**
- [ ] Gameplay Ability System set up in C++ (09)
- [ ] One extra Warden spirit with its own moveset; switching mid-combo carries the combo over
- [ ] One lantern and one dark zone: enemies are stronger in the dark, and relighting works (10)

**2E. Proof**
- [ ] A 5–10 minute sequence of fights in the gray box
- [ ] At least 3 people who didn't build it play it while you watch silently (18)
- [ ] Retrospective and tag `m2-graybox`

### Done when

- Testers keep playing without being asked to, and they use dodge, launchers, and switching instead of mashing one button.
- You can say in one sentence what decision each enemy forces on the player.
- If this isn't true yet, stay in Milestone 2. Cut or simplify a mechanic before adding a new one. A smaller combat system that feels great beats a larger one that feels mushy.

---

## Milestone 3: Vertical slice

**Goal:** a short, complete piece of the game at final quality: the cold open, the Lantern Market level, the lantern mechanic, the four enemy types, and the Sister Vesper boss fight, running in a **packaged build**. The slice answers two questions: "what does the finished game look and feel like?" and "how long does it take me to make it?" It is also the likely basis for a Steam demo later (20).

**Relies on:** walkthroughs 02–07 and 10–17, with 18 and 19 throughout.

### Checklist

**3A. Plan the slice**
- [ ] `docs/design/vertical-slice.md`: what's in, what's out, target play length, asset list
- [ ] Buy-vs-make list: what comes from Fab, what you make, what you commission (04, 06)
- [ ] Hours log split by area, so Milestone 4 can use it

**3B. Story, dialogue, and concept**
- [ ] Cold open and District 1 scenes broken down into a dialogue spreadsheet, imported as a Data Table (02)
- [ ] Concept art for Wraith, Sister Vesper, the four enemies, and Lantern Market mood boards (03)
- [ ] Turnaround sheets for Wraith and Vesper (03)

**3C. Level first, art second**
- [ ] Lantern Market blockout, played end to end with the gray-box combat and gray-box enemies (06, 10, 11)
- [ ] Encounter layout and lantern placement tested in blockout before any art (10)

**3D. Characters and animation**
- [ ] Wraith, including the tattered cloak with Chaos Cloth (04)
- [ ] Sister Vesper (04)
- [ ] Four enemy types: shielded cultist, Choir singer, snuffer, heavy (04; buy or adapt base meshes where you can)
- [ ] Rigs, mocap or keyframed combat animation, retargeting, Animation Blueprints (05)

**3E. World**
- [ ] Modular gothic kit on a consistent grid, snow and frost materials, snowfall, distant city, fog (06)
- [ ] Night lighting with Lumen, lantern gold and spirit violet accents, grading to the palette (07)

**3F. Gameplay content**
- [ ] All four archetypes with final behaviors and telegraphs (11)
- [ ] Snuffers and Sister Vesper interacting with the lantern system (10, 11)
- [ ] Sister Vesper boss with phases (11)

**3G. Presentation**
- [ ] Cold open cutscene flowing into gameplay with no loading screen (12)
- [ ] HUD built from the mockup: health, shadow energy, lantern counter, boss bar, combo and rank, spirit slots, subtitles (13)
- [ ] Menus: main, pause, settings (13)
- [ ] VFX: hit sparks, shadow energy, violet cracks, spirit release, snowfall (14)
- [ ] SFX, Japanese voice lines for the slice, music, first mix (15)
- [ ] English subtitles through Unreal's localization system and a Japanese-capable font (16)

**3H. Ship-quality checks**
- [ ] Packaged build (not just the editor) runs start to finish
- [ ] Frame-rate target met on the RX 9060 XT at the chosen resolution and scalability preset (17)
- [ ] Two playtest rounds with people outside the project (18)
- [ ] Retrospective and tag `m3-slice`

### Done when

The packaged slice runs from the cold open to the end of the Vesper fight on your PC at your frame-rate target, at least five outside players finish it, and you'd be comfortable showing it publicly.

---

## Milestone 4: Playtest and scope decision

**Goal:** decide what the full game is, based on playtest results and your measured hours rather than hope.

**Relies on:** [18 Testing and playtesting](walkthroughs/18-testing-and-playtesting.md), [19 Project management](walkthroughs/19-project-management.md), [20 Release and marketing](walkthroughs/20-release-and-marketing.md).

### Checklist

- [ ] Final slice playtests done and summarized: top five problems, top five things players loved (18)
- [ ] Hours audit for Milestone 3, split by area: level, characters, enemies, boss, cutscene minutes, voice lines, UI, VFX, audio
- [ ] Full-game cost extrapolated (method below)
- [ ] Scope chosen using the levers below, and written up in `docs/design/scope-decision.md` with the date
- [ ] `README.md` updated if the headline numbers change (8 districts, about 30 levels, 10+ hours)
- [ ] Milestone 5 section below rewritten with the real district list and target dates
- [ ] Decision on outside help and budget: voice actors, music, character art
- [ ] Steam page timing decided (20)
- [ ] Tag `m4-scope`

### How to extrapolate

Example with made-up numbers, only to show the arithmetic: the slice took 700 hours. Later districts reuse the systems, the pipeline, and part of the kit, so suppose each one costs about 60% of the slice's hours. Seven more districts then cost about 7 × 0.6 × 700 ≈ 2,940 hours. At 12 hours a week that is about 245 weeks, or roughly 4.7 years, before polish and launch.

Put in your own numbers. If the result is longer than you're willing to work on this game, pull levers until it fits.

### Scope levers, least damaging first

1. **Reuse the kit.** Redress one modular gothic kit per district with different snow, lighting, and props instead of building a new kit each time.
2. **Fewer, denser levels.** Three strong levels per district beat four padded ones.
3. **Merge districts.** Keep the story beats and cut the number of distinct places.
4. **Cheaper cutscenes.** Keep full cinematics for the key scenes. Do the rest as simple in-engine dialogue shots with few cameras.
5. **Voice budget.** Fully voice the cutscenes, and use text only for barks and side lines.
6. **Shorter game.** The README targets 10+ hours. That target is your call; a tighter game that ships is worth considering.

### Done when

There is a dated scope decision with a district-by-district schedule you believe at your measured pace.

---

## Milestone 5: Production, district by district

**Goal:** build the rest of the game one district at a time, reusing the slice pipeline.

**Relies on:** everything, per district. Use the vertical slice checklists at the end of each walkthrough as the template.

### Before the first new district

- [ ] Hub between missions (the README's structure pillar), built right after the slice because every mission passes through it
- [ ] Save/load, checkpoints, and mission select. **No walkthrough covers these yet.** Write a design doc in `docs/design/` first and ask Claude to help research current Unreal practice.
- [ ] Settings that persist: graphics, audio, controls, subtitles (13, 16, 17)

### Per-district loop (copy this block for each district)

- [ ] District brief: story beats, new enemy or mechanic, boss concept (`docs/design/district-N.md`)
- [ ] Dialogue spreadsheet updated and imported (02)
- [ ] Concept pass (03)
- [ ] Blockout of every level, played with current combat (06)
- [ ] Encounter and lantern pass (10, 11)
- [ ] New characters and enemies, rigged and animated (04, 05)
- [ ] Art pass: kit variants, set dressing, lighting (06, 07)
- [ ] Boss (11)
- [ ] Cutscenes (12)
- [ ] Voice recorded and implemented, subtitles (15, 16)
- [ ] VFX and audio pass (14, 15)
- [ ] Performance check (17)
- [ ] Playtest and fix pass (18)
- [ ] Tag `district-N`

### Alpha and beta

- [ ] **Alpha:** every district is playable start to finish. Rough art is fine.
- [ ] **Beta:** content complete, final assets in, only bugs and polish left.

### Keep marketing running

- [ ] Devlogs and short clips on a regular schedule (20)
- [ ] Wishlist count tracked monthly (20)
- [ ] Steam demo and Steam Next Fest planned (20)

### Done when

Beta is reached: the whole game can be played start to finish with final content.

---

## Milestone 6: Polish and launch

**Goal:** turn the beta into a release on Steam.

**Relies on:** [16](walkthroughs/16-localization-and-subtitles.md), [17](walkthroughs/17-performance.md), [18](walkthroughs/18-testing-and-playtesting.md), [20](walkthroughs/20-release-and-marketing.md), plus [13](walkthroughs/13-ui-and-hud.md) and [15](walkthroughs/15-audio-and-voice.md) for final polish.

### Checklist

- [ ] Full playthroughs by you and by testers; bugs triaged into must-fix, should-fix, won't-fix (18)
- [ ] Performance on lower-end PCs, scalability presets, shader-compilation hitches checked (17)
- [ ] Controller and keyboard polish, input remapping, accessibility options such as subtitle size and background, and a camera-shake toggle (13)
- [ ] Subtitles proofread; fonts checked on every screen (16)
- [ ] Final audio mix (15)
- [ ] Steam store page complete, trailer done, build uploaded, release date set (20)
- [ ] Steam content survey filled in, including the AI-content disclosure. VERIFY: Steam's current rules on disclosing AI-generated content, since concept art uses AI tools (03, 20).
- [ ] Release checklist in 20 completed
- [ ] Post-launch plan: first patch window, how you'll collect crash reports and feedback
- [ ] Tag `v1.0`

### Done when

The game is live on Steam and you have a plan for the first patch.

---

## Risks to watch the whole time

| Risk | Early warning sign | What to do |
|---|---|---|
| Scope too big for part-time solo work | Milestone 2 or 3 takes more than twice the guess | Use the Milestone 4 levers early, not late |
| Burnout | Skipped weeks, dreading sessions | Smaller weekly goals, one visible win per week (19) |
| Lost work | "I'll push later" | Push at the end of every session; test a restore each milestone (01) |
| Engine or tool churn | Wanting to upgrade mid-milestone | Upgrade only between milestones, after a tagged backup |
| Art before fun | Modeling characters during Milestone 2 | Stop. Finish the gray-box proof first |
| AI tool and licensing surprises | A tool changes its terms, or a store asks about AI use | Keep the source and license of every asset in a list (03, 06, 20) |
