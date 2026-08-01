# Meshy → Blender → Unreal — Getting Ryuma In (with his colors)

**Goal:** take a Meshy character prototype, retouch it in Blender **without losing its colors**, and get it into the UE5 project. Beginner-paced, mostly no-code. Companion to [`ENVIRONMENT_ART_PATH.md`](ENVIRONMENT_ART_PATH.md), [`CHARACTER_ART_PATH.md`](CHARACTER_ART_PATH.md), and [`../design/CHARACTER_DESIGN.md`](../design/CHARACTER_DESIGN.md) (Ryuma's canon look).

**Format rule (recap):** **GLB** for Meshy → Blender (packs textures), **FBX** for Blender → Unreal.

---

## Part A — "I lose the colors in Blender" (fix, in order of likelihood)

Meshy colors a model with a **baked color image (albedo PNG)**, not editor-assigned colors. "Losing" them is almost always one of these:

1. **Wrong viewport shading mode (most common).** Blender opens in **Solid** = flat grey. The textures are loaded; you can't see them. Top-right of the viewport, four spheres → click **"Material Preview"** (3rd). Colors should appear. ("Rendered," the 4th, also shows them.)
2. **Texture didn't travel with the file.** If you exported **FBX/OBJ** from Meshy, Blender may not find the PNG → grey. **Re-export from Meshy as GLB** — it embeds the textures, and they import automatically.
3. **Texture not linked (manual fix).** In the **Shading** workspace: from Meshy's download **textures** folder, drag the **base color / albedo** PNG into the node editor and connect it to **Base Color** on the Principled BSDF. (If Meshy used **vertex colors**, add a **Color Attribute** node → Base Color instead.)

> Rule of thumb: switch to Material Preview *first.* If that fixes it, there was never a problem — just the default grey shading.

---

## Part B — Retouch in Blender, then export

1. **Scale him sanely:** a human ≈ **1.8 m** tall. Meshy meshes often import tiny or huge.
2. **Apply transforms:** `Object → Apply → All Transforms` (`Ctrl+A`) so he doesn't arrive in UE rotated/mis-scaled.
3. *(Optional, recommended for game use)* **Retopo/decimate:** Meshy meshes are dense/uneven; a cleaner, lighter mesh animates and performs better. Not required just to see him.
4. **Export FBX:** `File → Export → FBX`
   - **Selected Objects** on (export just him).
   - **Path Mode → Copy**, then click the **image icon** beside it to **Embed Textures** (so PNGs ride inside the FBX). *(Or leave textures as loose files and import them into UE separately.)*

---

## Part C — Import into UE5

1. Drag the **FBX** into the **Content Browser**.
2. In the import dialog: tick **Import Textures** and **Import Materials**. For now choose **Static Mesh** just to place him and check scale/look. *(A playable character later imports as **Skeletal Mesh** with a skeleton — see Part D.)*
3. **Still grey in UE?** UE materials are separate from Blender's. Import the texture PNGs, create a **Material** (drag the base-color texture in → connect to **Base Color**), and **assign** it to the mesh's material slot. Metallic/roughness/normal textures plug into their matching pins.
4. Drop him into the test level next to Manny to sanity-check **scale** and **materials**.

---

## Part D — Next step: make him move (rigging)

Standing in the level ≠ playable. To animate him / reuse the Third-Person template's animations he must be **rigged to a skeleton**:
- **Easiest:** rig to the **UE5 Mannequin (Manny) skeleton** so he inherits all existing animations — via **Blender** (e.g. the Rigify → UE workflow or the Auto-Rig/Game-Rig tools), **Mixamo** (auto-rig, then retarget), or **Meshy's built-in auto-rig**.
- Then in UE use **IK Retargeter** to play Manny's animations on Ryuma.
- This replaces the `SKM_Manny_Simple` stand-in with the real Ryuma — the payoff of the character build path.

---

## Quick checklist
- [ ] Meshy export = **GLB** (textures embedded)
- [ ] Blender viewport = **Material Preview** (colors visible)
- [ ] Scale ≈ 1.8 m, **Apply All Transforms**
- [ ] Export **FBX**, Path Mode **Copy** + **Embed Textures**
- [ ] UE import with **Import Textures/Materials**
- [ ] Materials assigned; scale checked against Manny
- [ ] (Later) rigged to the Mannequin skeleton + IK Retarget
