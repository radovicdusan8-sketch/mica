# Wraith: The Black Hour

A dark gothic, story-driven 3D beat-em-up built by a solo developer in Unreal Engine 5, with help from Claude Code.

This README describes the project. `WHAT_TO_DO.md` tells Claude Code what to build first.

---

## 1. The Game in One Paragraph

Wraith, a dead Warden brought back with shadow powers, fights through Vesperhall, a vertical gothic city frozen in an endless winter night since its great cathedral clock stopped. Combat is a Spider-Man: Friend or Foe–style brawler with much deeper combos, spirit switching between fallen Wardens mid-fight, and a lantern light/dark mechanic. The story is told through AAA-style cinematic cutscenes with Japanese voice acting and English subtitles. Target length: at least 10 hours of main story.

---

## 2. Design Pillars

1. **Weighty, deep combat.** Never button mashing. Hit-stop, launchers, juggles, dodges, grabs, style ranks, and enemies that force decisions.
2. **Spirit switching.** Swap between Wraith and freed Warden spirits mid-combo. Each spirit has its own moveset.
3. **Light and dark.** Lanterns make areas safe. Where lanterns go out, the dead rise and enemies grow stronger.
4. **Cinematic storytelling.** Short, purposeful cutscenes built in Sequencer that flow straight into gameplay with no loading.
5. **Linear structure.** 8 districts, about 30 levels, one boss per district, a hub between missions.

---

## 3. Art Direction (summary)

- **Setting:** gothic city in eternal winter night. Heavy snow, frost, icicles, snow-covered rooftops and statues, fog between towers.
- **Palette:**

| Name | Hex | Use |
|---|---|---|
| Grave | #0B090C | Night sky, deep shadow |
| Wet slate | #22232C | Stone in shadow |
| Fog | #554A53 | Mist, distance |
| Lantern gold | #E0A24A | Light, runes, anything living |
| Spirit violet | #9B6BFF | The dead, Wraith's powers |
| Porcelain | #D8CCB8 | Masks, bone, the Choir |

- **Ratio:** about 70% darkness and stone, 20% warm lantern light, 10% violet.
- **Rules:** warm light means the living, violet means the dead, darkness means danger. Never put violet on anything living or warm light on anything dead. Characters must read by silhouette.

---

## 4. Story Reference

The full story lives in `docs/story/wraith-story-bible-v2.md`. Scene scripts live in `docs/story/scenes/`.

Key characters: Wraith (Elias), Maren, Oren, Kestrel, Tovan, the Cantor (Ansel), Master Aurel (also appears as the Pilgrim), Sister Vesper.

**First milestone:** the vertical slice. District 1, the Lantern Market: the cold open, the level, the lantern mechanic, 3–4 enemy types, and the Sister Vesper boss fight.

---

## 5. Developer and Hardware

- **Developer:** one person, working part-time. Has a coding background but is new to game development. Explanations should assume programming knowledge but not game-dev knowledge.
- **OS:** Windows 11.
- **GPU:** AMD Radeon RX 9060 XT, 16 GB VRAM. **No NVIDIA GPU and no CUDA.** Any tool or feature that requires NVIDIA (DLSS, CUDA-only AI tools) must be flagged, with an AMD-compatible alternative (for example TSR or FSR instead of DLSS).

---

## 6. Tech Stack

| Area | Tool |
|---|---|
| Engine | Unreal Engine 5 (latest stable version) |
| Gameplay code | C++ for core systems, Blueprints only for thin glue and tuning |
| Abilities / switching | Gameplay Ability System (GAS) |
| Input | Enhanced Input |
| Enemy AI | Behavior Trees or StateTree |
| Cutscenes | Sequencer |
| VFX | Niagara |
| UI | UMG |
| Audio | MetaSounds, or FMOD |
| 3D modeling | Blender |
| Cloth | Marvelous Designer |
| Texturing | Substance Painter or ArmorPaint |
| Rigging | AccuRig or Rigify |
| Animation | Phone mocap (Rokoko Video or Move.ai), Cascadeur, Blender cleanup |
| Asset library | Fab (including Megascans) |
| Concept art | AI image generation plus Krita paintovers |
| Voice editing | Reaper |
| Trailer editing | DaVinci Resolve |
| Version control | Perforce or Git LFS |
| AI assistance | Claude Code with Blender MCP and an Unreal MCP |
| Voice language | Japanese audio, English subtitles |

---

## 7. Pipeline Rule

**Blender makes the pieces. Unreal puts them together.**

Models, cloth, textures, and rigs are made outside Unreal. Levels, lighting, animation setup, cutscenes, VFX, UI, and all gameplay are assembled in Unreal. Cutscenes are never rendered in Blender.

---

## 8. Folder Structure

```
/docs
  /story            story bible, scene scripts
  /art              art direction, palette, reference boards
  /design           system design docs (combat, switching, lanterns, enemies)
  /walkthroughs     step-by-step guides for every production area
  ROADMAP.md        milestones and checklists
/source-art
  /blender          .blend files
  /marvelous        cloth projects
  /substance        texture projects
  /mocap            raw and cleaned motion data
  /concept          concept art
/audio
  /voice/ja         Japanese voice recordings
  /sfx
  /music
/WraithGame         the Unreal project
/tools              scripts (dialogue import, batch tools, automation)
README.md
WHAT_TO_DO.md
CLAUDE.md
```

---

## 9. Conventions

- **Unreal asset prefixes:** `SM_` static mesh, `SK_` skeletal mesh, `M_` material, `MI_` material instance, `T_` texture, `A_` animation, `ABP_` animation blueprint, `BP_` blueprint, `NS_` Niagara system, `WBP_` widget, `LS_` level sequence, `DT_` data table.
- **C++ classes:** prefix with `W` (for example `AWCharacter`, `UWLanternComponent`).
- **Branches or changelists:** one system or one feature at a time.
- **Every system gets a short design doc** in `/docs/design` before it's built.

---

## 10. Working With Claude Code

- Work on one system or one step at a time.
- Explain what you're about to do before doing it, and stop at checkpoints so the developer can test in the editor.
- Verify instructions against current official documentation. Don't guess menu paths, settings names, or version numbers; say when you're unsure.
- Never download or install anything large without stating its size first.
- Never delete or overwrite art, audio, or `.uasset` files without asking.
