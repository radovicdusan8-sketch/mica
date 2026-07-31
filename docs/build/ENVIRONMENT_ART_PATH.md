# Environment Art Path — Concept Painting → Playable City

**Goal:** turn a city *concept painting* (like the Takanoha / Ukishima / Homura keys) into a level you can actually walk, fight, and explore in Unreal Engine 5 — at a solo-learner pace, mostly without code.

**Companion to:** [`CITY_DESIGN.md`](../design/CITY_DESIGN.md) (the design intent per city) and the character/animation build paths in this folder. Same spirit as [`MILESTONE_0.md`](MILESTONE_0.md): learn by building one slice at a time.

**Good news:** environment art in UE is **almost entirely no-code** — placing meshes, painting materials, lighting, fog. It's the most beginner-friendly part of the whole game.

---

## The golden rule

> **A concept painting is a target feeling, not a blueprint to trace.**

You never model the painting pixel-for-pixel. You pull **five things** out of it and rebuild *those* in 3D:

1. **Landmark silhouette** — the one big shape players navigate by (the bell-cliff, the harbor tiers, the forge stacks).
2. **Player path & focal point** — where the player stands and where the eye is pulled.
3. **Palette** — the exact colors (eyedrop them from the painting).
4. **Lighting & time of day** — the mood. ~60% of the final result is lighting, not models.
5. **Key materials** — black water, lantern paper, wet wood, scorched iron.

`CITY_DESIGN.md` already extracted most of this for every city — that doc is the bridge between painting and engine.

---

## The pipeline (in this order — don't skip step 1)

### Step 1 — Greybox / blockout (NO art)
Build the whole location out of plain grey boxes and **play it** with the Manny stand-in from Milestone 0.
- Tools: UE **Modeling Mode** cubes, or simple placeholder meshes.
- Nail: **scale** (is the gate huge? is the alley tight?), **layout & player flow**, **sightlines to the landmark**, **combat arena** shapes, and **verticality**.
- Test constantly: can you run it, does it read, is it fun to move through — *before* it's pretty?
- **This is the step beginners skip and always regret.** A greybox that plays well becomes a beautiful level; a beautiful level that plays badly is wasted work.

### Step 2 — Build a small MODULAR KIT (not a city)
You don't model "Ukishima." You model ~10–20 **reusable pieces** and kitbash the city from them.
- In **Blender** (you already have it set up): make a wall segment, a roof piece, a pillar, stairs, a pier plank, a stilt, a railing, plus 2–3 **hero pieces** unique to that city (a bell-tower, a soul-ferry, a forge-bellows).
- Model to a consistent **grid size** (e.g. 1m / 2m) so pieces snap together in UE.
- Export as **FBX** → import to UE (same workflow as your `SKM_Manny` and katana).
- One kit builds an entire city, and re-skinned kits build the next one.

### Step 3 — Buy/borrow the generic, hand-make only the hero
Solo devs don't model everything. Save your hours for what makes the city *yours*.
- **Free & included:** Quixel **Megascans** (rocks, cliffs, foliage, surfaces — free in UE), UE **Starter Content**, **Fab** marketplace packs (Japanese/feudal kits exist).
- **Model by hand only:** your signature landmarks and story props (the Ember Forge, the bell-towers, Tomoe's forge, the Fivefold katana).
- Customize bought assets with your palette/materials so they don't look generic.

### Step 4 — Materials & palette (photoreal, high-fidelity)
**Art direction is realistic** (re-locked 2026-07-31): real buildings, real materials, real light — *not* cartoon or painterly. UE renders realistic by default, so here you *lean into* its strengths, not fight them.
- Use **PBR materials** and **Megascans**-grade surfaces (real stone, wood, metal, cloth); **Nanite** for high-detail geometry, **Lumen** for realistic global illumination. Aim for Ghost of Tsushima / Nioh / Elden Ring fidelity.
- The *style* comes from **design and mood**, not a stylized shader: dramatic, overkill architecture rendered photoreal.
- Add a **Post Process Volume** and color-grade to the concept's palette for *mood* (a LUT or manual grade) — pull the tone toward the concept **without** flattening it into an illustration.
- Keep the **clan palette** consistent (see `CITY_DESIGN.md` §0): Wind pale/sky-blue, Water blue/teal, Fire crimson/ember, etc.

### Step 5 — Lighting & atmosphere (the mood engine)
Match the painting's time of day and feeling.
- **Directional Light** (sun/moon) + **Sky** for the base; **Lumen** (UE5) for bounced light.
- **Exponential Height Fog + Volumetric Fog** for the drifting **mist** — your world's signature (Amagiri = "Heaven's Mist"). Thin in safe places, thick where the veil is close.
- **Light shafts / god-rays**, and local lights: **lantern glow** (Higan), **forge-orange** (Homura, Kurogane-jō), cold moonlight (Ukishima).
- Mood is ~60% of the result — spend real time here.

### Step 6 — Set dressing to "overkill," then optimize
- **Foliage tool** for grass/trees; **decals** for grime/posters/cracks; **Niagara particles** for the signature motion: **embers** (Homura), **drifting lanterns** (Higan), **blown leaves & swaying cloth/bells** (Takanoha), **rain & fog wisps** (Ukishima).
- Then optimize for the **open regions** you chose: **World Partition** (UE5 open-world streaming), **LODs/HLODs**, distance culling, **Nanite** for dense meshes.

---

## The matte-backdrop trick (use your paintings directly)
For the **unreachable distance** — the giant landmark on the horizon you never walk to — you don't have to build it in 3D. Drop a **high-resolution matte backdrop** (a realistic concept render / photo-composite, not a cartoon) onto a large card/dome in the far background, and build only the playable foreground in real geometry. Cheap, fast, and it keeps the *exact* dramatic vista while staying photoreal. Great for the Cliff of Bells' cloud-gulf and Homura's smoldering volcano.

---

## How this maps to the milestones
- The **character** path (Milestones 0–3) and this **environment** path run in parallel — you need a place to test Ryuma's movement and combat anyway.
- **First city to actually build: Takanoha** — it's the Milestone-4 Wind boss target. Don't build the whole city first; build a **vertical slice** (the summit shrine + the boss platform + one approach bridge), enough to stage the Tengu fight.
- Reuse that Takanoha kit + lighting recipe to go faster on the next city.

---

## Suggested first exercise (a weekend-sized win)
1. Greybox **one screen** of Takanoha: a bell-platform, a rope-bridge, and the shrine you're climbing to. Play it with Manny.
2. Add **fog + a directional light + a color-grade** to hit the pale, holy palette.
3. Drop the **Takanoha concept painting** as a matte backdrop in the cloud-gulf behind it.
4. Stand on the bridge. If it already *feels* like the painting with zero custom models — that's the lesson: **mood before models.**

## Notes
- Keep custom kit pieces and Blender sources under `art/` (as with the katana); UE `Content/` stays out of git via `.gitignore`.
- When a city's look is approved from concept art, add its **palette hex values + lighting recipe** to `CITY_DESIGN.md` so the in-engine build has exact targets.
