# 05. Rigging and Animation

> **Written for:**
> - AccuRIG 2 (free), with Auto-Rig Pro and Rigify + Expy Kit as alternatives.
> - Rokoko Vision 3.0 for phone and video motion capture, with Move One as an iPhone alternative.
> - Blender 5.2 LTS for cleanup.
> - Cascadeur 2026.2.
> - Unreal Engine 5.8 (5.8.3): IK Rig and IK Retargeter (with 5.8's retarget operation stack), Animation Blueprints, montages, root motion, and Motion Warping.
>
> **Facts checked:** 2026-09-27. Vendor sites were blocked from this environment, so vendor facts come from search excerpts of official pages. Blender facts were read from its 5.2.2 source. Prices change often: `VERIFY:` before paying.

## What this covers

This walkthrough gets characters moving:

- a single skeleton strategy for every humanoid;
- rigging and skin-weight checks;
- retargeting animations between skeletons with Unreal's IK Retargeter;
- free placeholder animations for the gray-box prototype;
- planning and recording combat motion capture at home with a phone;
- cleanup in Blender, and keyframing and polish in Cascadeur;
- importing animations with the right root-motion settings;
- montages and notifies for combat timing;
- the Animation Blueprint for Wraith and a shared one for enemies;
- a clear decision on root motion versus in-place animation for melee.

The combat logic itself (hit detection, hit-stop, combos) is walkthrough 08. This walkthrough builds the animation assets and hooks it uses.

## Why it matters for Wraith

- **Combat feel is mostly animation.** Launchers, air combos, grabs, dodges, and hit reactions only feel weighty if the animation has clear anticipation, a fast strike, readable active frames, and a recovery that can be cancelled at the right moment.
- **Many animations, one person.** A brawler needs dozens of player moves and hit reactions, plus attacks for four archetypes and a boss. Sharing one skeleton, reusing free and bought animations, and capturing at home make that possible.
- **Enemies must telegraph.** Readable wind-ups are an animation job (walkthrough 11 sets the timing).
- **Wraith snaps to targets.** Attacks must reach the enemy the player aimed at. Root-motion attacks plus Motion Warping solve that cleanly.

## Tools

| Tool | What it's for | Cost | Commercial license OK? | AMD notes |
|---|---|---|---|---|
| AccuRIG 2 (Reallusion) | Automatic rigging and skinning of your character | Free | `VERIFY:` explicit commercial terms (Reallusion markets it as free with no license fees) | None found |
| Auto-Rig Pro (alternative) | Blender rigging with Unreal-Mannequin-compliant export | About US$50, then an optional US$12.50/year for updates | Yes | None |
| Rigify + Expy Kit (free alternative) | Blender's built-in rigger, plus a converter to a single game-ready hierarchy | Free (GPL) | Yes | None |
| Rokoko Vision 3.0 | Motion capture from phone or webcam video | Free Starter: 30 s of processing per month. Basic: about US$10/month billed yearly or US$12 monthly, for 600 s per month, retargeting, BVH, and 60 fps export. | `VERIFY:` commercial terms per plan | Processing is in the cloud |
| Move One (Move.ai, alternative) | Single-iPhone motion capture at 60 fps | Starter US$18/month (60 credits), Standard US$48/month (180 credits), plus VAT | Commercial use is defined in their terms. `VERIFY:` which plans include it. | Cloud; **iPhone only** (no official Android app found) |
| QuickMagic, DeepMotion (other alternatives) | Video motion capture | Free tiers, then about US$9–50/month | DeepMotion requires a paid plan for commercial use. `VERIFY:` QuickMagic's plans. | Cloud |
| Blender 5.2 | Cleanup, retiming, baking, weight fixes | Free | Yes | None |
| Cascadeur 2026.2 | Keyframe animation with physics help; motion-capture cleanup | Free: **no commercial use**, and exports only Cascadeur's own format. Indie: commercial use while revenue or funding stays under US$100,000/year. Pro/Teams: unrestricted. Indie is about US$8/month (secondary sources). `VERIFY:` prices. | Indie and above only | System requirements list NVIDIA GPUs; release notes mention fixes for AMD. **Test the free version on your RX 9060 XT before paying.** |
| Unreal Engine 5.8 | IK Retargeter, Animation Blueprints, montages, Motion Warping | Free | Yes | None |
| Game Animation Sample Project (Epic) | 500+ free animations on the UE5 mannequin, including motion matching | Free on Fab | Yes, in Unreal projects (the listing is marked UE-only) | None |
| Mixamo (Adobe) | Free placeholder animations | Free with an Adobe account | Yes, royalty-free in games. You can't redistribute the raw files. | None |

## Before you start

- **Walkthroughs done:** 01. **From 04:** at least one retopologized, UV'd character mesh. The first enemy archetype is the best practice subject.
- **Read ahead:** 08 (combat), so you know what the notifies and montages are for.
- **Space for capture:** a clear floor area of about 3 × 3 m, a phone on a tripod, and bright, even light.
- **Warm up before recording combat moves.** Kicks and spins on a living-room floor pull muscles. Use a padded or foam prop instead of any real weapon.

---

## Steps

### Step 1. Choose one skeleton strategy

A **skeleton** is the hierarchy of bones animations move. Animations made for one skeleton only play directly on meshes that share it; otherwise they have to be **retargeted** (converted).

- **Goal:** the fewest skeletons possible, and an easy path for bought or free animations.
- **Do this:**
  1. Compare the options:

     | Option | Cost | Result | Effort |
     |---|---|---|---|
     | **AccuRIG 2 (recommended to start)** | Free | A clean rig with fingers, exported to FBX for Unreal or Blender. Its own bone names, so you retarget from the mannequin. | Low; retargeting is mostly automatic in 5.8 |
     | **Auto-Rig Pro** | About US$50 | Can export a skeleton compliant with the Unreal mannequin (hierarchy, bone axes, UE5 naming), so mannequin animations fit directly | Low to medium |
     | **Rigify + Expy Kit** | Free | Rigify has no game-export mode. Its deform bones follow control bones through constraints, and Blender's exporter includes extra parent bones. Expy Kit converts Rigify to a single game hierarchy. | Medium to high |

  2. **Decide:**
     - **Every humanoid enemy shares one skeleton**, rigged once on the shared base body (walkthrough 04, step 14).
     - Wraith and Sister Vesper can share it, or have their own if proportions differ a lot.
     - Everything else (mocap, Mixamo, the Game Animation Sample, Fab packs) is **retargeted** onto these skeletons with the IK Retargeter (step 5).
  3. Write the decision into `docs/design/animation.md`.
- **Done when:** the skeleton plan is written down.
- **Common mistakes:**
  - A different rig per character "because the tool made it that way", then retargeting everything four times.
  - Starting with Rigify's full control rig as the export skeleton.
- **Claude can help:** Claude can draft `docs/design/animation.md`, and later write batch-retargeting scripts.
- **Time:** 30 minutes.

### Step 2. Rig a character with AccuRIG 2

- **Goal:** a rigged, skinned character ready for Blender checks and Unreal.
- **Do this:**
  1. **Prepare the mesh** in Blender:
     - the low-poly character in an **A-pose or T-pose** (AccuRIG accepts both; your turnarounds use an A-pose);
     - all parts in place;
     - scale applied, at real height.

     Export it as FBX with the settings from walkthrough 04, step 10 (no armature yet).
  2. **In AccuRIG:**
     - import the FBX;
     - follow its guided steps to place body markers, then finger markers;
     - let it generate bones and skin weights.

     It handles characters made of several meshes and rigs fingers.
  3. **Test poses** in AccuRIG's preview: arms up, squat, twist. Look for collapsing shoulders and knees.
  4. **Export** as FBX for Blender or Unreal.
  5. **In Blender:**
     - import the FBX;
     - **rename the armature object to `Armature`** (walkthrough 04, step 10 explains why);
     - check that the top bone is a root bone at the feet. `VERIFY:` AccuRIG's root bone name and whether it offers a naming preset for the Unreal mannequin;
     - save as `source-art/blender/characters/<name>/<name>_rig.blend`.
- **Done when:** the character bends plausibly in all test poses, and the Blender armature is named `Armature`.
- **Common mistakes:**
  - Rigging a mesh that isn't at its final scale.
  - Unapplied transforms, which give strange bone orientations.
  - Forgetting the fingers, which grabs need.
- **Claude can help:** through the Blender MCP, Claude can prepare and export the mesh, rename the armature, list the bone hierarchy, and pose the rig for test renders. AccuRIG itself is manual.
- **Time:** 1–2 hours per character.

### Step 3. Check and fix skin weights in Blender

**Skin weights** say how much each bone moves each vertex. Bad weights show as collapsing elbows, pinched shoulders, or armor that bends like rubber.

- **Goal:** clean deformation in combat poses, within Unreal's limits.
- **Do this:**
  1. Pose the rig in extreme combat poses: an overhead swing, a deep lunge, a high kick, and a twist.
  2. Fix problems in **Weight Paint** mode:
     - **Rigid parts** (armor plates, masks, shields) should be weighted 100% to one bone, so they don't bend.
     - **Joints** should blend smoothly across two or three edge loops.
  3. **Limit influences:** **Weights > Limit Total**. Unreal's "unlimited" influences are capped at 12 in practice. Four to eight is plenty, and fewer is cheaper. Then run **Weights > Normalize All**.
  4. **Extra bones for secondary motion** (enemy robes, tassels, a lantern on a belt): add a few bones and weight to them. They'll move with Unreal's cheap **AnimDynamics** node (step 16), not with cloth.
- **Done when:** all four extreme poses look acceptable, and no vertex has more than your chosen influence limit.
- **Common mistakes:**
  - Armor weighted to several bones, so it bends like cloth.
  - Skipping Normalize.
  - Weighting Wraith's cloak to bones when it will be simulated by Chaos Cloth. Leave it to the cloth setup (walkthrough 04, step 12).
- **Claude can help:** Claude can run Limit Total and Normalize, report vertices over the limit, and pose and render test frames through the Blender MCP. Painting weights is manual.
- **Time:** 1–3 hours per character.

### Step 4. Import the skeletal mesh into Unreal

- **Goal:** the character in Unreal with its skeleton, Physics Asset, and a clean hierarchy.
- **Do this:**
  1. Export `SK_<Name>.fbx` from Blender with the `Wraith_UE` preset (walkthrough 04, step 10): Add Leaf Bones off, armature named `Armature`.
  2. Import into `/Game/Wraith/Characters/<Name>/`:
     - **first import of a skeleton:** Skeleton empty (new), **Create Physics Asset** on;
     - **enemies sharing the base skeleton:** pick the existing skeleton, `SKEL_EnemyBase`.

     Use the normal import settings from 04, step 10.
  3. Open the skeleton asset and check the hierarchy: `root` at the top, with no extra `Armature` bone above it and no `_end` leaf bones.
  4. Open the Physics Asset and check that the capsules roughly fill the body. Cloth (walkthrough 04) and hit reactions use them.
- **Done when:** the skeleton hierarchy is clean, and the character plays the template's idle animation after retargeting (step 5).
- **Common mistakes:**
  - Importing an enemy with a new skeleton instead of `SKEL_EnemyBase`, which splits the shared animations.
  - Deleting the Physics Asset because it looks unused; cloth and hit reactions need it.
- **Claude can help:** through the Unreal MCP, Claude can list the imported skeleton's bones and flag unexpected ones.
- **Time:** 20 minutes.

### Step 5. Retarget animations with the IK Retargeter

**Retargeting** transfers an animation from one skeleton to another with different bone names or proportions. Unreal does it with an **IK Rig** per skeleton (which bones form the spine, arms, and legs) and an **IK Retargeter** that maps one IK Rig onto another.

- **Goal:** any humanoid animation (mannequin, mocap, Mixamo, packs) plays correctly on Wraith and the enemies.
- **Do this:**
  1. **The fast way (5.8):**
     - In the Content Browser, select one or more animations, right-click, and choose **Retarget Animation Assets**. The **Auto Retarget** window opens.
     - Pick the source skeletal mesh (for example the mannequin, `SKM_Manny`) and the target (`SK_Wraith`), select the animations, and set an output folder and name prefix or suffix.
     - Click **Export Animations**.
     - Also click **Export Retarget Assets** to save the IK Rigs and IK Retargeter it generated, so you can fine-tune them.
  2. **The fine-tuning way:** open the saved IK Rig for your character.
     - **Auto Create Retarget Chains** matches bone chains (spine, arms, legs, fingers) by name to built-in templates. Check each chain.
     - Set the **retarget root** (the pelvis).
  3. **Open the IK Retargeter.** 5.8 organizes retargeting as a stack of operations you can reorder. The ones that matter for combat:
     - **Pelvis Motion** scales hip movement between characters of different proportions. 5.8 adds an option to stop vertical pelvis motion being damped on shorter characters.
     - **Root Motion** copies root motion from the source, or generates it from the pelvis motion. That's essential for attacks and dodges (step 12).
     - **IK goals for the feet** keep feet planted. 5.8 lets you define a foot plane and toes on the target, and the automatic templates use them.
  4. **Fix the retarget pose** if the source is a T-pose and your character is in an A-pose. Edit the retarget pose in the IK Retargeter so both start from the same stance.
  5. Name the assets `IKR_<Skeleton>` for IK Rigs and `RTG_<Source>_To_<Target>` for retargeters. These are suggested additions to the README's prefixes.
- **Done when:** a run cycle and one attack from the mannequin play on Wraith with planted feet, no floating, and hands reaching the same places.
- **Common mistakes:**
  - Mismatched starting poses (T versus A), so the arms are rotated wrong in every frame.
  - Forgetting root motion settings, so attacks lose their forward lunge.
  - Accepting sliding feet instead of setting up the foot IK.
- **Claude can help:** Claude can script batch retargeting over whole folders through the Unreal MCP's Python. `VERIFY:` which retargeting functions 5.8 exposes to Python. It can also check naming and list animations that haven't been retargeted yet.
- **Time:** 1–2 hours for the first setup, then minutes per batch.

### Step 6. Placeholder animations for the gray box

- **Goal:** enough animation for the Milestone 2 gray-box prototype, without recording anything.
- **Do this:**
  1. **Game Animation Sample Project** (Epic, free on Fab): 500+ animations on the UE5 mannequin, including motion-matching locomotion. The 5.8 version adds interaction assets for two-character animations, which is relevant to grabs. It's licensed for Unreal projects.
     - Download it as a separate project.
     - Use **Asset Actions > Migrate** to copy the animations you need into `/Game/Wraith/Dev/PlaceholderAnims/`.
     - Retarget them onto the gray-box character.
  2. **Mixamo** (Adobe, free with an account): many punches, kicks, dodges, and hit reactions.
     - Tick **In Place** for locomotion clips.
     - Download FBX "without skin" and retarget them.
     - You may use them royalty-free in your game, but you may not redistribute the raw files, so keep them out of anything public, including your repo if you ever make it public.
  3. **Fab combat packs:** paid melee packs are often on the mannequin skeleton. Buy one only if it fits the style, and log it (walkthrough 06, step 7).
  4. Keep all placeholders under `/Game/Wraith/Dev/PlaceholderAnims/`, so it's obvious what still needs replacing.
- **Done when:** the gray-box character can idle, run, jump, do a light chain, a heavy, a dodge, a launcher, and take hits, all with placeholders.
- **Common mistakes:**
  - Placeholders scattered through final folders, which then ship.
  - Spending days choosing placeholders. Anything close is fine for a gray box.
- **Claude can help:** Claude can migrate and organize placeholders through the Unreal MCP, batch-retarget them, and keep a list of which placeholder stands in for which final animation.
- **Time:** 1–2 sessions.

### Step 7. Plan the motion-capture shot list

- **Goal:** a complete, prioritized list of moves to capture, so recording sessions stay focused and fit the capture budget.
- **Do this:**
  1. Create `docs/design/mocap-shotlist.md` with one row per take: ID, character, move, notes, priority, and status. For example:

     | Take ID | Character | Move | Notes | Priority |
     |---|---|---|---|---|
     | W_LIGHT_01 | Wraith | Light attack 1 | Fast jab-slash, recovers to guard | Slice |
     | W_LAUNCH_01 | Wraith | Launcher | Rising strike, ends looking up | Slice |
     | W_DODGE_F | Wraith | Dodge forward | Low roll or slide | Slice |
     | E_CULT_ATK_01 | Shielded cultist | Shield bash | Clear wind-up, 0.5 s or more (walkthrough 11) | Slice |
     | VES_P1_ATK_01 | Sister Vesper | Phase 1 attack | Per the boss design (walkthrough 11) | Slice |

  2. **Cover these groups:**
     - **Wraith:** locomotion extras (starts and stops), light chain (3–4), heavy, launcher, air-attack poses (captured on the ground), slam, dodges in four directions, grab and throw, hit reactions (front, back, left, right; light and heavy), knockdown and get-up, taunts or idles.
     - **Each enemy archetype:** idle, walk, attack wind-up + strike + recovery, hit reactions, death.
     - **Vesper:** the full boss moveset.
  3. **Budget the capture seconds.** With Rokoko Vision's Basic plan (600 s of processing per month), 40 moves × 3 takes × 5 s = 600 s, exactly one month. Prioritize slice moves; placeholders or bought animations cover the rest.
  4. Air combos can't be performed in the air at home. Capture the upper-body motion standing, then lift and arc it in Cascadeur (step 11).
- **Done when:** the shot list covers every slice move and fits your capture budget.
- **Common mistakes:**
  - Capturing moves you could get from placeholders or packs, and running out of capture seconds for signature moves.
  - No enemy wind-ups on the list; telegraphs are what make enemies fair (walkthrough 11).
- **Claude can help:** Claude can build the shot list from the combat design (walkthrough 08) and enemy designs (walkthrough 11), estimate capture seconds, and track status.
- **Time:** 1 hour.

### Step 8. Record motion capture at home

- **Goal:** clean video that the capture service turns into usable animation.
- **Do this:** follow Rokoko's published best practices, plus combat-specific additions.
  1. **Camera:**
     - on a tripod, completely still (handheld or panning footage fails);
     - at chest height, pointing straight at you;
     - at least 2 m from the capture area;
     - no wide-angle lens.
  2. **Framing:** your whole body, head to soles, must stay in frame for the entire take, including kicks and jumps. Check the extremes before recording.
  3. **Light:** bright, even, diffuse light. Avoid harsh spotlights that throw dark shadows on the floor.
  4. **Clothing:** fitted clothes that contrast with the background and make joints obvious. No loose sleeves, long coats, or capes. Wraith's cloak comes from cloth simulation, not from you.
  5. **Two cameras (optional, better):** Rokoko Vision supports a dual-camera setup, calibrated with two A4 or Letter sheets on something hard and flat, with the cameras about 45–90° apart. Occluded arms and legs track much better.
  6. **Each take:**
     - Start in a neutral pose for a second.
     - Say the take ID out loud as a slate.
     - Perform.
     - End in a neutral pose.

     Record three takes per move.
  7. **Fast moves:** very fast strikes may blur and track poorly. Perform them at about 80% speed and speed them up during cleanup (step 10). Use your phone's highest frame rate and plenty of light to keep motion blur down. This is general video advice, not a Rokoko rule.
  8. **Safety:** warm up, clear the space, and use a foam or padded prop for weapons.
- **Done when:** every slice move has at least two usable takes on video, named by take ID.
- **Common mistakes:**
  - Feet leaving the frame on kicks.
  - Handheld phone.
  - Baggy clothing.
  - Dark rooms.
  - Forgetting the slate, then not knowing which take is which.
- **Claude can help:** Claude can turn the shot list into a printable session sheet and rename video files from your notes. Recording is you.
- **Time:** 1–2 hours per session.

### Step 9. Process the capture and export animation

- **Goal:** animation files on a skeleton you can retarget.
- **Do this:**
  1. **Upload and process** the takes in Rokoko Vision, or your chosen service. Watch every result before exporting; reject bad takes instead of trying to clean them.
  2. **Export as FBX** at 60 fps (a paid-plan feature in Rokoko). Rokoko's exporter has skeleton presets including the **UE5 mannequin**; choose it to make retargeting trivial.
  3. Save the raw exports in `source-art/mocap/raw/` (or in the outside-the-repo raw folder, if you chose that in walkthrough 01, step 4), named by take ID.
- **Done when:** each usable take is an FBX on the mannequin skeleton, named by take ID.
- **Common mistakes:** exporting at 30 fps and then fighting jitter in fast moves.
- **Claude can help:** Claude can rename and sort exports, and check frame rates and lengths.
- **Time:** 5–10 minutes per take.

### Step 10. Clean up in Blender

- **Goal:** mocap without jitter, sliding feet, or dead frames.
- **Do this:**
  1. **Import** the FBX into a cleanup file with your target rig, or keep it on the mannequin skeleton and clean it before retargeting.
  2. **Trim** the neutral poses and the slate from the start and end.
  3. **Smooth jitter** in the Graph Editor: select the noisy channels and use **Key > Smooth > Butterworth Smooth**. Blender describes it as keeping the curve's general shape while smoothing, which preserves the peaks of strikes. Lower the **Frequency Cutoff** for more smoothing. Use **Smooth (Gaussian)** for gentler, simpler smoothing.
  4. **Thin the keys:** **Key > Density > Decimate** removes keys that barely affect the curve, which makes later hand edits easier.
  5. **Retime:** speed up moves you performed slowly (step 8) by scaling keys in the Dope Sheet. Hold the strike's contact frame, and shorten the anticipation for player attacks.
  6. **Feet:** fix sliding by keying the foot bones still during contact, or leave foot sliding to Cascadeur's cleanup (step 11), which is built for it.
  7. **Bake** if you used constraints: **Object > Animation > Bake Action** with **Visual Keying** and **Clear Constraints**.
  8. Export with the `Wraith_UE` preset, animation only, as `A_<Character>_<Move>_<nn>.fbx`.
- **Done when:** the cleaned animation reads well at full speed, with no visible jitter or sliding.
- **Common mistakes:**
  - Over-smoothing, so strikes lose their snap.
  - Leaving the slate frames in.
- **Claude can help:** through the Blender MCP, Claude can trim frames, run the smoothing and decimation operators on chosen bones, bake, and export in batches. Judging the motion is yours.
- **Time:** 20–60 minutes per clip.

### Step 11. Keyframe and polish in Cascadeur

**Cascadeur** is an animation tool with physics help:
- **AutoPosing** moves the whole body naturally when you move a few controllers.
- **AutoPhysics** makes jumps, falls, and impacts physically plausible.
- **Animation Unbaking** turns dense mocap into editable keyframes.
- Its mocap cleanup fixes foot sliding, knee pops, and body parts passing through each other.

- **Goal:** combat animations with weight: air combos, slams, heavy hits, and anything you couldn't capture.
- **Do this:**
  1. **License first:**
     - The free version doesn't allow commercial use and only exports Cascadeur's own format.
     - **Indie** allows commercial use while your revenue or funding is under US$100,000 a year. An annual Indie or Pro plan becomes a perpetual license after one year, for the last version released while you were subscribed.
     - Test the free version on your AMD card first. The system requirements list NVIDIA GPUs, though release notes mention AMD fixes.
  2. **Set up your rig** in Cascadeur (its rig setup tool maps your skeleton's bones). `VERIFY:` the current workflow name in 2026.2.
  3. **Mocap polish:** import a cleaned take, use **Animation Unbaking** to get editable keys, and fix feet and knees with the cleanup tools.
  4. **Keyframe what mocap can't do:**
     - Launchers and air combos: start from the grounded upper-body take, then lift and arc the body with AutoPhysics.
     - Slams: exaggerate the fall.
     - Heavy hit reactions: push the impact frame.
  5. **Combat timing rules:**
     - **Player attacks:** short anticipation (responsiveness), a clear strike frame, and a recovery that walkthrough 08 can cancel into the next attack.
     - **Enemy attacks:** long, readable anticipation (the telegraph, walkthrough 11), then a fast strike.
     - Exaggerate key poses so they read as silhouettes.
  6. **Export** FBX for Unreal. Cascadeur 2026.1 added an **Unreal Engine Live Link** that streams animation into the editor while you work, which is useful for checking timing in context.
- **Done when:** the slice's key combat animations (launcher, air combo hits, slam, Vesper's signature attacks) exist and feel heavy at full speed in Unreal.
- **Common mistakes:**
  - Using the free version for animations you intend to ship.
  - Physically "correct" but lifeless motion. Exaggerate for games.
  - Long player anticipation, which makes controls feel sluggish.
- **Claude can help:** Claude can manage files, versions, and the shot list, and review timing numbers (frame counts of anticipation, strike, and recovery) against walkthrough 08's targets. The animating is yours.
- **Time:** 1–4 hours per animation.

### Step 12. Import animations into Unreal, with root motion set correctly

**Root motion** means the animation itself moves the character: the forward lunge of an attack is in the animation's root bone, and Unreal moves the capsule to match. **In-place** animations don't move; code moves the character.

- **Goal:** animations imported onto the right skeleton, with root motion on exactly where it should be.
- **Do this:**
  1. **Import** each `A_*.fbx` onto the character's skeleton: in the import dialog, pick the Skeleton and import animations only.
  2. **Decide root motion per animation:**

     | Animation type | Root motion? | Why |
     |---|---|---|
     | Idle, walk, run, strafe | **In place** (off) | Movement code controls speed and turning, so controls stay responsive |
     | Attacks, launchers, slams | **On** | The lunge distance is authored exactly; Motion Warping adjusts it toward the target (step 13) |
     | Dodges and rolls | **On** | Precise distance and timing for invulnerability windows |
     | Grabs and throws | **On** | Both characters' positions must line up |
     | Hit reactions and knockdowns | **On** | The knockback distance matches the animation |
     | Jump and fall loops | In place | Physics handles the arc |

  3. For root-motion animations, open the animation and, in **Asset Details > Root Motion**, tick **Enable Root Motion**. Set **Root Motion Root Lock** (usually "Anim First Frame") so the character doesn't jump back to the start when the animation ends.
  4. Check that each root-motion animation actually has movement on its `root` bone. If mocap put the motion on the hips instead, extract root motion first: the IK Retargeter's **Root Motion** operation can generate it from the pelvis (step 5), and Cascadeur has a motion-generation tool.
- **Done when:** each attack lunges the expected distance in a test map without the character snapping back, and locomotion stays in place.
- **Common mistakes:**
  - Root motion on locomotion, which feels floaty and unresponsive.
  - Root motion missing on attacks, so they "skate".
  - Motion on the hips instead of the root, so the mesh leaves the capsule.
- **Claude can help:** Claude can set root-motion flags in bulk through the Unreal MCP's Python, using the naming convention (for example every `A_*_ATK_*` gets root motion), and list animations whose root bone never moves.
- **Time:** minutes per batch.

### Step 13. Montages, notifies, and Motion Warping

An **Animation Montage** is a container for one or more animations that code can play on demand, split into sections (for example the four hits of a combo) and marked with **notifies**. A **notify** is an event at a moment in the animation; a **notify state** is a window with a start and an end.

- **Goal:** combat montages with timing windows that walkthrough 08's code reads.
- **Do this:**
  1. **Create the notify-state classes now as empty shells**, so you can place them while animating. Walkthrough 08 adds the logic. Ask Claude to add, for example, `WAnimNotifyState_HitWindow.h`:
     ```cpp
     #pragma once

     #include "CoreMinimal.h"
     #include "Animation/AnimNotifies/AnimNotifyState.h"
     #include "WAnimNotifyState_HitWindow.generated.h"

     /** Frames where an attack can hit. Walkthrough 08 adds the hit detection. */
     UCLASS(meta = (DisplayName = "Wraith Hit Window"))
     class WRAITHGAME_API UWAnimNotifyState_HitWindow : public UAnimNotifyState
     {
         GENERATED_BODY()

     public:
         /** Which attack's data (damage, hit-stop, reaction) this window uses. */
         UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Hit")
         FName AttackId;
     };
     ```
     Do the same for **`UWAnimNotifyState_ComboWindow`** (when the next attack input is accepted) and **`UWAnimNotifyState_Invulnerable`** (dodge invulnerability frames). Build with the editor closed.
  2. **Create montages** from the attack animations (right-click an animation > **Create > Create AnimMontage**). Name them `AM_<Character>_<Move>`; `AM_` is a suggested addition to the README's prefixes.
     - **Slot:** use `DefaultSlot` for full-body attacks. Create an `UpperBody` slot if you want hit reactions while running.
     - **Sections:** the light chain is one montage, `AM_Wraith_LightChain`, with sections `Light1` to `Light4`. Walkthrough 08 jumps between sections on input.
  3. **Place the notify states** on each montage's Notifies track: right-click, **Add Notify State**, pick a class.
     - **Wraith Hit Window** from the first to the last frame the weapon can hit, with its `AttackId` set.
     - **ComboWindow** from late in the strike through the recovery.
     - **Invulnerable** on dodges.
  4. **Motion Warping** (enable the **Motion Warping** plugin in **Edit > Plugins** first). It stretches or bends a root-motion animation so the attack lands on a target:
     - Add a **Motion Warping** notify state over the lunge part of each attack.
     - Set its root motion modifier to **Skew Warp**. (Simple Warp is deprecated.)
     - Give it the warp target name `AttackTarget`.

     In walkthrough 08, code calls **Add or Update Warp Target from Location and Rotation** with the chosen enemy's position before playing the montage.
  5. **Plain notifies** for effects and sound:
     - `FootL` and `FootR` on foot contacts (footprints, walkthrough 06);
     - `WhooshStart` for swing sounds (walkthrough 15);
     - `ImpactFX` for effects (walkthrough 14).
- **Done when:**
  - Wraith's light chain, heavy, launcher, dodge, and grab montages exist, with hit, combo, and invulnerability windows placed;
  - the lunge sections have Motion Warping windows;
  - footstep notifies are on the locomotion animations.
- **Common mistakes:**
  - Hit windows longer than the visible strike, so hits connect before the weapon arrives.
  - Combo windows too early, so inputs chain before the strike lands.
  - Warp windows over the whole animation, including the recovery.
- **Claude can help:** Claude writes the notify-state classes. Placing notifies is visual work in the editor. `VERIFY:` whether Epic's MCP toolsets can edit montage notifies; if so, Claude can place them from a timing table you give it.
- **Time:** 30–60 minutes per character's move set, after the first.

### Step 14. Wraith's Animation Blueprint

An **Animation Blueprint** decides every frame which animation poses to play and how to blend them.

- **Goal:** `ABP_Wraith` handles locomotion, jumping, and falling itself, and plays combat montages on top.
- **Do this:**
  1. **A thin C++ base class** holds the values the graph needs. Ask Claude to add `WAnimInstance.h` and `.cpp`:
     ```cpp
     // WAnimInstance.h
     #pragma once

     #include "CoreMinimal.h"
     #include "Animation/AnimInstance.h"
     #include "WAnimInstance.generated.h"

     UCLASS()
     class WRAITHGAME_API UWAnimInstance : public UAnimInstance
     {
         GENERATED_BODY()

     protected:
         virtual void NativeUpdateAnimation(float DeltaSeconds) override;

         /** Horizontal speed in cm/s, for the locomotion blend space. */
         UPROPERTY(BlueprintReadOnly, Category = "Wraith|Animation")
         float GroundSpeed = 0.f;

         UPROPERTY(BlueprintReadOnly, Category = "Wraith|Animation")
         bool bIsInAir = false;

         /** True while the character is being pushed by movement input. */
         UPROPERTY(BlueprintReadOnly, Category = "Wraith|Animation")
         bool bIsAccelerating = false;
     };
     ```
     ```cpp
     // WAnimInstance.cpp
     #include "WAnimInstance.h"

     #include "GameFramework/Character.h"
     #include "GameFramework/CharacterMovementComponent.h"

     void UWAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
     {
         Super::NativeUpdateAnimation(DeltaSeconds);

         const ACharacter* Character = Cast<ACharacter>(TryGetPawnOwner());
         if (!Character)
         {
             return;
         }
         const UCharacterMovementComponent* Movement = Character->GetCharacterMovement();
         GroundSpeed = Movement->Velocity.Size2D();
         bIsInAir = Movement->IsFalling();
         bIsAccelerating = Movement->GetCurrentAcceleration().SizeSquared() > UE_KINDA_SMALL_NUMBER;
     }
     ```
  2. **Create `ABP_Wraith`** with parent class `WAnimInstance`, for the Wraith skeleton.
  3. **AnimGraph:**
     - A **Locomotion** state machine:
       - **Idle/Move** uses a **Blend Space** `BS_Wraith_Locomotion` driven by `GroundSpeed`: idle at 0, walk around 150–250, run at 500, matching the template's `MaxWalkSpeed` (walkthrough 06, step 1).
       - **JumpStart**, **FallLoop**, and **Land**, driven by `bIsInAir`.
     - After the state machine, a **Slot** node (`DefaultSlot`), so montages play over locomotion.
     - Optionally a **Layered blend per bone** from the spine up, with the `UpperBody` slot, for hit reactions while running.
  4. **Class Defaults > Root Motion Mode: Root Motion from Montages Only.** Attacks and dodges (montages) move the character; locomotion doesn't. This is the default; confirm it.
  5. Assign `ABP_Wraith` to the character's skeletal mesh component (walkthrough 08 builds the character class).
- **Done when:** Wraith idles, walks, runs, jumps, and lands smoothly, and playing any combat montage from a test key overrides locomotion and then blends back.
- **Common mistakes:**
  - Game logic in the Animation Blueprint. It should only read state and pick poses; combat decisions live in C++ (walkthrough 08).
  - Blend space speeds that don't match movement speeds, so feet slide.
- **Claude can help:** Claude writes the C++ base class and builds. It can describe the AnimGraph node by node; building the graph is manual, unless Epic's MCP toolsets can create it. `VERIFY:` Blueprint graph editing support.
- **Time:** 2–3 hours.

### Step 15. Decide root motion versus in-place, once

- **Goal:** one clear, written rule the whole project follows.
- **Do this:** write this into `docs/design/animation.md`, adjusted as you see fit:
  > Locomotion is in place and driven by Character Movement, for responsive control. Attacks, dodges, grabs, and hit reactions are root-motion montages, so distances and timing are exactly as animated. Attacks use Motion Warping (Skew Warp, target `AttackTarget`) to reach the chosen enemy. The Animation Blueprint uses Root Motion from Montages Only.

  **Why this split:** in-place locomotion gives instant, tunable control. Root-motion combat gives precise lunges, dodge distances, and grab alignment. Motion Warping fixes root motion's weakness, which is not knowing where the enemy is.
- **Done when:** the rule is written down and every animation follows it (step 12's table).
- **Common mistakes:** exceptions made "just this once", such as a root-motion walk for one enemy, which later breaks AI movement and speed tuning.
- **Claude can help:** Claude can audit all animations against the rule and list violations.
- **Time:** 10 minutes.

### Step 16. Enemies: one shared Animation Blueprint, many archetypes

- **Goal:** four archetypes animated for the effort of about one.
- **Do this:**
  1. **`ABP_EnemyBase`** on the shared enemy skeleton, with parent `WAnimInstance`: locomotion, hit reactions, death, and a slot for attack montages.
  2. **One child Animation Blueprint per archetype:** right-click `ABP_EnemyBase` > **Create Child Blueprint Class**. In each child, use **Asset Override** to swap the blend space and animations for that archetype (for example a heavier walk for the heavy).
  3. **Secondary motion:** use an **AnimDynamics** node for the robe, tassel, or chain bones from step 3. It's cheap, looks alive, and needs no cloth simulation.
  4. **Attacks** are montages per archetype, with the same notify states as Wraith, so walkthrough 08's hit detection works for enemies too.
- **Done when:** all four archetypes use children of `ABP_EnemyBase`, and each has idle, move, attack, hit, and death.
- **Common mistakes:**
  - Four copied Animation Blueprints that drift apart.
  - Real cloth on crowd enemies.
- **Claude can help:** Claude can set up the parent and child structure through the Unreal MCP, and track which archetype still uses placeholders.
- **Time:** 1–2 sessions for the base, less per archetype.

---

## Vertical slice checklist

- [ ] `docs/design/animation.md` with the skeleton strategy and the root-motion rule
- [ ] Shared enemy skeleton `SKEL_EnemyBase` rigged (AccuRIG or alternative), weights checked in combat poses
- [ ] Wraith and Vesper rigged, armature named `Armature`, no extra root or leaf bones in Unreal
- [ ] IK Rigs and IK Retargeters for mannequin → Wraith, mannequin → enemy, and capture skeleton → each, with root motion and foot IK set
- [ ] Gray-box placeholder set (Game Animation Sample, Mixamo) retargeted in `/Game/Wraith/Dev/PlaceholderAnims/`
- [ ] `docs/design/mocap-shotlist.md` covering all slice moves within the capture budget
- [ ] Capture sessions recorded (two usable takes or more per slice move), processed, exported at 60 fps
- [ ] Cleaned takes (Blender) and polished key animations (Cascadeur Indie or better): launcher, air hits, slam, Vesper's signature attacks
- [ ] All slice animations imported with correct root-motion flags
- [ ] Notify-state shells (HitWindow, ComboWindow, Invulnerable) built; slice montages have windows placed
- [ ] Motion Warping plugin enabled; Skew Warp windows on attack lunges
- [ ] `ABP_Wraith` (C++ base `UWAnimInstance`) with locomotion and slots; Root Motion from Montages Only
- [ ] `ABP_EnemyBase` plus one child per archetype, with AnimDynamics secondary motion
- [ ] Wraith's cloak cloth (walkthrough 04, step 12) tested against the final combat montages

## Going further

- **Motion Matching** (Pose Search plugin) for locomotion that picks the best animation frame automatically. The Game Animation Sample Project is the reference. It's beautiful but more complex; add it after the slice if locomotion feels stiff.
- **Two-character interactions** for grabs, using the Game Animation Sample's interaction assets and "Motion Match Multi" (new in its 5.8 version).
- **Control Rig** in Unreal for procedural touches: look-at, hand placement on a grabbed enemy, foot placement on stairs.
- **Cascadeur's Live Link** to iterate combat timing directly against gameplay.
- **Facial animation** for unmasked characters in cutscenes (walkthrough 12).

## References

**Epic Games** (5.8 documentation)
- IK Rig animation retargeting: https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine
- Retargeting operation stack (5.8): https://dev.epicgames.com/documentation/en-us/unreal-engine/retargeting-operation-stack-in-unreal-engine-5-8
- Auto retargeting: https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-retargeting-in-unreal-engine
- Retargeting bipeds with IK Rig: https://dev.epicgames.com/documentation/en-us/unreal-engine/retargeting-bipeds-with-ik-rig-in-unreal-engine
- Root motion: https://dev.epicgames.com/documentation/en-us/unreal-engine/root-motion-in-unreal-engine
- Animation montages: https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-montage-in-unreal-engine
- Animation notifies: https://dev.epicgames.com/documentation/unreal-engine/animation-notifies-in-unreal-engine
- Motion Warping: https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-warping-in-unreal-engine
- Motion Matching: https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-matching-in-unreal-engine
- Game Animation Sample Project (5.8): https://www.unrealengine.com/tech-blog/download-the-latest-game-animation-sample-project-now-updated-for-ue-5-8

**Rigging**
- AccuRIG: https://actorcore.reallusion.com/auto-rig/accurig
- Auto-Rig Pro (game engine export): https://lucky3d.fr/auto-rig-pro/doc/ge_export_doc.html
- Expy Kit (Rigify to game hierarchy): https://github.com/pKrime/Expy-Kit

**Motion capture**
- Rokoko Vision: https://www.rokoko.com/products/vision
- Rokoko pricing: https://www.rokoko.com/pricing
- Rokoko Vision 3.0 capture best practices: https://support.rokoko.com/hc/en-us/articles/48823622640785-Best-Practices-for-Video-Capture-Rokoko-Vision-3-0
- Rokoko Vision capture space setup (dual camera): https://support.rokoko.com/hc/en-us/articles/29064372040977-Capture-Space-Setup-Rokoko-Vision
- Move One (Move.ai): https://docs.move.ai/knowledge/move-one-ios-app

**Animation tools**
- Blender Graph Editor, F-curve editing (smoothing, decimate): https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/editing.html
- Cascadeur plans: https://cascadeur.com/plans
- Cascadeur licensing FAQ: https://cascadeur.com/blog/general/cascadeurs-new-licensing-structure-comprehensive-faq
- Mixamo FAQ (license): https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html

**Recommended learning**
- Masahiro Sakurai on Creating Games (YouTube; animation timing, anticipation, and hit feel; used again in walkthrough 08): https://www.youtube.com/@sora_sakurai_en
- Unreal Engine on YouTube (official; animation and Motion Matching talks): https://www.youtube.com/@UnrealEngine
