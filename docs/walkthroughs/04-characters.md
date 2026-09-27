# 04. Characters

> **Written for:**
> - Blender 5.2 LTS (FBX exporter 5.15).
> - Marvelous Designer 2026.x.
> - Adobe Substance 3D Painter 2026, or ArmorPaint 1.0, or Blender with the Ucupaint add-on.
> - Unreal Engine 5.8 (5.8.3): Substrate materials, skeletal mesh import, and Chaos Cloth with the Dataflow-based Cloth Panel Editor, production-ready and the default in 5.8.
>
> **Facts checked:** 2026-09-27. Vendor sites (Epic, Adobe, Marvelous Designer) were blocked from this environment, so their facts come from search excerpts of official pages. Blender facts were read from Blender's source code. Export settings follow Epic's own "Send to Unreal" add-on defaults. Unconfirmed items are marked `VERIFY:`.

## What this covers

This walkthrough turns the turnaround sheets from walkthrough 03 into game-ready characters:

- choosing to make, adapt, or buy each character, with a budget for each;
- setting Blender up for character work;
- starting from a free base mesh, then blocking and sculpting;
- building Wraith's tattered cloak in Marvelous Designer;
- retopology (a clean, animation-friendly low-poly mesh), UVs, and baking;
- texturing in Substance 3D Painter, or a free alternative;
- exporting to Unreal with settings that avoid the classic scale and bone problems;
- Substrate character materials;
- Chaos Cloth, so the cloak moves in combat.

Rigging and animation are walkthrough 05. This one hands a finished, skinnable mesh to it, and takes the rigged result back for cloth.

## Why it matters for Wraith

- **Wraith's cloak is the game's signature motion.** In a dark, foggy brawler, the player tracks their character by silhouette, and the tattered cloak is that silhouette. It has to look good and move well during launchers, dodges, and air combos without exploding or clipping.
- **Readability beats detail.** Enemies are seen in fog, in snow, mid-combo. Clear shapes and clean value contrast (walkthrough 03) matter more than pore-level detail.
- **Crowds cost performance.** Four to eight enemies plus Wraith and effects share the GPU budget. Enemy characters need modest budgets and shared parts.
- **Solo time is the real limit.** A hero character can take weeks. Share bases, skeletons, and materials between enemies, and buy what fits the style.

## Tools

| Tool | What it's for | Cost | Commercial license OK? | AMD notes |
|---|---|---|---|---|
| Blender 5.2 LTS | Modeling, sculpting, retopology, UVs, baking, export | Free (GPL) | Yes | Cycles baking on the RX 9060 XT through HIP (RDNA 4 is included in 5.2's builds) |
| Blender Studio Human Base Meshes | Starting bodies, heads, and hands | Free (CC0) | Yes | None |
| MPFB2 (MakeHuman for Blender) | Parametric human base meshes | Free (GPLv3 code; CC0 assets; no claim on your output) | Yes | None |
| Marvelous Designer 2026 | Wraith's cloak; other cloth | Personal: US$39/month or US$280/year | Yes for individuals, freelancers, and sole proprietors. Companies of two or more people need Enterprise; an Indie Studio tier exists for teams under US$500k revenue. | **GPU simulation uses NVIDIA CUDA only.** On the RX 9060 XT it simulates on the CPU: slower, but fine for one cloak. |
| Adobe Substance 3D Painter 2026 (recommended) | Texturing | Subscription (Substance 3D Texturing, about US$24.99/month or US$249.88/year), or a perpetual "Substance 3D Painter 2026" license on Steam (about US$199.99). `VERIFY:` both prices. | Subscription: yes. **Steam license: Adobe community answers conflict on commercial use.** `VERIFY:` in Adobe's license text before buying. | AMD Radeon GPUs are supported. The Iray renderer is NVIDIA-only (you don't need it). GPU ray-traced baking only works on "compatible hardware". `VERIFY:` on RDNA 4; it falls back to CPU baking. |
| ArmorPaint 1.0 (budget alternative) | Texturing | Official binaries are paid (about US$19); the source code is free under the zlib license | Source license allows commercial use. `VERIFY:` terms for binaries and outputs. | Runs on Direct3D 12 and Vulkan |
| Blender + Ucupaint (free alternative) | Layer-based texture painting in Blender | Free (GPL-3.0) | Yes | Uses Blender's GPU paths |
| RetopoFlow 4 (optional) | Faster retopology in Blender | Paid, sold on Superhive. `VERIFY:` the price; sources disagree. | Yes | None |
| Quad Remesher (optional) | Automatic quad remeshing | **The US$59.90 Indie perpetual license isn't for commercial use.** Commercial: US$15.99 per 3 months, or a US$139.90 Pro perpetual license. | Only with the commercial licenses | None |
| Unreal Engine 5.8 | Import, materials, Chaos Cloth | Free | Yes | None |
| MetaHuman (in Unreal) | Realistic faces for unmasked characters in cutscenes | Free under the Unreal license; usable in other engines since 2025 | Yes | Heavy; check VRAM in walkthrough 17 |

## Before you start

- **Walkthroughs done:** 01. **Inputs from 03:** canon sheets and aligned turnarounds, loaded in Blender (03, step 12).
- **Read alongside:** 05. Rigging happens between this walkthrough's export test (step 10) and the cloth step (step 12).
- **Your first character should be an enemy archetype,** not Wraith. Make your beginner mistakes on a character that matters less. The shielded cultist or the heavy are good first choices.

---

## Steps

### Step 1. Decide make, adapt, or buy, and set budgets

- **Goal:** every slice character has a plan and a performance budget before modeling starts.
- **Do this:**
  1. Decide per character:

     | Character | Plan | Why |
     |---|---|---|
     | Wraith | Make (hero quality) | The player's character and the game's identity |
     | Sister Vesper | Make (hero quality) | Boss, on screen for a whole fight, story-critical |
     | Four enemy archetypes | Adapt: one shared base body plus modular parts | They're seen in crowds; sharing saves weeks |
     | Props (weapons, shields, lanterns) | Make or buy on Fab | Buy if a pack fits the style (walkthrough 06, step 7) |
     | Unmasked story characters in cutscenes | Consider MetaHuman (walkthrough 12) | Realistic faces and facial animation come built in |

  2. Set **starting budgets**. They're not Epic's numbers (Epic publishes none for PC characters); they're sensible starting points to confirm with profiling in walkthrough 17:

     | | Triangles (LOD0, including cloth) | Material slots | Textures | Bones |
     |---|---|---|---|---|
     | Wraith | 60,000–100,000 | 3–4 | 4K for body and cloak, 2K for small parts | Mannequin-like skeleton plus cloak or extra bones |
     | Sister Vesper | 60,000–100,000 | 3–4 | 4K | Same |
     | Each enemy | 20,000–50,000 | 1–3 | 2K (4K for the heavy if needed) | One shared skeleton |

  3. **Know what costs what** (from Epic's performance guidelines):
     - each material slot is a separate draw call;
     - UV seams and hard edges add vertices;
     - skinned vertices cost more than static ones;
     - each LOD (lower-detail version for distance) should at least halve the vertex count.

     Nanite now has a checkbox on skeletal meshes too ("Enable Nanite Support"). Its maturity in 5.8 is unconfirmed, so don't rely on it for the slice; use normal LODs.
- **Done when:** `docs/design/characters.md` lists each slice character with its plan and budget.
- **Common mistakes:**
  - Sculpting a million-polygon hero with no budget and then fighting to reduce it.
  - A separate skeleton per enemy. Walkthrough 05 shares one.
- **Claude can help:** Claude can draft the character design doc from the canon sheets and budgets, and keep it updated.
- **Time:** 1 hour.

### Step 2. Set up Blender for character work

- **Goal:** a clean, consistent `.blend` structure per character.
- **Do this:**
  1. Open the file from walkthrough 03, step 12 (`<name>_model.blend`, with the turnarounds at real height).
  2. **Units:** Metric, Unit Scale **1.0**, as for everything else in this project.
  3. **Collections:**
     - `High`: sculpts for baking;
     - `Low`: game meshes;
     - `Cloak`: Marvelous Designer imports and the cloak's render and sim meshes;
     - `Rig`: filled in walkthrough 05;
     - `Export`: only what goes to Unreal.
  4. **Naming:**
     - game meshes end in `_low` and their sculpted versions in `_high`, with matching base names (`Mask_low` / `Mask_high`). The bakers match by name.
     - The final export file is `SK_<Name>.fbx`.
  5. **Symmetry:** model one side with a **Mirror** modifier; apply it only when you add asymmetric details.
- **Done when:** the collections exist and the turnarounds line up at real height.
- **Common mistakes:**
  - Different unit settings in different files, so parts come out 100 times off.
  - `_low` and `_high` names that don't match exactly, so bakes project the wrong detail.
- **Claude can help:** through the Blender MCP, Claude can create the collection structure, check names and units, and flag objects in the wrong collection.
- **Time:** 15 minutes.

### Step 3. Start from a base mesh

A **base mesh** is a ready-made, clean human body you reshape instead of modeling from nothing.

- **Goal:** a body with good topology that matches the turnaround's proportions.
- **Do this:**
  1. Download **Blender Studio's Human Base Meshes** (CC0, free to use in anything). It has 17 meshes, including realistic and stylized bodies, heads, hands, and feet, as `.blend` files. Append the body closest to your character (**File > Append**).
  2. Alternatively, install **MPFB2** (the MakeHuman plugin for Blender 4.2+) and dial in proportions with sliders. Its assets are CC0 and its authors claim nothing in your output.
  3. **Fit it to the turnaround:** in the Front and Side views, use proportional editing, the Lattice modifier, or sculpting (Grab and Snake Hook brushes) to match the silhouette. Don't worry about clothes yet.
  4. Keep the base's clean edge loops at the joints. You'll want them when you rig in walkthrough 05.
- **Done when:** the body matches the front and side turnarounds within a centimeter or two at the key landmarks.
- **Common mistakes:** starting from scratch "to learn". It's slower and usually gives worse deformation. Learn on the base; model from scratch later if you want to.
- **Claude can help:** through the Blender MCP, Claude can append the base, scale it to the design height, and position it on the references.
- **Time:** 1–2 hours.

### Step 4. Block out and sculpt the high-poly model

- **Goal:** a detailed high-poly model (armor, masks, straps, folds) to bake onto the game mesh.
- **Do this:**
  1. **Blockout:** model armor pieces, masks, belts, and bags as separate simple objects over the base body, following the canon sheet.
  2. **Hard surfaces** (porcelain masks, armor plates, buckles): model with bevels and supporting edges, or booleans, keeping them clean.
  3. **Organic detail** (folds, wear, stitching): in Sculpt Mode, add a **Multiresolution** modifier to each piece and sculpt at higher levels. The base level stays usable.
  4. **Materials in the silhouette:** give each material a different viewport color (stone gray for porcelain, dark leather, rusted metal), so you can check readability early.
  5. Leave out the cloak here; it comes from Marvelous Designer (step 5).
- **Done when:** the high-poly model matches the canon sheet and reads correctly as a black silhouette. Toggle a black matcap or use Krita's value check on a render.
- **Common mistakes:**
  - Sculpting detail smaller than the texture can show. Check what's visible at your texel density.
  - Sculpting everything in one mesh, so you can't bake parts separately.
- **Claude can help:** Claude can set up modifiers, render silhouette checks, and organize objects. The sculpting and design are your work.
- **Time:** days to weeks per hero character; much less for enemies built on the shared base.

### Step 5. Wraith's tattered cloak in Marvelous Designer

**Marvelous Designer (MD)** designs clothing like a tailor: you draw flat 2D pattern pieces, sew them together, and simulate them falling onto a 3D body. The result looks like real fabric.

- **Goal:** a cloak mesh with believable folds and tattered edges, exported for retopology and for Unreal's cloth.
- **Do this:**
  1. **Export the avatar** from Blender: Wraith's body (or a simplified version) in the A-pose, as FBX or OBJ, at real scale. In MD's import dialog, choose the unit that matches (for example centimeters) and check that the avatar is about 1.85 m tall in MD. `VERIFY:` MD 2026's import dialog wording.
  2. **Draw the pattern:**
     - a back panel, two front panels, and optionally a hood, shaped from the canon sheet;
     - arrange them around the avatar;
     - sew the shoulder and side seams;
     - simulate. The default fabric is a starting point; try a heavy wool preset.
  3. **Tatter it:**
     - Cut ragged shapes into the hem and edges in the 2D pattern, so the silhouette is torn.
     - Leave the fine tatters and holes to an **opacity mask texture** in Unreal (step 11); they cost nothing in geometry.
  4. **Particle distance:** keep the default (about 20 mm) while designing, because on your AMD card MD simulates on the CPU. Lower it for the final drape only.
  5. **Export for games:**
     - Use MD's quad remeshing ("Quad (Optimized)" mesh type) to get clean quads.
     - Export one of these:
       - **FBX or OBJ**: a single, thin mesh with UVs from the pattern pieces, which are ideal for fabric textures;
       - **USD with simulation data**: MD's "USD to Unreal Engine Chaos Cloth" workflow, which exports a render mesh plus a simulation mesh for Unreal's panel cloth. MD's help pairs MD 2025.2+ with UE 5.6+.

     UE 5.8's release notes add "round-tripping with Marvelous Designer" for Chaos Cloth. `VERIFY:` how that works (plugin or USD, which MD version) before depending on it. There's also a separate CLO/MD LiveSync plugin on Fab.
  6. Save the MD project to `source-art/marvelous/wraith-cloak/` (`.zprj`, which Git stores through LFS) and the exports next to it.
- **Done when:** a cloak mesh with good folds and a torn silhouette is exported, and it fits the Blender body when imported back.
- **Common mistakes:**
  - Wrong avatar scale, so the fabric behaves like silk or like cardboard.
  - Dense meshes straight from MD into the game. Always remesh or retopologize.
  - Modeling every tatter as geometry instead of an opacity mask.
- **Claude can help:** Claude can prepare and export the avatar through the Blender MCP, and bring the MD export back in and align it. MD itself is manual.
- **Time:** 1–3 sessions.

### Step 6. Retopology for games

**Retopology** means building a new, clean, low-polygon mesh on top of the detailed one. Its edge flow bends well when animated, and it fits the budget.

- **Goal:** `_low` meshes for body, armor, and cloak that stay within budget and deform well.
- **Do this:**
  1. **Body:**
     - start from the base mesh's topology, which is already clean;
     - reduce where it's hidden under armor or the cloak;
     - keep at least three edge loops around elbows, knees, shoulders, and hips.
  2. **Armor and masks:** simple, separate low meshes over the high ones. Rigid parts don't need deformation loops, only enough shape.
  3. **Tools:**
     - Blender's built-in **snapping to faces** (Face Project / Face Nearest) with the **Poly Build** tool lets you draw quads directly onto the high mesh.
     - A **Shrinkwrap** modifier keeps the low mesh on the surface.
     - **QuadriFlow** or voxel remeshing give quick automatic starts for rigid parts.
     - RetopoFlow 4 (paid) is faster for big jobs.
     - Quad Remesher's cheap license isn't for commercial use.
  4. **The cloak needs two versions if you use panel cloth** (step 12):
     - a **render mesh**, the one players see, with enough loops for the folds;
     - a coarser, evenly spaced **simulation mesh**, which the physics solver moves.

     With the simpler clothing tool, the cloak's own vertices simulate, so keep it moderate. A few hundred to about 1,500 vertices is a common range for a hero cloak. `VERIFY:` against your own profiling in walkthrough 17.
  5. Check the triangle count with **Overlays > Statistics** against the budget.
- **Done when:** the low meshes cover the high ones, fit the budget, and the body has deformation loops at every joint.
- **Common mistakes:**
  - Even density everywhere. Spend polygons on the silhouette and the joints, not on flat backs.
  - Long, thin triangles in the cloak, which make cloth jitter.
- **Claude can help:** Claude can report counts per object, find n-gons and poles, apply modifiers, and run automatic remeshing on rigid parts through the Blender MCP.
- **Time:** 1–3 sessions per character.

### Step 7. UVs

**UVs** are the 2D layout that tells the game where each part of the texture goes on the 3D mesh.

- **Goal:** clean UVs with even texel density (texture pixels per centimeter) and little wasted space.
- **Do this:**
  1. **Mark seams** where they're hidden: under arms, inside legs, along armor edges, the back of the head. Unwrap.
  2. **Even density:** use **UV > Average Islands Scale** so all pieces use the same pixels per centimeter. Check with a checker texture: the squares should look about the same size everywhere. Give the face or mask, and anything the camera sees up close, slightly more space on purpose.
  3. **Mirror** symmetrical parts onto the same UV space to save space, except anything with text, emblems, or asymmetric damage.
  4. **Pack** with **UV > Pack Islands** (Blender 5.2 has exact-shape packing, rotation, and margins). Leave a margin of a few pixels at 2K or 4K so mipmaps don't bleed.
  5. **One UV set per material slot**, each filling 0 to 1. Unreal can use UDIMs (multi-tile UVs), but a normal 0–1 layout is simpler for games.
- **Done when:** the checker looks even, islands don't overlap (except intentional mirrors), and space usage is high.
- **Common mistakes:**
  - Seams across the most visible areas (face, chest, the cloak's outer surface).
  - Mirroring UVs on parts with text or emblems, which then appear backwards on one side.
  - Margins too small, so colors bleed across seams at a distance.
- **Claude can help:** through the Blender MCP, Claude can average island scales, pack, and report overlapping or flipped islands.
- **Time:** 1–2 sessions per character.

### Step 8. Bake high to low

**Baking** transfers detail from the high-poly sculpt into textures (normal maps, ambient occlusion, curvature) for the low-poly mesh, so it looks detailed at low cost.

- **Goal:** clean mesh maps for texturing.
- **Do this:**
  1. **In Substance 3D Painter** (recommended if you use it for texturing):
     - When creating the project, set the normal map format to **DirectX**, which is what Unreal uses.
     - In the baker, set matching to **by mesh name**, so `Mask_low` only receives detail from `Mask_high`. That avoids detail projecting from one part onto another.
     - Bake normal, world-space normal, ambient occlusion, curvature, position, thickness, and ID maps.
  2. **In Blender** (for ArmorPaint or a Blender-only pipeline): bake with Cycles on the GPU (**HIP**; Blender 5.2 includes RDNA 4). Use a cage or an extrusion distance. Blender bakes **OpenGL-style normals** (green up), so tick **Flip Green Channel** on the texture in Unreal.
  3. **Inspect** the normal map for waviness, skewed details, and edges that projected from the wrong part. Adjust cages and distances, and rebake.
- **Done when:** the baked normal map on the low mesh looks like the sculpt, with no bleeding between parts.
- **Common mistakes:**
  - Mixed normal-map conventions, so details look inverted, like dents instead of bumps.
  - One bake for all parts together without name matching, so buckles project onto the chest.
- **Claude can help:** Claude can set up Blender bakes through the Blender MCP (cage, margins, output paths) and check the normal map's convention.
- **Time:** 1 session per character.

### Step 9. Texture the character

- **Goal:** PBR textures (base color, normal, roughness, metallic, ambient occlusion, and emissive where needed) that follow the palette rules and read at night.
- **Do this:**
  1. **Choose your tool** (see Tools):
     - Substance 3D Painter is the industry standard, with smart materials and ready Unreal export presets.
     - ArmorPaint 1.0 is a cheap alternative.
     - Blender with Ucupaint is free.
  2. **Set up the project in Painter:** 4K document resolution for hero characters and 2K for enemies, DirectX normals, and the baked maps from step 8.
  3. **Texture to the palette** (walkthrough 03, style guide):
     - Keep base colors dark and desaturated, because the 70% base applies to characters too.
     - **Wraith is dead**, so violet emissive accents (runes, cracks, power effects) are allowed, and warm light never is.
     - **The Choir's porcelain** is `#D8CCB8`, the brightest non-light value on them.
     - Living characters carry no violet.
  4. **Tattered edges** are an opacity mask painted on the cloak, used as a masked material in Unreal (step 11).
  5. **Check in context:** preview under a warm point light in a dark environment, not under Painter's default bright studio environment. Load a dark HDRI or turn the environment down. That's how players will see it.
  6. **Export** with Painter's Unreal preset, which is packed: base color, normal, and **occlusion/roughness/metallic** in one texture's R/G/B channels. `VERIFY:` the preset's exact name in Painter 2026.
     - Name the files `T_<Name>_<Part>_BC`, `_N`, `_ORM`, and `_E` for emissive.
     - Put them in `source-art/substance/<name>/export/`.
- **Done when:** the textures match the canon sheet, follow the palette rules, and read in dark, warm-lit previews.
- **Common mistakes:**
  - Texturing under bright default lighting, then everything turns to mud in the game's night.
  - Violet on living characters.
  - Baking lighting into base color (painted-in shadows), which fights Lumen.
- **Claude can help:** Claude can check exported textures (resolution, channel packing, naming) and preview them in Blender through the MCP. The painting is yours.
- **Time:** 1–3 sessions per character.

### Step 10. Export to Unreal

These settings are the source for every Blender-to-Unreal export in this project, including walkthrough 06's kit and walkthrough 05's skeletal meshes. They match the defaults of **Send to Unreal**, Epic's own Blender add-on, which is a known-good combination.

- **Goal:** meshes arrive in Unreal at the right scale and orientation, with correct normals, and (after rigging) without an extra root bone.
- **Do this:**
  1. **Blender FBX export** (**File > Export > FBX (.fbx)**):

     | Setting | Value | Why |
     |---|---|---|
     | Limit to | Selected Objects (the `Export` collection) | Nothing extra gets in |
     | Scale | 1.00 | Scene units are already meters at scale 1.0 |
     | Apply Scalings | **All Local** | Matches Send to Unreal |
     | Apply Unit | On | Unreal gets correct units |
     | Forward / Up | **Y Forward / Z Up** | Matches Send to Unreal |
     | Apply Transform | **Off** | Blender marks it experimental and broken with armatures |
     | Smoothing | **Face** | Unreal gets smoothing groups |
     | Apply Modifiers | On | Mirrors and bevels are baked in |
     | Add Leaf Bones (skeletal) | **Off** | Otherwise extra `_end` bones appear in Unreal |
     | Only Deform Bones (skeletal) | Off, with only deform bones in the `Export` collection | The option still exports non-deforming parents of deforming bones, so control what's exported instead |

     Save it as an operator preset named `Wraith_UE`, so every export uses it.
  2. **The armature object must be named `Armature`** (walkthrough 05). Unreal's FBX importer treats that name as a special keyword and doesn't add it as an extra root bone. With any other name, your skeleton gets an unwanted bone above `root`, and animations from the Unreal mannequin won't match.
  3. **Now:** export the unrigged low mesh as a static mesh test. Check the scale against the mannequin and look at the materials. **After walkthrough 05:** export the rigged character as `SK_<Name>.fbx`.
  4. **Unreal import** (skeletal mesh, after rigging):
     - **Skeletal Mesh** on;
     - Skeleton: none (a new one) for the first character, or the shared skeleton for enemies (walkthrough 05);
     - **Create Physics Asset** on, for cloth collision later;
     - **Normal Import Method: Import Normals and Tangents**, and Compute Weighted Normals on;
     - **Convert Scene** off and **Convert Scene Unit** off, as Send to Unreal uses them;
     - Import Uniform Scale 1.0;
     - Materials: create them, then replace them with your instances (step 11).
  5. **Importer caveat:** Unreal's newer **Interchange** importer handles FBX in recent versions. Some users reported it discarding imported normals by default in 5.5, and the community Send to Unreal fork requires the legacy FBX importer for 5.5 and later (console variable `Interchange.FeatureFlags.Import.FBX False`). If normals look wrong or options are missing in 5.8, try the legacy importer the same way. `VERIFY:` in 5.8.
- **Done when:** the test mesh arrives about as tall as the design (compare it to the 180 cm mannequin), faces the expected direction, with smooth shading where intended. After rigging, the skeleton's top bone is `root`, with no extra bone above it.
- **Common mistakes:**
  - An armature named `Wraith_Rig`, so the skeleton has an extra root.
  - Add Leaf Bones left on.
  - Apply Transform turned on, which breaks armatures.
  - Scale 100× off: check Scale 1.0, All Local, and Apply Unit.
- **Claude can help:** fully for the Blender side. Claude can export with exactly these settings through the Blender MCP and check the resulting bone list. Through the Unreal MCP it can inspect the imported skeleton's hierarchy.
- **Time:** 30 minutes the first time.

### Step 11. Character materials in Unreal (Substrate)

- **Goal:** one master character material with instances per character and part.
- **Do this:**
  1. **Import textures** into `/Game/Wraith/Characters/<Name>/Textures/`:
     - `_BC`: sRGB on.
     - `_ORM`: **sRGB off**, compression **Masks (no sRGB)**.
     - `_N`: compression **Normalmap**. Tick **Flip Green Channel** only if the map was baked OpenGL-style (Blender); Painter's DirectX export needs no flip.
     - `_E` (emissive): sRGB on.
  2. **Master material** `M_Character_Master` (Substrate), built on one Substrate **Slab**:
     - Base color from `_BC` times a tint parameter.
     - Roughness and metallic from `_ORM`'s G and B channels; ambient occlusion from R.
     - Normal from `_N`.
     - Emissive from `_E` times an `EmissiveColor` and an `EmissiveStrength` parameter. Default the color to Spirit violet `#9B6BFF` for the dead; keep the strength 0 on living characters.
     - A **masked** variant (static switch `UseOpacityMask`) for the cloak's tatters.
     - A **two-sided** variant for the cloak, so its back faces render.
  3. **Instances:** `MI_Wraith_Body`, `MI_Wraith_Cloak` (masked, two-sided), `MI_Wraith_Mask`, and so on.
  4. **Skin** (for unmasked faces such as Vesper's, if hers is visible): Substrate slabs have subsurface-scattering controls. Use them lightly. `VERIFY:` the 5.8 Substrate subsurface parameters. MetaHuman faces come with their own materials.
- **Done when:** each character renders correctly in `L_LookDev_Night` (walkthrough 07). Tatters are see-through, the cloak's inside isn't missing, and emissive appears only where the palette allows.
- **Common mistakes:**
  - `_ORM` imported as sRGB, so roughness looks washed out.
  - Double-flipped normals.
  - A separate master material per character (maintenance hell).
- **Claude can help:** through the Unreal MCP, Claude can create material instances, assign textures by naming convention, and set parameters. You or Claude build the master material graph from a node list; `VERIFY:` how far Epic's toolsets can edit material graphs.
- **Time:** 1–2 sessions for the master, minutes per instance.

### Step 12. The cloak with Chaos Cloth

**Chaos Cloth** is Unreal's cloth simulation. In 5.8 the **Dataflow-based Cloth Panel Editor** is production-ready and the default cloth editor. You build a **Cloth Asset** (simulation mesh, render mesh, weight maps, and settings) and attach it to the character with a **Chaos Cloth component**. The older **Clothing Tool**, where you paint cloth directly on a skeletal mesh section, is still documented in 5.8.

- **Goal:** Wraith's cloak moves naturally while running, dodging, launching, and slamming, without clipping or exploding, at a small cost.
- **Do this:**
  1. **Pick your path:**
     - **Quick start (older Clothing Tool):**
       - In the Skeletal Mesh editor, turn the cloak's material section into clothing data.
       - Paint **Max Distance**: 0 at the neck and shoulders (pinned), rising toward the hem.
       - Add a **Backstop**, which stops painted points moving into the body.
       - Apply it to the section.

       You can get a moving cloak in an afternoon.
     - **Production path (5.8 Cloth Panel Editor):**
       - Create a Cloth Asset.
       - In its Dataflow graph, import the simulation and render meshes (the USD from Marvelous Designer contains both, through a USD import node), and transfer skin weights from Wraith's skeletal mesh.
       - Add weight maps and set the **Physics Asset** for collision.
       - Add a **Chaos Cloth component** to the character using the asset.

       It's more setup, but gives better quality and is the future-proof workflow. Follow Epic's "Chaos Cloth Updates 5.8" tutorial and the Panel Cloth Editor overview (References) for the exact node names. `VERIFY:` them in your editor.

     Start with the quick path to learn how cloth behaves, then move to the panel editor for the final cloak.
  2. **Collision:** cloth collides with the capsules and spheres of the character's **Physics Asset**, created on import (step 10). Make sure legs, hips, and the torso have capsules that roughly fill the body, or the cloak passes through the legs when running.
  3. **Tune for combat:**
     - Wraith turns and dashes fast. Look for the cloth settings that scale how much of the character's linear and angular velocity reaches the cloth, and lower them, so the cloak doesn't stretch like rubber on a dash.
     - Increase stiffness near the shoulders.
     - Test with the most violent animations from walkthrough 05 (launcher, slam, dodge) in a loop.

     `VERIFY:` the exact setting names in 5.8.
  4. **Wind:** a **Wind Directional Source** actor in the level moves cloth. A gentle, gusting wind sells the blizzard, even when Wraith stands still.
  5. **Budget:**
     - Only Wraith and Sister Vesper get simulated cloth.
     - Enemies get cheaper secondary motion: the **AnimDynamics** or **RigidBody** animation nodes on a few extra bones (walkthrough 05), or nothing.
     - Turn cloth off on lower LODs.
- **Done when:** in a test map, looping the launcher, slam, and dodge animations, the cloak stays behind and around Wraith, never passes through the legs, and doesn't stretch unnaturally. Profile the cloth's cost later in walkthrough 17 (Chaos Cloth simulates on the CPU).
- **Common mistakes:**
  - Pinning too little, so the cloak slides off the shoulders.
  - A too-dense simulation mesh.
  - No leg capsules in the Physics Asset.
  - Judging the cloth only on idle and walk animations.
- **Claude can help:** Claude can set up the Physics Asset capsules' sizes through the Unreal MCP, write a test harness that loops combat animations, and explain the cloth settings. Painting weights and judging motion are manual and visual.
- **Time:** 1–2 sessions for the quick path; 2–4 for the panel editor.

### Step 13. Check the character in the engine

- **Goal:** confirm the character is right before moving on.
- **Do this:**
  1. **Scale:** stand the character next to the Unreal mannequin (about 180 cm).
  2. **Silhouette:** place it in `L_LookDev_Night` against lit fog. Take a screenshot and use Krita's value check (walkthrough 03). Does it read as that character in 1 second?
  3. **Budget:** the Skeletal Mesh editor shows triangles, vertices, and sections per LOD. Compare them with step 1.
  4. **Palette:** run `tools/art/palette_ratio.py` on a close-up. Violet only on the dead; no warm glow on the dead.
  5. **Animation test:** after walkthrough 05, loop a few combat animations and look for broken skinning at the shoulders, knees, and neck.
- **Done when:** all five checks pass, and `docs/design/characters.md` has the final numbers.
- **Common mistakes:**
  - Checking only in a bright test scene; the game is played at night.
  - Skipping the animation test until late, then finding skinning problems after texturing is done.
- **Claude can help:** Claude can read the mesh statistics through the Unreal MCP, run the palette check, and compare the results with the budget table.
- **Time:** 30 minutes.

### Step 14. Enemies, efficiently

- **Goal:** four readable archetypes for the effort of about one and a half characters.
- **Do this:**
  1. **One shared base body** (steps 3–10 done once), with one skeleton (walkthrough 05).
  2. **Modular parts:** robes, porcelain masks, shields, snuffer tools, and armor for the heavy, as separate skeletal meshes on the same skeleton. In the enemy Blueprint, the body is the main mesh; each part is another Skeletal Mesh component that follows it with **Set Leader Pose Component** (called "Master Pose" in older tutorials).
  3. **Shared texture sets** for parts that repeat, with material instances for color and wear variations.
  4. **Silhouette first:** the parts that make each archetype unique (walkthrough 03's 64-pixel test) get the modeling time. Everything else is shared.
  5. **Buy where it fits:** a Fab armor or robe pack in the right style can save days. Log it (walkthrough 06, step 7).
- **Done when:** all four archetypes exist on the shared base, pass the silhouette and budget checks, and share one skeleton.
- **Common mistakes:**
  - Each enemy a unique full character, which quadruples the work.
  - Parts on different skeletons, so they can't follow the body.
- **Claude can help:** Claude can build the enemy Blueprints' component setup in C++ or through the MCP, create material instance variations, and track which parts each archetype uses.
- **Time:** about as long as one hero character, for all four.

---

## Vertical slice checklist

- [ ] `docs/design/characters.md` with plan and budget for Wraith, Vesper, and the four archetypes
- [ ] Shared enemy base body retopologized, UV'd, and exported
- [ ] Shielded cultist, Choir singer, snuffer, and heavy built from the base plus modular parts, each passing the 64-pixel silhouette test
- [ ] Wraith: high-poly, low-poly, UVs, bakes, and textures (violet emissive only), exported with the `Wraith_UE` preset
- [ ] Wraith's cloak designed in Marvelous Designer (project in `source-art/marvelous/wraith-cloak/`), remeshed, render mesh plus simulation mesh
- [ ] Sister Vesper at hero quality
- [ ] `M_Character_Master` (Substrate) with masked and two-sided variants; instances for every slice character
- [ ] Skeletal meshes imported with the settings in step 10; no extra root bone
- [ ] Wraith's cloak simulated with Chaos Cloth (quick path first, then the panel editor), tested on launcher, slam, and dodge loops
- [ ] Vesper's cloth (if she has any) set up the same way; enemies use cheaper secondary motion
- [ ] All characters checked in `L_LookDev_Night` for scale, silhouette, budget, and palette

## Going further

- **MetaHuman** for unmasked story characters in cutscenes (walkthrough 12). Since 5.6 the MetaHuman Creator runs inside the editor, and 5.8 adds an experimental MetaHuman Crowd plugin.
- **Nanite skinned meshes**, when Epic marks them production-ready. They could remove LOD work for characters.
- **Skin Weight Profiles**, alternative skin weights that can be swapped in (for example tighter weights on LOD0).
- **ML Deformer** for better shoulder and elbow deformation on the hero.
- **Character Creator 5** (Reallusion) as a paid alternative source of base characters; royalty-free for games. `VERIFY:` the price.

## References

**Epic Games**
- Chaos Cloth updates 5.8 (tutorial): https://dev.epicgames.com/community/learning/tutorials/Wb2V/unreal-engine-chaos-cloth-updates-5-8
- Panel Cloth Editor overview: https://dev.epicgames.com/documentation/en-us/unreal-engine/panel-cloth-editor-overview
- Dataflow graph: https://dev.epicgames.com/documentation/en-us/unreal-engine/dataflow-graph
- Building an Outfit asset (USD from MD or CLO): https://dev.epicgames.com/documentation/en-us/unreal-engine/building-an-outfit-asset-in-unreal-engine
- Clothing Tool (older workflow): https://dev.epicgames.com/documentation/en-us/unreal-engine/clothing-tool-in-unreal-engine
- Clothing Tool properties: https://dev.epicgames.com/documentation/en-us/unreal-engine/clothing-tool-in-unreal-engine---properties-reference
- Chaos Cloth demystified (tutorial): https://dev.epicgames.com/community/learning/tutorials/MZeq/unreal-engine-fortnite-chaos-cloth-demystified-a-zero-to-hero-guide-to-chaos-cloth
- FBX import options: https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-import-options-reference-in-unreal-engine
- Interchange FBX options (knowledge base): https://dev.epicgames.com/community/learning/knowledge-base/KPql/unreal-engine-interchange-fbx-options
- Skeletal mesh rendering paths (bone influences): https://dev.epicgames.com/documentation/en-us/unreal-engine/skeletal-mesh-rendering-paths-in-unreal-engine
- Skin Weight Profiles: https://dev.epicgames.com/documentation/en-us/unreal-engine/skin-weight-profiles-in-unreal-engine
- Nanite: https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine
- MetaHuman license: https://www.metahuman.com/license

**Blender and add-ons**
- Human Base Meshes: https://developer.blender.org/docs/features/asset_system/asset_bundles/human_base_meshes/
- MPFB2: https://github.com/makehumancommunity/mpfb2
- Ucupaint: https://github.com/ucupumar/ucupaint
- RetopoFlow: https://github.com/CGCookie/retopoflow
- Send to Unreal (Epic): https://github.com/EpicGamesExt/BlenderTools
- Send to Unreal (community fork, Blender 5.x): https://github.com/poly-hammer/BlenderTools

**Other tools**
- Marvelous Designer system requirements: https://support.marvelousdesigner.com/hc/en-us/articles/47358219834649-System-Requirements-April-2026
- Marvelous Designer USD to Chaos Cloth workflow: https://support.marvelousdesigner.com/hc/en-us/articles/47358311524249-9-USD-to-Unreal-Engine-Chaos-Cloth-Workflow
- Marvelous Designer licenses: https://support.marvelousdesigner.com/hc/en-us/articles/47358297616153-What-is-the-difference-between-Personal-and-Enterprise-License
- Substance 3D Painter system requirements: https://helpx.adobe.com/substance-3d-painter/getting-started/system-requirements.html
- ArmorPaint: https://github.com/armory3d/armorpaint
- Quad Remesher licenses: https://exoside.com/quadremesher/quadremesher-buy/

**Recommended learning channels**
- Unreal Engine on YouTube (official; Chaos Cloth and MetaHuman talks): https://www.youtube.com/@UnrealEngine
- Blender Studio (Blender's own training courses and production files): https://studio.blender.org
