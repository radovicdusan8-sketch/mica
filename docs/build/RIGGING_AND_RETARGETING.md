# Rigging & Retargeting — Make Ryuma Move

**Goal:** take the Ryuma mesh that's now *standing* in UE5 and make him **walk, run, jump, and fight** by rigging him to a skeleton and borrowing the Third-Person template's animations (Manny's). Beginner-paced. Direct continuation of [`MESHY_TO_UNREAL.md`](MESHY_TO_UNREAL.md) Part D; pairs with [`MILESTONE_0.md`](MILESTONE_0.md).

**Engine:** UE 5.x (your project is 5.8). The tool for reusing animations across characters is the **IK Retargeter**.

---

## The concept — why this is *two* steps

1. **Rigging** = giving the mesh a **skeleton** (bones/armature) and **skin weights** (which bone moves which part of the mesh). A mesh with no skeleton can only stand there.
2. **Retargeting** = playing animations made for **one** skeleton (Manny's) on a **different** skeleton (Ryuma's). You do this because it lets you reuse the entire Third-Person animation set (and any Marketplace/Fab animation packs) instead of animating from scratch.

> Shortcut to know up front: if your rig tool can output the **exact UE5 Mannequin skeleton** (same bone names/hierarchy), you can skip retargeting entirely — assign the Mannequin skeleton on import and reuse animations directly. Most auto-riggers *don't*, so retargeting is the reliable path below.

---

## Step 1 — Rig him (pick ONE)

**Pre-rig checklist (do this first, in Blender):**
- Pose him in a **T-pose or A-pose** (arms out straight) — auto-riggers need this.
- **Apply All Transforms** (`Ctrl+A`), scale ≈ **1.8 m**.
- Reasonably clean mesh (retopo/decimate if it's a dense Meshy blob).

**Option A — Mixamo (easiest, free).** Upload the mesh (FBX/OBJ) to mixamo.com → place the auto-rigger markers (chin, wrists, elbows, knees, groin) → it rigs him. Download as **FBX**. *Cons:* Mixamo skeleton ≠ Mannequin, so you'll retarget (Step 3). Great for a fast first result.

**Option B — Meshy auto-rig.** If the prototype is from Meshy, use its built-in **auto-rig** and download the rigged model. Same deal: retarget afterward.

**Option C — Blender (most control).** Use **AutoRig Pro** (paid, excellent, has a "UE Mannequin" export preset), **Game Rig Tools**, or **Rigify**. AutoRig Pro can output a UE-Mannequin-compatible rig — the one path that can *skip* retargeting.

*Recommendation:* start with **Mixamo or Meshy auto-rig** to get moving fast; graduate to AutoRig Pro when you want it clean and Mannequin-native.

---

## Step 2 — Import the rigged mesh into UE5

1. Drag the **rigged FBX** into the Content Browser.
2. In the import dialog: **Skeletal Mesh = ON**, **Import Textures/Materials** ON. It creates a **Skeletal Mesh** + a new **Skeleton** asset (Ryuma's own skeleton).
3. Check materials (see [`MESHY_TO_UNREAL.md`](MESHY_TO_UNREAL.md) Part C) and scale against Manny in a test level.

---

## Step 3 — Retarget Manny's animations onto Ryuma (IK Retargeter)

This is the heart of it. UE5 uses **IK Rigs** (a description of each skeleton) + an **IK Retargeter** (the translator between two IK Rigs).

1. **Source IK Rig — Manny:** UE ships one (`IK_Mannequin` / `IK_UE5Mannequin`) with the Third-Person content. Use it as-is.
2. **Target IK Rig — Ryuma:** right-click Ryuma's **Skeletal Mesh → Create → IK Rig.** Inside:
   - Set the **Retarget Root** (his **pelvis/hips** bone).
   - Define **Retarget Chains** — Spine, LeftArm, RightArm, LeftLeg, RightLeg, Head (and optionally fingers) — selecting the start/end bones of each. **Name them the same as the Mannequin's chains** so they auto-map.
3. **Create the IK Retargeter:** right-click Ryuma's IK Rig → **Create IK Retargeter.** Set **Source = Mannequin IK Rig**, **Target = Ryuma IK Rig.** Chains auto-map by name; fix any that didn't.
4. **Fix the Retarget Pose (critical):** in the retargeter, put **both** characters in a matching base pose ("Edit Pose") — if Manny is T-pose and Ryuma is A-pose, straighten Ryuma to match. **Mismatched poses = twisted, broken limbs.** This one step fixes 90% of ugly results.
5. **Preview:** pick a Manny animation in the retargeter and scrub — it should now play on Ryuma. Tweak chain settings/pose until clean.
6. **Get the animations onto him — two ways:**
   - **Bake (simplest to reason about):** in the retargeter, select the Third-Person animations → **Export Selected Animations** → you get Ryuma-skeleton copies.
   - **Live retarget (flexible):** keep Manny's Anim Blueprint and use **"Retarget Pose From Mesh"** so Ryuma is driven by Manny's animation live. More advanced.

---

## Step 4 — Put him in the game

1. **Retarget the Anim Blueprint too:** right-click the Third-Person **Anim Blueprint → Retarget Anim Blueprints → Duplicate and Retarget**, targeting Ryuma's skeleton (uses your retargeter). You get a Ryuma-driving ABP + retargeted anims in one shot.
2. Open **`BP_ThirdPersonCharacter`** (from Milestone 0):
   - **Mesh component → Skeletal Mesh = Ryuma.**
   - **Mesh component → Anim Class = the retargeted Anim Blueprint.**
   - Nudge the mesh's transform so his feet sit on the capsule floor and he faces forward (-90° Z is the usual fix).
3. **Press Play.** Run, sprint, jump — as **Ryuma**. This is the moment `SKM_Manny_Simple` gets replaced by the real character.

---

## Common gotchas (and the fix)
- **Twisted/broken limbs** → mismatched **Retarget Pose**; fix in the retargeter's *Edit Pose* (Step 3.4).
- **Feet sliding / floating / sinking** → pelvis/root retarget settings, or scale mismatch; check he's ~1.8 m and the Retarget Root is the pelvis.
- **Facing sideways / backwards** → import rotation; fix with **Apply Transforms** in Blender, or rotate the mesh component -90° Z in the character BP.
- **Way too big/small** → non-applied scale; re-apply in Blender or set uniform scale on import.
- **Fingers claw/curl weird** → finger chains optional; leave them out early, add later.
- **Animations don't appear to retarget** → chain **names** don't match between the two IK Rigs; rename Ryuma's chains to match the Mannequin's.

---

## Checklist
- [ ] Mesh in **T/A-pose**, transforms applied, ~1.8 m
- [ ] Rigged (Mixamo / Meshy / AutoRig Pro)
- [ ] Imported to UE as **Skeletal Mesh** (+ Skeleton), materials OK
- [ ] **IK Rig** for Ryuma (Retarget Root + chains, named like Mannequin's)
- [ ] **IK Retargeter** (Mannequin → Ryuma), **Retarget Pose matched**
- [ ] Animations baked/retargeted; **Anim Blueprint** retargeted
- [ ] `BP_ThirdPersonCharacter` mesh + Anim Class swapped to Ryuma
- [ ] **Play** — he moves 🎉

---

## Troubleshooting — "imported but tiny / static / invisible until I move"

Three classic symptoms, usually two root causes:

- **Character is tiny** → **unit/scale mismatch** (Blender metres vs UE centimetres). Fix at source: in Blender set height ≈ **1.8 m**, `Ctrl+A → All Transforms`, re-export/re-import. Or in UE: re-import with **Import Uniform Scale = 100**, or scale up the **Mesh** component in `BP_ThirdPersonCharacter`. (Sanity check: open the Skeletal Mesh asset — a speck next to the grid = scale bug.)
- **Invisible until he moves** → a *consequence* of being tiny: micro **bounds** get **culled** at rest and only redraw on movement. Fixing the scale fixes this. (Also check he isn't positioned sunk into the floor.)
- **Positioned wrong** → in `BP_ThirdPersonCharacter`, Mesh component **Location Z ≈ -88**, **Rotation Z = -90** (Manny defaults) so feet sit on the capsule bottom, facing forward.
- **Still static (no animation)** → no working Anim Blueprint on *his* skeleton. (1) Double-click the Skeletal Mesh and drag a retargeted anim into the preview — if it plays, the mesh is fine. (2) Set the Mesh component's **Anim Class** to the **retargeted (Ryuma-skeleton)** Anim Blueprint. (3) **#1 cause:** the mesh's **Skeleton** and the ABP's target skeleton must both be **Ryuma's** — assigning Manny's ABP to Ryuma's mesh = static.

## Troubleshooting — "rigged in Blender but the target is STATIC in the IK Retargeter"

**Key idea:** rigging in Blender gives you a **skeleton + skin weights**. The Retargeter drives motion through an **IK Rig** (Retarget **Root** + Retarget **Chains**) you must build **in Unreal**. Skeleton ≠ IK Rig. No chains = frozen target.

**10-second diagnosis** (IK Retargeter → **Asset Browser** at the bottom → click an animation):
- **Source (Mannequin) also static** → no anim selected, or toolbar is in **Edit Pose** not **Run Retarget**. Pick an anim; switch mode.
- **Source moves, target frozen** → Ryuma's IK Rig has no chains/root, or chain mapping is empty. Fix ↓.

**"I don't see Retarget Root/Chains" →** you're in the **Skeleton** asset. Those live in a separate **IK Rig** asset you must create (right-click the Skeletal Mesh → **Create → IK Rig**). *(IK Rig/Retargeter need no C++ — they're editor assets and work the same in a C++ project.)*

**Example chain setup for a Meshy/Mixamo-style rig** (bone names like `Pelvis`, `L_Upperarm`, `L_Hand`, `Spine01`): Retarget Root = **Pelvis**; chains — `Spine` (Spine01→Spine02), `LeftArm` (L_Upperarm→L_Hand), `RightArm` (R_Upperarm→R_Hand), `LeftLeg` (L_Thigh→L_Foot), `RightLeg` (R_Thigh→R_Foot), `Head` (Neck→Head), `Root` (Root→Root). Name them to match the Mannequin's chains so the retargeter auto-maps.

**Build Ryuma's IK Rig:**
1. Open his **IK Rig** (or right-click his Skeletal Mesh → **Create IK Rig**).
2. Right-click **pelvis/hips** → **Set Retarget Root.**
3. For each limb, select **start + end bone** → right-click → **New Retarget Chain**: Spine, LeftArm, RightArm, LeftLeg, RightLeg, Head (+Neck). **Name them like the Mannequin's chains.**
4. IK Retargeter → **Chain Mapping** panel: map each **Target** chain to its **Source** chain (do it by hand if bone names differ, e.g. Mixamo `mixamorig:` names won't auto-map).
5. Confirm **Source IK Rig = Mannequin**, **Target IK Rig = Ryuma** in Details.
6. Fix the **Retarget Pose** if limbs then look twisted (match Ryuma's base pose to the Mannequin's).

## Where this sits in the milestones
This completes the jump from the **Manny stand-in** (Milestone 0) to the **real Ryuma** driving the same movement/combat you build in Milestones 1–3 — with **zero-magic** animations, exactly his Prologue state. New attack/combat animations later slot into the same retargeted Anim Blueprint.
