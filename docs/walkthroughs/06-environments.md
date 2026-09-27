# 06. Environments

> **Written for:** Unreal Engine 5.8 (5.8.3) with Substrate materials (the default for new 5.8 projects), Modeling Mode's CubeGrid tool, Nanite, PCG (production-ready since 5.7), and Niagara; Blender 5.2 LTS; Fab.
> **Facts checked:** 2026-09-27. Epic's and Fab's sites were blocked from this environment, so Epic facts here come from search excerpts of official pages. Anything unconfirmed, or likely to differ in your editor, is marked `VERIFY:`.

## What this covers

This walkthrough builds Wraith's levels from the first gray box to a finished snowy district, using the Lantern Market as the example. You block out with player metrics, build a modular gothic kit in Blender on a fixed grid, and decide what to buy on Fab (including Megascans). Then you make Substrate materials for stone, snow, frost, and ice; place icicles with PCG; add Niagara snowfall; add footprints and deformable snow only where they matter; build a distant city with PCG; and set up fog and atmosphere. Lighting itself is walkthrough 07; the full snowfall effect is walkthrough 14.

## Why it matters for Wraith

- **A brawler is played in arenas.** Every fight space must fit a crowd of enemies, room to dodge, and a third-person camera that doesn't clip into walls. Get the sizes right in gray boxes; art can't fix a cramped arena.
- **Lanterns are level design.** Where lanterns stand, and where it's dark, decides where the dead rise and enemies grow stronger (walkthrough 10). They're placed in the blockout, not added as decoration later.
- **A vertical city in eternal winter.** Towers, fog between them, and snow on everything. Snow has to come from one material system that works on every mesh. Painting snow into each texture by hand would never stay consistent, and a solo developer can't afford it.
- **The palette's 70% base is mostly environment.** Stone, darkness, and snow in shadow make up the "70% darkness and stone" in the README. Environment textures stay dark and desaturated so that lantern gold and spirit violet mean something.
- **Solo and part-time.** A modular kit, carefully chosen Fab purchases, and PCG give you a whole district without modeling every building by hand.

## Tools

| Tool | What it's for | Cost | Commercial license OK? | AMD notes |
|---|---|---|---|---|
| Unreal Engine 5.8: Modeling Mode, Nanite, PCG, Niagara, Substrate | Blockout, placement, procedural layout, particles, materials | Free (engine royalty terms in walkthrough 01) | Yes | All work on the RX 9060 XT. Niagara GPU raytracing collisions (Experimental) need hardware ray tracing, which RDNA 4 has; the walkthrough uses depth-buffer collision instead. |
| Blender 5.2 LTS | The modular kit, icicles, distant-city silhouettes | Free (GPL) | Yes | None for modeling |
| Fab | Marketplace for props, materials, and Megascans | Free and paid listings | Yes. Under the Fab Standard License you can ship assets inside a game; you can't redistribute them on their own. Personal tier if you earned US$100,000 or less in the last 12 months, Professional above that. | None |
| Megascans (sold on Fab) | Scanned surfaces, rocks, and ruins | The free "claim everything" period ended on 31 Dec 2024. A free starter pack of 1,500+ assets remains; everything else is bought per asset or pack. `VERIFY:` current prices. | Yes, under the Fab Standard License | None |
| Krita (from walkthrough 03) | Painting the trim sheet and snow masks | Free | Yes | None |

## Before you start

- **Walkthroughs done:** 01 (project, Blender, MCPs). **Read first:** 03 for the Lantern Market key frames and the kit elevation sheet.
- **Milestone:** blockout work belongs to Milestone 2, as the gray-box arena, and to Milestone 3, as the Lantern Market. Art passes (steps 4–12) are Milestone 3.
- **You need a character that moves:** the template character is enough for blockout; the gray-box combat from walkthrough 08 is better.
- **Design doc first** (README rule): you'll write `docs/design/environment-metrics.md` in step 1. Every later step refers to it.

---

## Steps

### Step 1. Measure your character and write the metrics document

**Metrics** are the fixed sizes that a level must respect, such as step height, jump height, and door width. They come from your character's collision capsule and movement settings. Level designers work from a metrics sheet so every space is playable before it's pretty.

- **Goal:** `docs/design/environment-metrics.md` holds the real numbers from your project, and every blockout follows them.
- **Do this:**
  1. Ask Claude to read `WraithGame/Source/WraithGame/WraithGameCharacter.cpp` and list the capsule size, `MaxWalkSpeed`, `JumpZVelocity`, `AirControl`, and camera boom length. Projects made from the 5.8 C++ Third Person template show:
     - capsule radius 42 and half-height 96, so about 192 cm tall;
     - `MaxWalkSpeed` 500;
     - `JumpZVelocity` 500;
     - `AirControl` 0.35;
     - camera boom 400 cm.

     Older UE5 templates used a jump velocity of 700, so use your file's numbers, not a tutorial's. `VERIFY:` these came from GitHub projects generated from the template, not from Epic's docs.
  2. Add the engine defaults the template doesn't override. Unless your character changes them, the Character Movement component uses a **Max Step Height** of 45 cm and a **Walkable Floor Angle** of about 44.8°, and gravity is −980 cm/s² (World Settings). Check them in the character Blueprint's **Character Movement** details.
  3. Work out jump height: **apex = JumpZVelocity² ÷ (2 × 980)**. With 500 that's 250,000 ÷ 1,960 ≈ **128 cm**; with 700 it would be 250 cm.
  4. Write the metrics document. Use this table as a **starting point**; these are guidelines to playtest, not rules:

     | Element | Starting size | Reasoning |
     |---|---|---|
     | Character | ~192 cm tall (capsule) | From the template |
     | Grid for architecture | 100 cm; modules in 100 cm steps | Unreal works in centimeters, and round numbers keep snapping predictable |
     | Grid for props | 50 cm, with 10 cm for fine placement | Props need finer placement |
     | Doorway you walk through | 200 cm wide, 300 cm tall | Epic's rule of thumb for third-person spaces is about 1.5× real scale. A real 80 cm door feels cramped and the camera clips. |
     | Street where fights can happen | at least 600 cm wide | Room to dodge sideways and for the 400 cm camera boom |
     | Small arena (3–4 enemies) | about 15 × 15 m | Enemies circle while others attack (walkthrough 11) |
     | Main arena (6–8 enemies, or the boss) | about 25–35 m across | Launchers and knockbacks need space |
     | Stairs | 20 cm rise, 30 cm run | Well under the 45 cm step height, so the character walks up smoothly |
     | Waist-high wall or rail | 100 cm | Reads clearly as "can't pass, can see over" |
     | Wall the player must not jump onto | 200 cm or more | Higher than jump apex plus step height (128 + 45 = 173 cm) |
     | Slope the player can walk up | 40° or less | Stays under the walkable angle |

  5. Add the kit rules from step 3, and the blockout color code from step 2, to the same document.
- **Done when:** the metrics document exists with your project's real numbers, and Claude has read it. Point future Claude sessions to it for any level work.
- **Common mistakes:**
  - Copying metrics from a tutorial made on another engine version.
  - Forgetting the camera. Third-person spaces need extra width and height for the camera boom, not just for the capsule.
  - Designing real-world-scale spaces. They feel tiny in third person.
- **Claude can help:** Fully. Claude reads the C++ and Blueprint defaults, computes the derived numbers, and drafts the document for you to review.
- **Time:** 1 hour.

### Step 2. Block out the Lantern Market with CubeGrid

A **blockout** (or gray box) is a level built from plain shapes, used to test layout, fights, and sightlines before any art exists.

- **Goal:** a playable gray-box Lantern Market, fought through with gray-box combat, with lantern positions and dark zones marked.
- **Do this:**
  1. **Create the map.** Choose **File > New Level > Basic** and save it as `/Game/Wraith/Maps/LanternMarket/L_LanternMarket_Blockout`. The README has no prefix for levels; `L_` is a suggested addition. Keep a "Basic" level, without World Partition, for now (see step 13).
  2. **Write a beat chart before building.** Walk through the district's story beats from the story bible and turn each into a space. The table below is an **example format**, not your story; replace every row:

     | Beat | Space | Fight or event | Lanterns | New element introduced |
     |---|---|---|---|---|
     | 1 | Entry street | 2 cultists, teaches basics | Lit | — |
     | 2 | Market square (small arena) | Mixed group | Lit, then one is snuffed | Snuffer |
     | 3 | Side alley | Short fight in the dark | Dark | Enemies empowered in darkness |
     | 4 | Stairs to the cathedral terrace | Choir singers support enemies | Relight to win | Relighting |
     | 5 | Vesper arena (main arena) | Boss | Scripted by the fight | Sister Vesper |

  3. **Open Modeling Mode** from the mode selector in the level editor toolbar. Use **Create > CubeGrid**.
     - CubeGrid builds blockout meshes on a grid: you push and pull faces to extrude them.
     - Set the block size to **100 cm** to match the metrics document.
     - Move the grid with its gizmo (**R**) or **Ctrl + middle-click**.

     `VERIFY:` the exact push/pull keys and setting names in 5.8's CubeGrid panel.
  4. **Use a strict color code.** Put these as material instances on blockout meshes:

     | Color | Meaning |
     |---|---|
     | Gray (Unreal's default grid material) | Walkable, solid |
     | Dark red | Blocking: the player can't go here |
     | Lantern gold | A lantern position (walkthrough 10) |
     | Spirit violet | A dark zone, where enemies are empowered |
     | Blue | Enemy spawn points and encounter triggers |

     The code follows the art rules (gold means the living's light, violet means the dead), so the blockout already reads like the finished game.
  5. **Place landmarks early.** The README's stopped cathedral clock is the natural landmark. Put a tall placeholder tower where the player can see it from most streets; it doubles as navigation.
  6. **Mark camera trouble spots.** Walk every path with the template character. Wherever the camera clips or swings wildly, widen the space, raise the ceiling, or add a camera-blocking volume later.
  7. **Fight in it.** Once walkthrough 08's gray-box combat exists, run the whole level with gray-box enemies. Adjust the spaces, not the combat, until fights feel good.
- **Done when:** you can play from the entry to the Vesper arena. Every arena has passed a fight test, every lantern and dark zone is marked, and the beat chart matches the layout.
- **Common mistakes:**
  - Detailing the blockout. Stay with boxes: the point is cheap iteration.
  - Building arenas without enemies in them. Two enemies in a 15 m square feels completely different from six.
  - Hiding the landmark. If players can't orient themselves, they get lost in a dark, snowy city.
- **Claude can help:** Through the Unreal MCP, Claude can spawn blockout shapes to exact sizes, lay out repeated elements such as market stalls on a grid, place lantern markers from a list, and report distances between points. You judge the feel by playing.
- **Time:** 1–3 sessions for a first pass; more after playtests.

### Step 3. Design the modular gothic kit

A **modular kit** is a set of meshes (walls, arches, floors, stairs, trims) built to one grid so they snap together into many buildings.

- **Goal:** a written kit specification, so every piece you model or buy fits together.
- **Do this:** add a "Kit" section to `docs/design/environment-metrics.md` with these rules. Adjust the numbers to your kit elevation sheet from walkthrough 03.
  - **Module sizes (cm):**
    - walls 100, 200, and 400 wide; 400 per storey high; 50 thick;
    - arches 400 wide and 600 high;
    - floor tiles 400 × 400;
    - stairs 400 long and 200 high.
  - **Pivot (origin):**
    - walls and floors: bottom-left-front corner;
    - props and lanterns: bottom center;
    - stairs: bottom of the first step, left side.

    With every pivot on the same corner, snapping at 100 cm always lines pieces up.
  - **Facing:** the "front" of every wall faces Blender's −Y, which is what you see in Blender's Front view (Numpad 1).
  - **Naming:** `SM_Kit_<Category>_<Width>x<Height>_<Variant>`, for example `SM_Kit_Wall_400x400_A`, `SM_Kit_Arch_400x600_A`, and `SM_Kit_Stair_400x200_A`. Collision objects are named `UCX_<MeshName>_00` (step 4).
  - **Materials:** at most two slots per piece: a tiling stone material, and one shared **trim sheet** for moldings and edges. Snow is never baked into kit textures; it comes from the material system in step 6.
  - **Starter kit list:** about 20 pieces:
    - walls: plain, window, and door;
    - arch;
    - pillar;
    - buttress;
    - corner;
    - roof: slope, ridge, and edge;
    - floor tile;
    - stair;
    - balcony;
    - cornice trim.

    Add pieces only when a real building needs one.
- **Done when:** the kit section exists and matches the elevation sheet.
- **Common mistakes:**
  - Mixing grids, such as 128 cm walls with 100 cm floors. Pick one and never break it.
  - Pivots in the center of walls, which makes snapping a fight.
  - Too many unique pieces. A good kit is small and reused with variety from materials and props.
- **Claude can help:** Claude can derive the kit list from your beat chart and elevation sheet, and check that the dimensions are consistent.
- **Time:** 1 hour.

### Step 4. Model the kit in Blender

- **Goal:** the starter kit exists as clean, correctly scaled, correctly pivoted meshes, exported one FBX per piece.
- **Do this:**
  1. **Scene units.** Open **Scene Properties > Units** and set Unit System to **Metric** and Unit Scale to **1.0**. Keep modeling in meters; the FBX export converts to Unreal's centimeters, as the smoke test in walkthrough 01 proved.
  2. **Grid and snapping.** In the Viewport Overlays popover, set the grid **Scale** so one grid line is 0.5 m. In the snapping popover (the magnet icon), snap to **Increment** with absolute grid snapping, so vertices land on grid lines, not on offsets from where you started. `VERIFY:` the snapping option names in Blender 5.2, which have changed across 4.x versions.
  3. **One piece per object**, named per the kit rules, with the origin on the pivot corner. To set it, snap the 3D cursor to the corner vertex (**Shift+S > Cursor to Selected** in Edit Mode), then choose **Object > Set Origin > Origin to 3D Cursor**.
  4. **Edges and bevels.** Give outer edges a small bevel (1–2 cm). Nanite makes the extra triangles cheap, and bevels catch lantern light in a way sharp edges can't. Use a **Weighted Normal** modifier so large flat faces shade flat.
  5. **UVs.** Keep one texel density across the kit so textures tile at the same scale on every piece. One way: set one UV tile to cover 2 m (**UV > Cube Projection**, cube size 2 m), then move trim-sheet strips onto the right rows of the trim texture.
  6. **Collision.** For each piece, add simple convex boxes named `UCX_<MeshName>_00`, `_01`, and so on. Unreal's FBX import turns objects with this prefix into the mesh's collision. Keep collision simple, even when the visual mesh is detailed.
  7. **Export.** Use the static-mesh FBX settings from walkthrough 04, step 10. For the whole kit, ask Claude to run a batch export through the Blender MCP. It's roughly this script, run inside Blender:
     ```python
     import bpy, os

     out_dir = bpy.path.abspath("//exports/kit")  # next to the .blend file
     os.makedirs(out_dir, exist_ok=True)

     pieces = [o for o in bpy.context.selected_objects
               if o.type == 'MESH' and not o.name.startswith("UCX_")]
     for piece in pieces:
         bpy.ops.object.select_all(action='DESELECT')
         piece.select_set(True)
         for other in bpy.data.objects:          # include the piece's collision hulls
             if other.name.startswith(f"UCX_{piece.name}_"):
                 other.select_set(True)
         saved = piece.location.copy()
         piece.location = (0.0, 0.0, 0.0)        # export every piece at the origin
         bpy.ops.export_scene.fbx(              # same settings as walkthrough 04, step 10
             filepath=os.path.join(out_dir, f"{piece.name}.fbx"),
             use_selection=True,
             object_types={'MESH'},
             global_scale=1.0,
             apply_unit_scale=True,
             apply_scale_options='FBX_SCALE_NONE',   # shown as "All Local" in the export dialog
             axis_forward='Y',
             axis_up='Z',
             use_mesh_modifiers=True,
             mesh_smooth_type='FACE',
         )
         piece.location = saved
     ```
     The script moves each piece to the origin only for its own export. That works for collision hulls parented to their piece. Unparented hulls stay where they are, so parent them first, or ask Claude to move them along. `VERIFY:` run it on two pieces first and check the result in Unreal (step 5) before exporting the whole kit. On that first import, note which way a wall's front faces in Unreal, and keep that convention for every piece.
  8. Save the `.blend` in `source-art/blender/environments/lantern-market/` and the exports in `source-art/blender/environments/lantern-market/exports/kit/`, then commit.
- **Done when:**
  - every kit piece exists, named and pivoted per the rules, with collision;
  - the FBX files are exported;
  - a test import of two pieces snaps together at 100 cm in Unreal.
- **Common mistakes:**
  - Scaled objects. Apply scale (**Ctrl+A > Scale**) before export, or pieces arrive at odd sizes.
  - Flipped normals on some faces, which show up as black or missing faces in Unreal. Check with **Overlays > Face Orientation**.
  - Collision named after the wrong mesh, which Unreal then silently ignores.
- **Claude can help:** A lot. Through the Blender MCP, Claude can create exact-size block primitives for each piece, set origins, add `UCX_` boxes, check names and scales, and run the batch export. The shaping and look of each piece are your work.
- **Time:** 2–5 sessions for about 20 pieces.

### Step 5. Import the kit and build a kit test map

- **Goal:** the kit lives in Unreal as Nanite meshes, and you've proven it snaps together.
- **Do this:**
  1. Import the FBX files into `/Game/Wraith/Environments/Shared/Kit/`. In the import dialog:
     - keep collision import on, so the `UCX_` objects become collision;
     - turn on **Build Nanite**;
     - leave materials for step 6.

     `VERIFY:` whether 5.8's import dialog (Unreal's newer Interchange importer) turns Nanite on by default, and the exact option names.
  2. Nanite supports **opaque and masked** materials; translucent materials aren't rendered by Nanite. Keep glass and other translucent parts as separate, non-Nanite meshes.
  3. Create `/Game/Wraith/Dev/L_KitTest`. Place every piece on a 100 cm grid (grid snapping on, size 100) and build a small test building.
  4. For facades you repeat many times, select the actors and use **right-click > Level > Create Packed Level Actor**. That merges them into one render-optimized actor that you place as a unit. Use **Level Instances** for reusable setups that include gameplay actors, such as a lantern post with its gameplay component. Level Instances keep editing linked: a change updates every copy.
- **Done when:** a test building assembles with no gaps or overlaps at 100 cm snapping, collision works (walk into walls, up stairs), and at least one Packed Level Actor facade exists.
- **Common mistakes:**
  - Snapping off-grid by forgetting to turn grid snapping on.
  - Making everything a Packed Level Actor, including things you still need to edit one by one.
- **Claude can help:** Through the Unreal MCP, Claude can place all kit pieces in a labeled grid in the test map, check Nanite and collision settings on every mesh, and report problems.
- **Time:** 1–2 hours.

### Step 6. Stone, snow, frost, and ice materials with Substrate

**Substrate** is Unreal's material system, on by default in new 5.8 projects and production-ready since 5.7. A Substrate material is built from **slabs** (one physical layer of matter each) that you mix or layer. It's more flexible than the old single-layer model, and it's how snow on stone is built here. If you see older tutorials with the legacy material output node, the ideas carry over; the nodes differ.

- **Goal:** a small set of master materials. Stone gets snow automatically on upward-facing surfaces, controlled globally, and frost and ice look cold under warm lantern light.
- **Do this:**
  1. **Global weather controls.** Create a Material Parameter Collection `MPC_Weather` in `/Game/Wraith/Environments/Shared/Materials/` with scalars `SnowAmount` (0–1), `FrostAmount` (0–1), and `WetAmount` (0–1). Any material can read these, and gameplay or a cutscene can change them for the whole world at once.
  2. **Snow mask function.** Create a material function `MF_SnowMask` that outputs 0–1:
     - start from the world-space vertex normal's Z (1 on flat tops, 0 on walls);
     - subtract a threshold, multiply for sharpness, and saturate;
     - multiply by a noise texture so edges are irregular;
     - multiply by `SnowAmount` from `MPC_Weather`;
     - add vertex color R, so you can paint extra snow into corners with the Mesh Paint tool.

     Unreal's built-in **WorldAlignedBlend** function does the first part. Epic's layered-material docs use it exactly this way, so snow stays on top however the mesh is rotated.
  3. **Master stone material** `M_Stone_Master`, built from two Substrate slabs:
     - **Stone slab:**
       - Base color is the stone texture multiplied by a tint parameter defaulting toward Wet slate `#22232C`.
       - Roughness is lowered by `WetAmount` for the wet-slate look.
       - Normal from the texture.
     - **Snow slab:**
       - Base color is near-white, about 0.8 linear, not pure white. Real snow isn't a perfect reflector, and pure white blows out under lanterns.
       - High roughness.
       - A fine noise normal.
     - Mix the two slabs with `MF_SnowMask` using Substrate's horizontal mixing node, so snow covers stone where the mask is 1.

     `VERIFY:` the exact Substrate node names in 5.8 (Slab BSDF, Horizontal Mixing, and Vertical Layering are the names used since Substrate appeared).
  4. **Material instances** for each stone type and Fab asset: `MI_Stone_Cobble`, `MI_Stone_Wall`, and so on. Keep albedo dark and desaturated, because the palette's 70% base lives here.
  5. **Frost.** Add a frost layer to `M_Stone_Master`, driven by `FrostAmount` and a mask that's stronger near the ground, in corners (vertex color G), and at grazing view angles (a Fresnel node). Frost is a whitish, very rough slab with fine crystalline normal detail. Keep it subtle on stone; make it strong on metal, glass, and wood.
  6. **Ice** `M_Ice`: a single slab with low roughness (0.05–0.15), a slightly blue-gray base color, and strong specular. Use it on icicles and frozen puddles. Avoid translucent, refractive ice for anything numerous: translucency isn't rendered by Nanite and costs a lot. Opaque ice with sharp highlights reads well at night.
  7. **Lantern glass** (for the lantern prop in walkthrough 10) is a separate, non-Nanite mesh with an emissive, masked or translucent material. Its glow color is Lantern gold `#E0A24A` when lit, and nearly black when snuffed. Leave the value as a parameter; walkthrough 10 drives it.
  8. Check a test room under a warm point light (walkthrough 07 has proper values). Snow should be clearly lighter than stone, but never the brightest thing in the frame; the lantern is.
- **Done when:**
  - kit pieces and Fab assets use instances of `M_Stone_Master`;
  - `SnowAmount` changes snow on every surface at once;
  - frost and ice materials exist;
  - `tools/art/palette_ratio.py` on a screenshot of the test room shows the base around 70%.
- **Common mistakes:**
  - Pure white snow: it clips to white and loses all shape. Keep the albedo around 0.8.
  - Baking snow into textures, so it can't be changed later and doesn't match between assets.
  - Heavy translucency on Nanite meshes. It isn't rendered by Nanite; split translucent parts into separate meshes.
- **Claude can help:** Claude can't wire material nodes by clicking, but it can write out every node and connection for you to build. Through the Unreal MCP's Python it can create the Material Parameter Collection, material instances, and parameter values. `VERIFY:` how much of material graph editing Epic's toolsets expose. Claude can also run `palette_ratio.py` on your screenshots.
- **Time:** 2–4 sessions.

### Step 7. Buy smart on Fab (and use Megascans)

- **Goal:** fill the district with props and surfaces you don't need to make, while staying on palette and on budget.
- **Do this:**
  1. **Decide what to buy.** Make: the kit (it defines the district's look), lanterns (gameplay objects), and anything story-specific. Buy or use free assets for: generic props (crates, barrels, market goods, cloth awnings), ground surfaces, rubble, and statues if a style fits.
  2. **Understand the license.**
     - Fab content is under the **Fab Standard License** (some free items use Creative Commons).
     - You may ship it inside a game, but not redistribute it on its own.
     - Buy under the **Personal** tier if you (and any company you control) earned US$100,000 or less from digital content in the last 12 months; otherwise **Professional**. The tier is fixed at the time of purchase.
     - Assets from the old Unreal Marketplace or Quixel generally keep their original license.
  3. **Megascans:**
     - Claim the free starter pack of 1,500+ assets first, and check what it covers.
     - Anything you claimed during 2024's free period stays yours.
     - New Megascans are bought per asset on Fab.
  4. **Get content into Unreal** through the Fab window inside the editor. Epic's docs have a "Fab Window in Unreal Engine" page for 5.8. `VERIFY:` the menu path. Quixel Bridge is being phased out in favor of Fab, so don't build a workflow around it.
  5. **Make it fit the palette.** Megascans are photographed in daylight. Parent their materials to your masters where you can, or darken and desaturate them with instance parameters, and let `MF_SnowMask` add snow.
  6. **Log every asset** in `docs/art/asset-sources.csv`: asset name, Fab URL, license, tier, price, and date. You'll need this for credits, legal questions, and walkthrough 20.
- **Done when:** every non-kit prop in the blockout has a chosen asset (bought, free, or planned to make), and the asset log is complete.
- **Common mistakes:**
  - Mixing art styles: a stylized prop next to photoreal Megascans. Buy for a consistent look.
  - Leaving daylight colors on scanned assets, which breaks the 70% dark base.
  - Not logging licenses, then not knowing later where something came from.
- **Claude can help:** Claude can keep the asset log, check that every imported pack appears in it, and bulk-reparent Fab materials to your masters through the Unreal MCP. Browsing and buying are yours.
- **Time:** ongoing; about 1 session for the first pass.

### Step 8. Icicles along the eaves with PCG

**PCG (Procedural Content Generation)** is Unreal's node-graph system for placing things by rules: "every 30 cm along this roof edge, place a random icicle". It's production-ready since 5.7, and in 5.8 you can hand-edit the generated results without breaking the procedural setup.

- **Goal:** icicles hang along roof edges automatically and consistently, and you can change density everywhere from one graph.
- **Do this:**
  1. **Model 6–8 icicle variants** in Blender: tapered cones with some lumpiness, from 10 to 60 cm long, and one or two clusters. Pivot at the top, since that's where they attach. Name them `SM_Icicle_A` to `SM_Icicle_H`, export them, and import them as Nanite meshes with `M_Ice`.
  2. **Create a PCG graph** `PCG_EaveIcicles` in `/Game/Wraith/Environments/Shared/PCG/`, with this chain:
     - **Get Spline Data**, which reads a spline on the same actor;
     - **Spline Sampler**, with one point every 25–40 cm;
     - **Transform Points**, with a random yaw of 0–360°, a random scale of 0.6–1.3, and a small random offset along the edge;
     - **Density Filter**, to skip some points so the row isn't perfect;
     - **Static Mesh Spawner**, with a weighted list of the icicle meshes (more small ones than large).
  3. **Make a Blueprint actor** `BP_EaveIcicles` with a Spline component and a PCG component using the graph. Place it under a roof edge, shape the spline along the eave, and click **Generate**.
  4. **Gameplay check.** Icicles hang above the player: keep them outside the camera's usual paths and out of collision. Turn collision off on the icicle meshes.
- **Done when:** `BP_EaveIcicles` follows any roof edge, regenerates when you move the spline, and density can be changed in one place.
- **Common mistakes:**
  - Wrong pivot, so icicles float below the eave or stick up through the roof.
  - Collision left on, so the camera bumps into icicles.
  - Too dense. A few clusters read better than a comb of identical spikes.
- **Claude can help:** Claude can create the icicle variants through the Blender MCP (simple, noise-displaced cones), and explain or check the PCG graph. `VERIFY:` whether Epic's MCP toolsets can create PCG graphs; if not, you build the graph and Claude reviews it.
- **Time:** 1–2 sessions.

### Step 9. Snowfall with Niagara (first version)

**Niagara** is Unreal's particle and effects system. This step makes a working snowfall; walkthrough 14 refines it and sets budgets.

- **Goal:** snow falls around the player everywhere outdoors, cheaply, without piling up indoors.
- **Do this:**
  1. **Create a Niagara System** `NS_Snowfall` in `/Game/Wraith/VFX/Weather/` from an empty or simple sprite emitter.
  2. In **Emitter Properties**:
     - set **Sim Target** to **GPUCompute Sim**, because GPU particles handle tens of thousands of flakes cheaply;
     - set **Fixed Bounds**, for example a box of 4000 × 4000 × 2000 cm. GPU emitters need fixed bounds because the CPU can't read the size of a GPU simulation.
  3. **Spawn** in a box around the system's position (a Shape Location module set to a box, about 3000 × 3000 cm wide). Put the box's top about 1000 cm above the player.
  4. **Motion:**
     - initial velocity downward, 50–150 cm/s;
     - a little curl noise for drift;
     - a wind direction parameter, which later reads from `MPC_Weather`.
  5. **Looks:** small sprites (about 1–3 cm), a soft round texture, near-white color with low alpha, and camera-facing. Farther flakes can be slightly larger and slower.
  6. **Follow the player.** Attach `NS_Snowfall` to the player camera, or to a small actor that follows it. Keep particles in **world space**, so flakes don't swing with the camera; only the spawn box follows.
  7. **Stop snow indoors and under roofs:**
     - Add a **Collision** module using **GPU depth buffer** collision, and kill particles on collision. It's cheap, but it only knows about geometry visible on screen.
     - For covered markets and interiors, use trigger volumes that fade `NS_Snowfall`'s spawn rate to zero while the player is inside.

     Accurate hidden-geometry collision (Niagara's GPU ray-tracing collisions) is Experimental. Skip it.
  8. **Start count:** about 10,000–20,000 live particles, then measure (walkthrough 17).
- **Done when:** snow falls around the player wherever they go, doesn't fall through the covered market, and `stat gpu` shows the effect as a small cost.
- **Common mistakes:**
  - No fixed bounds on a GPU emitter, so particles pop out of view.
  - Particles in local space, so snow "sticks" to the camera when it turns.
  - Big, bright flakes near the camera that cover the fight. Keep near flakes small and faint.
- **Claude can help:** Claude can list every module and value for you to set. Through Epic's MCP toolsets it may be able to adjust parameters on an existing system. `VERIFY:` Niagara editing support. It can also write the trigger-volume Blueprint logic or C++.
- **Time:** 1–2 sessions.

### Step 10. Footprints and deformable snow, only where it matters

Real deformable snow, meaning geometry that sinks where characters walk, is expensive and fiddly. There's no official Epic sample for it. Nanite tessellation (Unreal's way of adding real geometric detail from a displacement map) is still Experimental in 5.8, and one forum report says landscape displacement broke in 5.8. For a solo developer, fake it almost everywhere.

- **Goal:** footprints and disturbed snow where the player looks closely (the market square, the Vesper arena), at almost no cost.
- **Do this:**
  1. **Option A, recommended: footprint decals plus snow puffs.**
     - A **deferred decal** is a material projected onto whatever surface is below it. Make `M_Decal_Footprint`: domain Deferred Decal, affecting normal and roughness, with a soft footprint-shaped mask.
     - In walkthrough 05, add foot-contact **Anim Notifies** to walk and run animations (`FootL`, `FootR`).
     - On each notify, spawn a decal at the foot with `UGameplayStatics::SpawnDecalAtLocation`, rotated to the foot, with a lifetime of 20–60 s. Spawn a tiny `NS_SnowPuff` burst too.
     - Only spawn when the surface below is snowy. A **Physical Material** named `PM_Snow` on snow materials lets the code check this with a trace.
     - Cap the number of live decals (for example 64) and remove the oldest first.
  2. **Option B, advanced, for one hero arena only: render-target trails plus displacement.** Draw character positions into a render target, then use it as a height mask to lower the snow material. The displacement comes from Nanite tessellation (Experimental) or from a dense mesh with World Position Offset. Only try this after Option A exists, and after profiling says you have room.
  3. **Combat puffs:** dodges, knockdowns, and slams spawn bigger `NS_SnowPuff` bursts and a larger decal. That sells "deep snow" more than true deformation.
- **Done when:** walking through the market square leaves fading footprints and puffs, and the cost is negligible in `stat gpu` (walkthrough 17).
- **Common mistakes:**
  - Starting with Option B. It can eat weeks, and players rarely notice the difference in a fast brawler.
  - Unlimited decals, which slowly cost more and more.
  - Footprints on stone. Check the physical material first.
- **Claude can help:** Claude can write the decal-spawning C++ or Anim Notify class, the decal cap, and the surface check. You tune the look.
- **Time:** 1–2 sessions for Option A.

### Step 11. The distant city with PCG

The README calls Vesperhall a vertical gothic city. Beyond the playable streets, players should see towers, spires, and rooftops fading into fog, for almost no cost.

- **Goal:** a believable skyline all around the playable area, generated by rules, cheap to render, and on palette.
- **Do this:**
  1. **Make 8–12 silhouette meshes** in Blender: towers, spires, roof clusters, a bridge, and a few big landmark shapes. They should be simple (a few hundred to a few thousand triangles), with one shared material and a window mask in UVs. Nobody will see them up close.
  2. **Distant material** `M_DistantCity`:
     - dark base color near Grave/Wet slate;
     - windows lit with Lantern gold emissive, randomized per instance with the **PerInstanceRandom** node, so only a few windows glow;
     - no normal detail.

     Keep lit windows sparse, because the 20% warm share of the frame belongs to the playable space.
  3. **PCG graph** `PCG_DistantCity`:
     - **Create Points Grid**, at 1,500–3,000 cm spacing, over a large area around the level;
     - a **Difference** node with a volume covering the playable area, so nothing spawns where the player goes;
     - **Transform Points**, with a random offset, a random yaw, and a random height scale (taller near the cathedral, if you like);
     - **Density Filter**, for gaps;
     - **Static Mesh Spawner**, with weighted silhouettes.
  4. Put it on a **PCG Volume** around the level, and generate in the editor (not at runtime), so the result is saved as instances. Turn off collision on the distant meshes. Consider turning off **Cast Shadow** for the farthest ones.
  5. **Layer the depth:** the playable area, a near ring of kit buildings you place by hand, the PCG city, and fog hiding the far edge (step 12).
- **Done when:** from every street you see a layered skyline that fades into fog, and it costs little on the GPU (check `stat gpu`).
- **Common mistakes:**
  - Too many lit windows, which breaks the palette ratio and makes the city look festive instead of dead.
  - Distant meshes with collision or shadows, paying for detail no one sees.
  - Runtime generation you don't need. Generate once in the editor.
- **Claude can help:** Claude can create the silhouette meshes through the Blender MCP from your sketches, describe the PCG graph node by node, and run `palette_ratio.py` on screenshots to check the lit-window share.
- **Time:** 2–3 sessions.

### Step 12. Fog and atmosphere

- **Goal:** fog that separates the city into depth layers, makes lantern light glow in the air, and hides the distant city's edge.
- **Do this:**
  1. **Exponential Height Fog:**
     - add it to the level;
     - set the fog color toward Fog `#554A53`;
     - start with a low density and raise it until the far city just disappears;
     - turn on **Volumetric Fog**, so lights create visible glows and shafts in the air.
  2. **Volumetric fog settings.** Start from these and tune by eye:
     - **Scattering Distribution** about 0.2–0.6. At 0 light scatters evenly; toward 0.9 it scatters mostly forward, which gives stronger halos when you look toward a lantern.
     - **Extinction Scale** at 1. Above 1 absorbs more light.
     - **View Distance** only as far as you need, because a longer view distance shows more under-sampling artifacts.
  3. **Local Fog Volumes** add denser pockets of fog between towers, in alleys, and at the edge of dark zones. With volumetric fog on they're lit and shadowed properly, at a higher cost.
  4. **Sky:** a very dark night sky (walkthrough 07 sets the moon and sky light). Skip volumetric clouds for now; snow and fog hide the sky, and clouds cost a lot.
  5. **Readability check:** in every arena, enemies must stay readable against the fog. If silhouettes vanish, lower the fog density in that space with a Local Fog Volume.
- **Done when:** the far city fades out, lanterns glow in the air, and fights stay readable.
- **Common mistakes:**
  - Fog so thick that enemies disappear in fights.
  - Relying on the volumetric fog view distance to hide the city edge, which causes artifacts. Hide it with regular fog density instead.
- **Claude can help:** through the Unreal MCP, Claude can set fog values from a list you choose, and take before/after screenshots for you to compare. Values you like can be saved into the metrics document as the district's "weather preset".
- **Time:** 1 session, plus tuning with walkthrough 07.

### Step 13. Dress the level and decide its structure

- **Goal:** the blockout becomes the art level without losing any gameplay metrics.
- **Do this:**
  1. **Duplicate** `L_LanternMarket_Blockout` to `L_LanternMarket`. Keep the blockout as a reference.
  2. **Replace** blockout boxes with kit pieces or Packed Level Actor facades. Select a box, then use **right-click > Replace Selected Actors with** and pick the kit mesh. Keep lantern markers, spawn points, and trigger volumes exactly where they were.
  3. **Place props** from Fab and your own lanterns (walkthrough 10), then the icicle Blueprints, snowfall volumes, footprint surfaces, the distant city volume, and fog.
  4. **Level structure.** For linear levels the size of the Lantern Market, a normal level (no World Partition) plus Level Instances is simplest.
     - Epic recommends **World Partition** for level streaming in UE5 projects, and it saves each actor in its own file ("One File Per Actor"). That helps with version control, but adds concepts such as streaming, Data Layers, and HLOD builds.
     - Switch a level to World Partition only if walkthrough 17 shows memory or load problems, or if a district becomes one large continuous space.
  5. **Replay the whole level** with combat after dressing, and fix anything the art broke: blocked paths, camera clipping, or lost readability.
- **Done when:** `L_LanternMarket` plays from start to end with art, every gameplay marker survived, and a playtest finds no new navigation or camera problems.
- **Common mistakes:**
  - Art pieces with more collision than the blockout, so paths are suddenly blocked. Compare against the metrics.
  - Dressing before the blockout has passed a fight test.
- **Claude can help:** through the Unreal MCP, Claude can do the bulk replacement of blockout actors with kit meshes from a mapping you agree on, and compare the positions of gameplay markers between the two levels.
- **Time:** several sessions; the biggest chunk of environment work.

### Step 14. Environment performance and palette check

- **Goal:** the district fits a sane budget and matches the palette before lighting polish.
- **Do this:**
  1. In the viewport, use the Nanite visualization modes (**Nanite Visualization > Triangles, Clusters, Overdraw**) to find hot spots.
  2. Run `stat unit` and `stat gpu` in a busy fight in the market square. Write down the numbers in the metrics document (walkthrough 17 sets the targets).
  3. Take screenshots from the three most important views and run:
     ```powershell
     python tools/art/palette_ratio.py Saved\Screenshots\WindowsEditor\shot1.png --mask shot1_mask.png
     ```
     Aim for a base around 70%, warm around 20%, and violet around 10%. Walkthrough 07 does the final grading. `VERIFY:` the screenshot folder on your machine.
- **Done when:** the numbers are written down and no view is far off the palette ratio.
- **Common mistakes:**
  - Measuring an empty level; measure during a busy fight, with snow and enemies.
  - Judging performance in the editor viewport only. Walkthrough 17 uses packaged builds for final numbers.
- **Claude can help:** Claude runs the palette script, reads the mask images, and suggests which assets push the ratio off.
- **Time:** 1 hour.

---

## Vertical slice checklist

- [ ] `docs/design/environment-metrics.md` with your project's real character numbers, the metrics table, the kit rules, and the blockout color code
- [ ] Beat chart for the Lantern Market, written from the story bible
- [ ] `L_LanternMarket_Blockout`, playable from entry to the Vesper arena, fight-tested in every arena
- [ ] Lantern positions and dark zones marked in the blockout (inputs to walkthrough 10)
- [ ] Starter kit (~20 pieces) modeled, named, pivoted, with collision, exported, and imported as Nanite
- [ ] `L_KitTest` proves the kit snaps at 100 cm; at least one Packed Level Actor facade
- [ ] `MPC_Weather`, `MF_SnowMask`, `M_Stone_Master` (stone, snow, frost), `M_Ice`, and instances for every stone type
- [ ] Fab purchases chosen and logged in `docs/art/asset-sources.csv`, with the license tier recorded
- [ ] `BP_EaveIcicles` with `PCG_EaveIcicles` along the market's roofs
- [ ] `NS_Snowfall` following the player; no snow inside the covered market
- [ ] Footprint decals and snow puffs in the market square and the Vesper arena
- [ ] `PCG_DistantCity` skyline around the district, fading into fog
- [ ] Exponential Height Fog with volumetric fog, plus Local Fog Volumes between towers
- [ ] `L_LanternMarket` dressed, replayed, and fight-tested
- [ ] Performance numbers and palette ratios recorded for three key views

## Going further

- **Shape Grammar in PCG** can build whole building facades from rules. Epic's Cassini sample shows it, along with GPU processing and spline workflows.
- **City Sample** was updated for 5.8 and rebuilt with PCG and the Unreal MCP. It's worth studying for city-scale procedural layout; check its license before reusing assets.
- **Mesh Terrain** (new and Experimental in 5.8) allows overhangs and tunnels in terrain. Probably unnecessary for a city.
- **Nanite tessellation** for the one snow arena, once it leaves Experimental.
- **Trim-sheet authoring** in Substance 3D Designer, or by hand in Krita, for a more varied kit with the same number of textures.
- **Weather states:** drive `MPC_Weather` from gameplay or cutscenes (a blizzard during the Vesper fight, calm after).

## References

**Epic Games** (5.8 documentation)
- CubeGrid tool: https://dev.epicgames.com/documentation/en-us/unreal-engine/cubegrid-tool-in-unreal-engine
- PolyGroup Edit tool: https://dev.epicgames.com/documentation/unreal-engine/polygroup-edit-tool-reference-in-unreal-engine
- Actor snapping: https://dev.epicgames.com/documentation/en-us/unreal-engine/actor-snapping-in-unreal-engine
- Level instancing and Packed Level Actors: https://dev.epicgames.com/documentation/en-us/unreal-engine/level-instancing-in-unreal-engine
- Level design setup and blockout (Designer series): https://dev.epicgames.com/documentation/unreal-engine/designer-01-project-setup-and-level-blockout-in-unreal-engine
- Nanite: https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine
- Substrate overview: https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-substrate-materials-in-unreal-engine
- Layered materials (snow with WorldAlignedBlend): https://dev.epicgames.com/documentation/unreal-engine/creating-layered-materials-in-unreal-engine
- Runtime Virtual Texturing quick start: https://dev.epicgames.com/documentation/en-us/unreal-engine/runtimevirtual-texturing-quick-start-in-unreal-engine
- PCG development guides: https://dev.epicgames.com/documentation/en-us/unreal-engine/pcg-development-guides
- PCG with GPU processing: https://dev.epicgames.com/documentation/unreal-engine/using-pcg-with-gpu-processing-in-unreal-engine
- GPU sprite effect in Niagara: https://dev.epicgames.com/documentation/unreal-engine/how-to-create-a-gpu-sprite-effect-in-niagara-for-unreal-engine
- Niagara scalability and best practices: https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-and-best-practices-for-niagara
- Volumetric fog: https://dev.epicgames.com/documentation/unreal-engine/volumetric-fog-in-unreal-engine
- Exponential Height Fog: https://dev.epicgames.com/documentation/en-us/unreal-engine/exponential-height-fog-in-unreal-engine
- Local Fog Volumes: https://dev.epicgames.com/documentation/en-us/unreal-engine/local-fog-volumes-in-unreal-engine
- World Partition: https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine
- One File Per Actor: https://dev.epicgames.com/documentation/en-us/unreal-engine/one-file-per-actor-in-unreal-engine
- Fab window in Unreal Engine: https://dev.epicgames.com/documentation/en-us/unreal-engine/fab-window-in-unreal-engine
- City Sample with PCG: https://dev.epicgames.com/documentation/unreal-engine/city-sample-pcg-for-unreal-engine

**Fab**
- Licenses and pricing: https://dev.epicgames.com/documentation/en-us/fab/licenses-and-pricing-in-fab
- Fab EULA: https://www.fab.com/eula
- Free Megascans: https://www.fab.com/megascans-free
- Fab transition FAQ: https://support.fab.com/s/article/Fab-Transition-FAQs

**Samples**
- Cassini sample (PCG): https://www.unrealengine.com/en-US/news/the-cassini-sample-project-is-now-available
- Electric Dreams environment: https://www.unrealengine.com/electric-dreams-environment

**Blender**
- Blender manual (units, snapping, modifiers): https://docs.blender.org/manual/en/latest/

**Recommended learning channels**
- Unreal Engine on YouTube (official; search for PCG and Nanite talks): https://www.youtube.com/@UnrealEngine
- Epic Developer Community learning library (community tutorials on snow and PCG): https://dev.epicgames.com/community/unreal-engine/learning
