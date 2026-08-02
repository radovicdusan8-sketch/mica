# MASTER ROADMAP — From Zero to an Animated Ryuma in UE5

**Who this is for:** a beginner starting fresh, who wants the **entire ordered path** — katana → character → textures → rig → Unreal → moving in-game — with enough interface detail (menus, shortcuts, folders) to *learn the basics*, not just follow blindly.

**How to read this:** do it **top to bottom.** Each Phase is a self-contained skill with a clear "done when." Don't skip ahead — the whole point is no more jumping steps. Where a topic already has its own deep doc, this links to it *at the moment you need it.*

**Honest expectation:** this is a **months-long learning journey**, not a weekend. That's normal. The katana (Phase 2) is your first real win; the moving character (Phase 8) is the big one. Celebrate each phase.

**Tools & versions:** Blender (latest stable, 4.x), Unreal Engine **5.8**, Epic Games Launcher. All free.

---

## PHASE 0 — Folders & Mental Model *(do this once)*

### 0.1 Disk layout (decide now, never reorganize later)
```
C:\Claude\severed-blade\
├─ SeveredBlade\            ← the Unreal project (from Milestone 0)
│   └─ SeveredBlade.uproject
├─ art\
│   └─ blender\             ← your .blend working files (matches the repo)
│       ├─ katana.blend
│       └─ ryuma.blend
├─ exports\                 ← FBX/GLB you send to Unreal
└─ textures\                ← PNG texture maps
```
*(Your git repo already tracks `art/blender/`. UE's `Content/` is auto-generated and stays out of git — see `.gitignore`.)*

### 0.2 In-Unreal content layout (make these folders in the Content Browser)
```
Content/SeveredBlade/
├─ Characters/Ryuma/        (mesh, skeleton, materials, textures)
├─ Weapons/Katana/
├─ Animations/Ryuma/
└─ Materials/
```
Keeping everything under one `SeveredBlade/` folder means nothing collides with template content.

### 0.3 The mental model (the whole pipeline in one breath)
> **Model** the shape → **UV unwrap** it (flatten for texturing) → **texture** it (color/material) → **rig** it (skeleton + weights) → **export FBX** → **import to UE** → **retarget animations** → **play.**
Weapons skip rigging (they're static meshes attached to a hand bone). Characters do all of it.

---

## PHASE 1 — Learn the Blender Interface *(don't model yet — get fluent first)*

Spend a session *just* navigating. This removes 90% of the "where is that?" pain.

### 1.1 The screen (default Layout workspace)
- **3D Viewport** (center) — where you build.
- **Outliner** (top-right) — the list of everything in the scene.
- **Properties editor** (bottom-right) — tabs down its left edge: **Render, Output, View Layer, Scene, World, Object (orange square), Modifiers (wrench), Particles, Physics, Constraints, Object Data (green triangle), Material (checkered sphere)**. You'll live in **Modifiers (wrench)** and **Material**.
- **Timeline** (bottom) — for animation later.
- **Workspace tabs** (very top): **Layout · Modeling · Sculpting · UV Editing · Texture Paint · Shading · Animation · Rendering** — each rearranges the screen for that job. You switch tabs as you move through the pipeline.

### 1.2 Navigation (memorize these five)
- **Orbit:** Middle-Mouse-Button drag.
- **Pan:** Shift + MMB drag.
- **Zoom:** scroll wheel.
- **Focus on selected:** Numpad `.` (period). Frame everything: `Home`.
- **Views:** Numpad `1` front, `3` right, `7` top, `Ctrl+`those for back/left/bottom, `5` toggles ortho/perspective.
- **No numpad?** Edit → Preferences → Input → **Emulate Numpad** (uses the top-row number keys), or use the little axis-gizmo top-right of the viewport.

### 1.3 The ten operations you'll use constantly
| Action | Key | Notes |
|---|---|---|
| Select | LMB | `A` = select all, `Alt+A` = none, `B` = box select |
| Move / Rotate / Scale | `G` / `R` / `S` | then type an axis `X`/`Y`/`Z`, then a number, then Enter |
| Enter/exit **Edit Mode** | `Tab` | edit the mesh's verts/edges/faces |
| Vertex / Edge / Face mode | `1` / `2` / `3` | (while in Edit Mode) |
| Extrude | `E` | pull new geometry out |
| Inset face | `I` | shrink a face inward |
| Loop cut | `Ctrl+R` | add edge loops (scroll to add more) |
| Bevel | `Ctrl+B` | round/chamfer an edge (scroll for segments) |
| Add object | `Shift+A` | cube, cylinder, etc. |
| **Apply transforms** | `Ctrl+A` | **critical before export** — bakes scale/rotation |
| Save | `Ctrl+S` | do it constantly; `Ctrl+Shift+S` = save as (increment: ryuma_01, _02…) |

### 1.4 Set units (once per file)
Properties → **Scene** tab → Units → Metric, Unit Scale 1.0. Model at **real-world size** (katana ≈ 1 m, Ryuma ≈ 1.8 m). Unreal uses cm; the FBX exporter converts for you.

> **Done when:** you can orbit/pan/zoom without thinking, add a cube, move/scale it on one axis, enter Edit Mode, and save. That's the foundation everything else stands on.

---

## PHASE 2 — Model the Katana *(your first real model — hard-surface basics)*

The katana is the **perfect first project**: mostly straight, teaches box-modeling, bevels, and materials without organic sculpting. Deep step-by-step lives in [`CHARACTER_ART_PATH.md`](CHARACTER_ART_PATH.md) ("katana first"); the ordered summary:

1. **Blade:** `Shift+A → Mesh → Cube`. Scale it thin and long (`S`, `Z`/`X`). Tab into Edit Mode; use **loop cuts** (`Ctrl+R`) and move verts to shape the curve and the tapered tip. Add a subtle edge with a **bevel** (`Ctrl+B`).
2. **Tsuba (guard):** `Shift+A → Cylinder`, flatten it (`S`, `Z`, small), position at the blade's base.
3. **Tsuka (handle):** a stretched cube or cylinder below the guard; bevel the edges.
4. **Kashira (pommel cap):** small shape at the handle's end.
5. **Join or keep separate:** select all → `Ctrl+J` to join into one object (fine for a prop).
6. **UV unwrap:** switch to the **UV Editing** workspace, select all faces (`A`), `U → Smart UV Project` (good enough for a hard-surface prop).
7. **Material & color:** **Material** properties tab → **New** → set **Base Color** (blade = steel grey, high metallic; cord = your crimson `#8A1F1F`-ish; iron parts = near-black, per `../design/CHARACTER_DESIGN.md` §0). Switch the viewport to **Material Preview** (top-right spheres, 3rd) to see it.
8. **Apply transforms** (`Ctrl+A → All Transforms`) and **save** as `art/blender/katana.blend`.

> **Done when:** a katana that looks right in Material Preview, correctly scaled (~1 m), transforms applied. You've now learned modeling, UVs, and materials on something simple. **This is a big milestone — everything else is the same skills scaled up.**

---

## PHASE 3 — Get Ryuma's Base Body *(the honest fork)*

Full character modeling from scratch (blockout → sculpt → retopo → bake) is **advanced** — weeks of skill on its own. Pick the path that matches your goal:

- **Path A — Hybrid (recommended for now):** use your **Meshy Ryuma prototype** (or a free base mesh: MakeHuman, or a Blender base-mesh add-on) as the body, and *learn the rest of the pipeline* (clean-up, UVs, texturing, rig, UE) on it. You get a moving character in weeks, not months, and you learn every downstream skill. Import his GLB per [`MESHY_TO_UNREAL.md`](MESHY_TO_UNREAL.md) Part A.
- **Path B — From scratch (the long learning road):** block out the body from primitives → **Sculpt** workspace to shape it → **retopologize** (build clean low-poly over the sculpt) → UV → bake detail. Do this *after* you've shipped a character via Path A, so you're not learning everything at once.

**Recommendation:** **Path A now.** Ship a moving Ryuma with the Meshy base; come back to Path B when you want a bespoke model and have the fundamentals. (Modeling the katana from scratch in Phase 2 already gives you real modeling reps.)

### 3.1 Clean-up (Path A, in Blender)
- Import the GLB (`File → Import → glTF 2.0`).
- Switch to **Material Preview** to confirm colors (the #1 "lost colors" fix — see [`MESHY_TO_UNREAL.md`](MESHY_TO_UNREAL.md) Part A).
- Optional but recommended: **Decimate** modifier (Modifiers/wrench tab) or manual **retopo** to lighten a dense Meshy mesh.
- Stand him in **T-pose or A-pose** (arms out) — required for rigging.
- Scale to **~1.8 m**, `Ctrl+A → All Transforms`.

> **Done when:** a clean-ish Ryuma body, colors visible, T/A-pose, ~1.8 m, transforms applied.

---

## PHASE 4 — Texture Ryuma *(give him his canon colors)*

His look is locked in [`../design/CHARACTER_DESIGN.md`](../design/CHARACTER_DESIGN.md) §1: **dark indigo kimono, tattered charcoal haori, forearm wraps, single crimson accent cord, Kurogane charcoal/steel-blue.**

- **If the Meshy albedo is close:** keep it; just tweak colors in an image editor or Blender's **Texture Paint** workspace.
- **To assign flat colors by part:** in Edit Mode select the faces of a part → in **Material** properties make a new material slot → **Assign** → set its Base Color. Repeat per part (kimono, haori, cord, skin, metal).
- **Save his textures** to `textures/` and keep the .blend linked to them.

> **Done when:** Ryuma reads as *Ryuma* — indigo/charcoal with the crimson cord — in Material Preview.

---

## PHASE 5 — Rig Ryuma *(make him deformable)*

Full detail in [`RIGGING_AND_RETARGETING.md`](RIGGING_AND_RETARGETING.md) Step 1. In order:
1. Confirm T/A-pose + applied transforms (Phase 3).
2. Rig via **Mixamo** (easiest), **Meshy auto-rig**, or **AutoRig Pro** in Blender.
3. You now have a **skeleton + skin weights** — he can be posed by bones.

> **Done when:** you can select a bone, rotate it, and the mesh deforms with it.

---

## PHASE 6 — Attach the Katana to His Hand

- The katana stays a **static mesh**; it rides a hand bone.
- **Simplest (do it in UE):** import both separately; in Unreal add a **Socket** on the right-hand bone of Ryuma's skeleton and attach the katana to it. (Covered as a follow-up; ask when you reach it.)
- *(You can also parent it to the hand bone in Blender, but the UE socket way is more flexible for combat later.)*

---

## PHASE 7 — Export to UE5 *(FBX, the right settings)*

Full detail in [`MESHY_TO_UNREAL.md`](MESHY_TO_UNREAL.md) Parts B–C. In order:
1. **Apply All Transforms** (`Ctrl+A`) — again, always.
2. `File → Export → FBX` → **Selected Objects**, **Path Mode: Copy** + **Embed Textures** (the image icon). Save to `exports/`.
3. Katana: export as its own FBX (static mesh). Ryuma: export the **rigged** FBX (with the armature).

---

## PHASE 8 — Import, Materials, Animate, Play

This is the payoff. Order:
1. **Import katana** → Static Mesh (into `Content/SeveredBlade/Weapons/Katana/`).
2. **Import Ryuma** → **Skeletal Mesh** (creates his Skeleton) into `Characters/Ryuma/`. Tick Import Textures/Materials. Fix materials if grey ([`MESHY_TO_UNREAL.md`](MESHY_TO_UNREAL.md) Part C).
3. **Retarget** Manny's animations onto Ryuma via the **IK Retargeter** — the full flow (IK Rigs, retarget chains, the critical **retarget-pose match**, bake/live) is in [`RIGGING_AND_RETARGETING.md`](RIGGING_AND_RETARGETING.md) Steps 3–4.
4. **Swap into the game:** open `BP_ThirdPersonCharacter` → set **Skeletal Mesh = Ryuma**, **Anim Class = retargeted Anim Blueprint**; attach the katana to the hand socket (Phase 6).
5. **Press Play.** You run, sprint, and jump as **Ryuma, holding his katana.** 🎉

> **Done when:** the Manny stand-in is gone and Ryuma moves through the Milestone-0 test level — his zero-magic Prologue state.

---

## PHASE 9 — Keep Getting Better *(the learning plan)*

You don't need to master everything at once. A sane order to *deepen*:
1. **Blender fundamentals:** the classic **"Blender Donut" beginner series (Blender Guru on YouTube)** — the standard first tutorial; it teaches the whole interface via one project. Do it even though it's a donut, not a sword — the *skills* transfer.
2. **Game-art / character basics:** **Grant Abbitt** (YouTube) — friendly low-poly and game-character tutorials.
3. **Unreal basics:** Epic's own free **"Your First Hour in Unreal Engine"** and the learning portal.
4. **Practice cadence:** small finished things > big unfinished ones. Katana → a prop → a simple environment kit piece → a full character. Ship each.

> **The meta-skill:** learn to *search well.* "Blender [thing] shortcut," "UE5 IK Retargeter feet sliding," etc. Every problem you'll hit, someone has documented. This roadmap gets you unstuck on the *order*; the web gets you unstuck on the *details.*

---

## The Build Docs, in the order you'll open them
1. [`MILESTONE_0.md`](MILESTONE_0.md) — UE project setup, movement, the Manny stand-in.
2. **This roadmap** — the ordered spine.
3. [`CHARACTER_ART_PATH.md`](CHARACTER_ART_PATH.md) — deep katana / character modeling.
4. [`MESHY_TO_UNREAL.md`](MESHY_TO_UNREAL.md) — Meshy → Blender → UE, fixing colors.
5. [`RIGGING_AND_RETARGETING.md`](RIGGING_AND_RETARGETING.md) — skeleton + animation reuse.
6. [`ANIMATION_PATH.md`](ANIMATION_PATH.md) — animation deep-dive.
7. [`ENVIRONMENT_ART_PATH.md`](ENVIRONMENT_ART_PATH.md) — building the cities.
