# 03. Concept Art

> **Written for:**
> - Krita 5.3.x (the krita.org build) with the Krita AI Diffusion plugin 1.53.
> - ComfyUI with ROCm on Windows, and FLUX.2 [klein] 4B as the local model.
> - Hosted generators as of September 2026: Midjourney V8.2, ChatGPT Images 2.5, Google's Nano Banana 2 (Gemini 3.1 Flash Image), and Adobe Firefly.
> - Blender 5.2 LTS for reference images.
> - Repo files `docs/art/wraith-palette.gpl` and `tools/art/palette_ratio.py`.
>
> **Facts checked:** 2026-09-27. Most vendor sites were blocked from this environment, so vendor facts come from search excerpts of official pages or from the projects' GitHub repositories. AI tools and their terms change monthly, so recheck prices and terms before paying. Unconfirmed items are marked `VERIFY:`.

## What this covers

This walkthrough produces consistent, usable concept art for Wraith by combining AI image generation with Krita paintovers:

- a written style guide and the palette loaded into Krita;
- a reference library with licenses recorded;
- mood boards and Lantern Market key frames;
- silhouette-first character design;
- locked "canon" sheets that keep characters consistent from image to image;
- orthographic turnaround sheets that Blender can model from;
- environment and prop sheets (the lantern above all);
- the records that copyright and Steam's AI disclosure rules will ask about.

## Why it matters for Wraith

- **The README's art rules are strict and unusual:**
  - 70% darkness and stone, 20% warm light, 10% violet;
  - warm means the living, violet means the dead;
  - characters must read by silhouette.

  Concept art is where these rules become concrete pictures. Every later area (04, 06, 07, 14) copies from it.
- **A brawler needs instantly readable enemies.** In a dark, snowy, fogged scene in the middle of a combo, the player must tell a shielded cultist from a Choir singer from a snuffer from a heavy by shape alone.
- **AI speeds up exploration but drifts.** It gives you many options fast, but characters change between images, details don't add up, and front and side views never line up. The Krita pass and the turnaround rules turn pretty pictures into production drawings.
- **Modeling depends on turnarounds that agree.** A front view and a side view that disagree cost hours of guessing in Blender (walkthrough 04).
- **Legal and store requirements.** AI-generated images alone aren't copyrightable in the US, and Steam asks about AI content. Keep records from day one.

## Tools

| Tool | What it's for | Cost | Commercial license OK? | AMD notes |
|---|---|---|---|---|
| Krita 5.3.x | Paintovers, silhouettes, turnaround cleanup, palette checks | Free (GPL-3.0) from krita.org. Krita calls 6.0 experimental and recommends 5.3 for real work. | Yes | None |
| Krita AI Diffusion plugin 1.53 | AI generation inside Krita: inpainting, live painting, pose and line-art control, reference images, upscaling | Free (GPL-3.0) | Yes (plugin); model licenses vary, see below | Supports AMD on Windows through ROCm via its managed install. DirectML is obsolete in the plugin. |
| ComfyUI (local generation engine) | Runs open models on your GPU; used by the Krita plugin | Free (GPL-3.0) | Yes (model licenses vary) | Officially supports AMD on Windows through ROCm, including RDNA 4. AMD's own table lists RDNA 4 on Windows as "build passing", not fully tested, so expect some rough edges. |
| FLUX.2 [klein] 4B (open model) | Local generation and multi-reference editing | Free | **Apache 2.0**: yes | About 8–9 GB of VRAM, so it fits the 16 GB card |
| Midjourney V8.2 | Mood and style exploration | Subscription. `VERIFY:` current plan prices. | Yes. Companies with over US$1M annual revenue need Pro or Mega. **Images are public unless you have Stealth, which only Pro and Mega include.** | Hosted; no GPU needed |
| ChatGPT Images 2.5 (OpenAI) | Reference-based character images and edits | Included in ChatGPT plans. `VERIFY:` limits and prices. | Yes. OpenAI's terms assign output rights to you. | Hosted |
| Nano Banana 2 (Google, Gemini 3.1 Flash Image) | Multi-reference consistency. Google cites up to 14 reference images and up to 5 consistent characters for its Nano Banana models; `VERIFY:` whether that figure applies to Nano Banana 2 or only to Nano Banana Pro. | Through Gemini plans or the API. `VERIFY:` prices. | Yes. Google doesn't claim ownership. Outputs carry an invisible SynthID watermark and C2PA metadata. | Hosted |
| Adobe Firefly | "Commercially safe" generation (trained on licensed content) | Firefly Pro from US$29.99 (7,000 credits). Partner models from other companies use extra credits. | Yes for Firefly's own models; you judge partner models yourself | Hosted |
| BeeRef | Reference boards | Free (GPL-3.0). Last release 2024, so it's quiet but works. | Yes | None |
| PureRef 2 (alternative) | Reference boards | Commercial use needs a paid per-seat license. `VERIFY:` the price for a sole developer. | Only with a paid license | None |
| Blender 5.2 | Turnarounds as modeling references; 3D paintover blocks | Free | Yes | None |

**Model licenses, the short version.** Output rights and model rights differ, so read the actual license:
- **Apache 2.0 (fine for a commercial game):** FLUX.2 [klein] 4B, FLUX.1 [schnell], Qwen-Image. Qwen-Image is 20B parameters, too big for 16 GB without offloading.
- **Fine with conditions:**
  - SDXL (OpenRAIL++-M): no rights claimed on outputs; use restrictions apply.
  - Stable Diffusion 3.5 (Stability AI Community License): free if total annual revenue is under US$1M, and you must register.
- **Avoid for Wraith:** FLUX.1 [dev], FLUX.2 [dev], and FLUX.2 [klein] 9B. Their licenses restrict the models to non-commercial use, even though they say outputs may be used commercially. That contradiction is worth avoiding entirely.

## Before you start

- **Walkthroughs done:** 01 (repo, Blender).
- **Inputs:** the README's art direction and the story bible's character descriptions.
- **Budget decision:** one hosted subscription, local generation on your own GPU, or both (step 4).
- **Disk space** if you go local:
  - the Krita plugin's managed install plus one model: roughly 15–25 GB;
  - AMD's optional "AI Bundle" (ComfyUI, PyTorch, and more, installed through AMD Software): about 35 GB.

  Check the sizes shown before downloading.
- **Mindset:** AI output is raw material. The design decisions, and the final drawings, are yours.

---

## Steps

### Step 1. Write the visual style guide

- **Goal:** a short document that anyone, including Claude or an AI generator prompt, can follow to stay on-style.
- **Do this:** create `docs/art/style-guide.md` with these sections. Ask Claude to draft it from the README and the story bible, then rewrite it in your own words.
  1. **Palette:** the six README colors with hex values, what each is for, and the 70/20/10 ratio.
  2. **The rules:**
     - warm light means the living;
     - violet means the dead;
     - darkness means danger;
     - never violet on anything living, never warm light on anything dead;
     - characters read by silhouette.
  3. **Values first.** Most of every image is in the darkest third of the value range. The brightest values are reserved for lanterns and focal points.
  4. **Shape language:** gothic verticals, pointed arches, tall narrow windows, snow-softened tops, and icicles on every edge. Add a line per faction as you design them.
  5. **Materials:** wet slate stone, frost, snow in shadow, old iron, porcelain masks (the Choir), candle and oil light.
  6. **Readability rules for enemies:** each archetype has one silhouette feature that reads at 64 pixels tall.
  7. **Prompt vocabulary:** words that produce the look ("wet slate", "lantern-lit", "deep blue-black shadow", "heavy snow", "fog between towers"), and words to avoid ("neon", "sunny", "cyberpunk", "vibrant").
  8. **Ethics rule:** don't prompt with living artists' names. It's a common courtesy, it's the direction the law is moving, and it isn't needed when you have your own style guide and references.
- **Done when:** the guide fits on about two pages and you'd be happy handing it to a hired artist.
- **Common mistakes:**
  - A style guide that's a list of adjectives with no rules.
  - Leaving out the value structure, which matters more than color at night.
- **Claude can help:** Claude can draft and tighten the guide, and later check images against it: it can view PNG and JPG files and run `palette_ratio.py`.
- **Time:** 1–2 hours.

### Step 2. Set up Krita with the Wraith palette and check layers

- **Goal:** Krita ready for paintovers, with the palette loaded and one-click checks for value and palette.
- **Do this:**
  1. Install **Krita 5.3.x from krita.org**. The AI plugin's docs say some parts can't install into the Windows Store or Steam versions.
  2. **Import the palette** `docs/art/wraith-palette.gpl` (in this repo): use **Settings > Manage Resources > Import Resources**, or the import button in the Palette docker. Show the Palette docker with **Settings > Dockers > Palette**. `VERIFY:` the exact import menu in 5.3.
  3. **Make a paintover template** `source-art/concept/_templates/paintover.kra`:
     - a canvas of 3840 × 2160 px for key frames;
     - a layer group "Paint" for your work;
     - on top, two **filter layers**, hidden by default:
       - **Value check:** a filter layer with **Adjust > Desaturate**. Toggle it to see only values; night scenes should be mostly dark.
       - **Palette check:** a filter layer with **Map > Gradient Map**, using a gradient from Grave through Wet slate and Fog to Porcelain. Toggle it to see how the image maps onto the palette's value range.
  4. Turn on **View > Show Rulers** and drag guides out of the rulers for alignment (used in step 10).
- **Done when:** the palette appears in the Palette docker, and both filter layers toggle on and off in the template.
- **Common mistakes:** painting on the filter layers. They're views; keep your paint in the "Paint" group.
- **Claude can help:** the palette file already exists in the repo. Claude can generate more palettes (for example a per-district accent palette) in the same `.gpl` format. The Krita setup is manual.
- **Time:** 30 minutes.

### Step 3. Build a reference library with licenses recorded

**References** are real-world photos and artworks you study for ideas: architecture, clothing, lighting. They're not traced into final assets.

- **Goal:** organized references, with where each came from, so there are no legal surprises later.
- **Do this:**
  1. Use these folders:
     - `source-art/concept/references/architecture/`
     - `.../costume/`
     - `.../lighting/`
     - `.../snow-and-ice/`
     - `.../props/`
  2. Keep `docs/art/reference-sources.csv` with the columns `file, source URL, license or "reference only", notes`. Photos you took yourself are the best references of all: winter nights, candles, stone, and frost.
  3. Make one board per topic in **BeeRef** (free). PureRef needs a paid license for commercial use. Save boards next to the images. Add `*.bee` and `*.pur` to `.gitattributes` as LFS types (walkthrough 01, step 7), since boards embed images.
  4. **Rule:** references inform; they're never copied. Nothing from `references/` goes into the game or its marketing.
- **Done when:** the folders and boards exist for architecture, costume, lighting, and snow, and every image has a row in the sources file.
- **Common mistakes:**
  - Hoarding thousands of images. Fifty good references per topic beat five thousand.
  - Losing track of where images came from.
- **Claude can help:** Claude can keep the sources CSV tidy, find missing entries by comparing it to the folders, and summarize references into notes for the style guide. It can view images you give it. It can't browse image sites for you from this setup.
- **Time:** 2–3 hours, then ongoing.

### Step 4. Choose your AI tools

- **Goal:** one main generator you know well, plus an optional second one, chosen for consistency, privacy, and license.
- **Do this:** compare the options below, try your top choice on one real task (a Wraith variation from his canon sheet, step 8), then decide.
- **Compare:**

  | | Hosted (Nano Banana 2, ChatGPT Images, Midjourney, Firefly) | Local (Krita AI Diffusion + FLUX.2 [klein] 4B on your RX 9060 XT) |
  |---|---|---|
  | Quality out of the box | High, and improving monthly | Good; fewer "wow" images, more control |
  | Consistency tools | Reference images: many in Google's Nano Banana models (up to 14 by Google's figures), up to 4 in Midjourney V8's edit model; ChatGPT preserves subjects from references | Multi-reference editing, pose and line-art control, painting directly into the generation |
  | Privacy (unannounced game) | Private, except **Midjourney without Stealth (Pro or Mega only), where images are public** | Fully private |
  | Cost | Monthly subscription or credits | Free after setup; uses your GPU and electricity |
  | Setup risk | None | ROCm on Windows for RDNA 4 is new; expect some fiddling |
  | License clarity | Read each service's terms; the four above all let you use outputs commercially, with conditions noted in the Tools table | Apache 2.0 model: clear |

- **Recommendation:**
  1. Start with **one hosted tool that's strong at multiple references**: Nano Banana 2 or ChatGPT Images. Character consistency is your main problem, and both handle reference images well.
  2. Add **local Krita AI Diffusion** when you start paintovers and turnarounds. Painting directly into generations, with pose and line-art control, is where it shines.
  3. Use **Midjourney** only if you like its aesthetic for mood boards and accept that images are public below the Pro plan. That's a real spoiler risk for an unannounced game.
- **Done when:** you've written your choice and the reasons in `docs/art/style-guide.md`, under "Tools".
- **Common mistakes:**
  - Juggling four subscriptions.
  - Using a tool whose license restricts commercial use of the model.
- **Claude can help:** Claude can compare the current terms if you paste them in, and write prompt templates for the chosen tool. **Claude Code can't generate images itself.**
- **Time:** 30 minutes.

### Step 5. Optional: local generation on the RX 9060 XT

- **Goal:** a working local setup inside Krita, if you want privacy and hands-on control.
- **Do this, in order of simplicity:**
  1. **Krita AI Diffusion's managed server** (recommended):
     - Download the plugin ZIP from its GitHub releases.
     - In Krita, use **Tools > Scripts > Import Python Plugin from File**, then restart Krita.
     - Open **Settings > Dockers > AI Image Generation** and click **Configure**.
     - Choose **Local Managed Server** and pick the AMD (ROCm) backend **before** installing.

     The plugin then installs its own ComfyUI with a ROCm build of PyTorch.
  2. **ComfyUI's portable AMD build** (for using ComfyUI directly): download `ComfyUI_windows_portable_amd.7z` from ComfyUI's releases and start it with `run_amd_gpu.bat`. In the Krita plugin, choose **Custom Server** to connect to it.
  3. **AMD's "AI Bundle"**, an optional install in AMD Software: Adrenalin Edition 26.1.1 and later. It includes ComfyUI and PyTorch, and needs about 35 GB. AMD lists "RX 7700-series or newer" as the requirement. `VERIFY:` that your RX 9060 XT qualifies.

  **Model:** download **FLUX.2 [klein] 4B** through the plugin's model options or ComfyUI's model manager. It's Apache 2.0 and about 8–9 GB of VRAM, and it supports multi-reference editing.

  **If setup fails:** AMD's own support table marks RDNA 4 on Windows as "build passing" but not fully tested. If it won't run after an honest try (an evening), don't sink more time into it. Use the hosted tools, and revisit after the next AMD driver release.
- **Done when:** Krita generates a 1024 × 1024 image locally in a reasonable time. Write the time down; it's your baseline.
- **Common mistakes:**
  - Installing models whose licenses restrict commercial use (see Tools).
  - Using the Windows Store or Steam version of Krita with the plugin.
  - Running Unreal and local generation at once and wondering why everything is slow. They share the 16 GB of VRAM.
- **Claude can help:** Claude can read install logs and error messages you paste, and suggest fixes. Installing is manual.
- **Time:** 1–3 hours, with a stop rule of one evening.

### Step 6. Mood boards and Lantern Market key frames

A **key frame** here is a finished illustration of an important view. It's the target that environment (06) and lighting (07) try to match.

- **Goal:** two or three approved key frames that define the Lantern Market's look.
- **Do this:**
  1. **Mood board:** in BeeRef, collect 20–40 references and early generations for the district: architecture, market life, snow, lantern light.
  2. **Thumbnails:** generate 20–40 small, fast variations. A prompt template to start from, adapted per tool:
     > wide shot of a gothic market street at night in heavy snow, stone buildings with pointed arches, a stopped cathedral clock tower in the fog behind, lit only by warm amber lanterns, deep blue-black shadows, cold desaturated stone, fog between towers, painterly concept art

     Attach your palette image and one or two best references as image prompts. Most generators follow reference images better than hex codes typed into text.
  3. **Pick 3–5** by squinting. Choose clear value structure and composition, not detail.
  4. **Paintover in Krita:** fix the composition, push values toward mostly dark, pull color into the palette, put lanterns where the level design wants them, and remove everything that isn't Wraith (stray neon, wrong architecture, daylight colors).
  5. **Check:** toggle the value and palette check layers, and run:
     ```powershell
     python tools/art/palette_ratio.py source-art/concept/environments/lantern-market/KF_LanternMarket_Street_v03.png --mask kf_mask.png
     ```
     Aim for a base around 70%, warm around 20%, violet around 10%. Violet can be lower in a scene without the dead.
  6. **Approve** two or three frames: a market street, the market square, and the Vesper arena. Save them as `KF_<Subject>_v##.png` and copy small JPGs to `docs/art/` so they're easy to link from design docs.
- **Done when:** the key frames are approved, pass the palette check, and are linked from `docs/design/environment-metrics.md` (walkthrough 06).
- **Common mistakes:**
  - Approving a gorgeous image whose composition can't be built with the kit.
  - Accepting AI lighting that breaks the rules, such as warm light on a spirit.
- **Claude can help:** Claude can write and vary prompts, review candidates you save (it can view the images), run the palette check, and compare frames against the style guide.
- **Time:** 2–4 sessions.

### Step 7. Character design, silhouettes first

- **Goal:** designs for Wraith, Sister Vesper, and the four enemy archetypes that read instantly by shape.
- **Do this:**
  1. **Silhouettes before detail.** For each character, fill 12–20 small black shapes in Krita: no interior detail, just the outline. Try distinct ideas, not variations of one.
  2. **The 64-pixel test.** Shrink the sheet so each figure is 64 px tall. Can you tell every enemy archetype apart instantly? Now imagine them in fog, mid-attack. Ask yourself for each one: *what single shape identifies it?* The README gives some anchors: the Choir wears porcelain; the shielded cultist has a shield; snuffers put out lanterns; the heavy is large. Decide the rest from the story bible.
  3. **Wraith's silhouette** is the tattered cloak (walkthrough 04 builds it in Marvelous Designer). Design how it reads standing, running, and mid-attack. It's the player's anchor in the dark.
  4. **Variations with AI:** take the two or three strongest silhouettes and generate costume and material variations, attaching the silhouette as a reference or control image.
  5. **Palette logic per character:**
     - The dead get violet accents, never warm light.
     - The living may carry warm light, never violet.
     - Enemies' dangerous parts (weapons, telegraph glows) must be visible against dark backgrounds, without breaking those two rules.
- **Done when:** each character has a chosen silhouette that passes the 64-pixel test, and one AI-assisted costume direction.
- **Common mistakes:**
  - Detailing too early.
  - Enemies that differ only in color or texture. In fog and snow, color and texture vanish first.
- **Claude can help:** Claude can review silhouette sheets you save and point out which figures are confusable. It can also write generation prompts per archetype from your notes.
- **Time:** 1–2 sessions per character; enemies can share sessions.

### Step 8. Lock each character with a canon sheet

A **canon sheet** is the one authoritative image of a character. Every later image, model, and texture is checked against it.

- **Goal:** one sheet per character that ends debates about "which version is right".
- **Do this:**
  1. Paint over your chosen direction into a clean, front-facing, full-body image with even lighting.
  2. Add callouts:
     - materials;
     - palette hex values per area;
     - which parts glow (and which color);
     - which parts are cloth that will be simulated (the cloak);
     - 2–3 detail close-ups: mask, weapon, emblem.
  3. Save as `source-art/concept/characters/<name>/<name>_canon_v01.kra`, with a PNG export. Update the version number only when you deliberately change the design.
  4. Link it from the character's section in the story bible or style guide.
- **Done when:** Wraith, Vesper, and the four archetypes each have a canon sheet at v01 or later.
- **Common mistakes:** letting the canon drift by treating any nice new generation as the new canon. Changes should be deliberate, versioned, and noted.
- **Claude can help:** Claude can keep a character sheet index (`docs/art/characters.md`) and check new images against the canon for obvious deviations.
- **Time:** 1 session per character.

### Step 9. Keep characters consistent across images

- **Goal:** new images of a character look like the same character.
- **Do this**, depending on the tool:
  - **Hosted tools:**
    - Always attach the canon sheet, and a detail close-up, as reference images. Google's Nano Banana models take many references (up to 14 by Google's figures) and keep several characters consistent. ChatGPT Images 2.5 is built to preserve subjects from references.
    - Midjourney V8's edit model takes up to 4 reference images. `--sref` (style reference), moodboards, and personalization keep the style steady. The older `--oref` (omni reference) only works with V7.
  - **Local, in Krita AI Diffusion:**
    - FLUX.2 [klein] 4B's multi-reference editing.
    - Pose control: an editable pose figure, so the character's pose is set independently of its design.
    - Line-art control: your own sketch drives the shapes.
    - Fixed seeds for repeatable variations.
  - **LoRA training** (teaching a model your character) isn't practical on AMD Windows right now. The common training tools only support AMD on Linux, or not at all. Skip it; paintover is more reliable anyway.
  - **Paintover is the real consistency tool.** Generate close, then correct by hand against the canon sheet.
  - **Log every kept image** in a sidecar text file next to it (`<image>.prompt.txt`): tool, model, prompt, reference images, seed, and date. You'll thank yourself when you need a variation months later.
- **Done when:** five new images of Wraith in different poses all match the canon sheet after paintover.
- **Common mistakes:**
  - Regenerating endlessly instead of fixing the last 10% by hand.
  - Not saving prompts, so a good result can't be reproduced.
- **Claude can help:** Claude can maintain the prompt logs, spot differences from the canon, and write variation prompts.
- **Time:** ongoing.

### Step 10. Turnaround sheets for modeling

A **turnaround** shows a character from exact front, side, and back views at the same scale, like an engineering drawing. Walkthrough 04 models directly on top of these images.

- **Goal:** turnarounds for Wraith and Vesper, plus simpler ones for the four archetypes, that line up perfectly across views.
- **Do this:**
  1. **Spec**, which applies to every turnaround:
     - **Pose:** an **A-pose**, arms about 45° down from horizontal, palms down, legs slightly apart. AccuRIG (walkthrough 05) accepts A or T poses, and an A-pose deforms better at the shoulders.
     - **Views:** front, side (left), and back; a three-quarter view optionally, for reading only.
     - **Canvas:** one PNG per view at the same size, for example 2048 × 2048, with the feet on the same bottom line and the head at the same height in every view.
     - **Guides:** horizontal guides at the top of the head, eyes, chin, shoulders, chest, waist, hips, knees, and soles, identical in all views.
     - **Lighting:** flat and even, no cast shadows, no perspective. Orthographic, like a blueprint.
     - **The cloak** (Wraith): one set with the cloak and one without, so the body underneath can be modeled.
     - **Details:** separate close-ups of the head or mask (front and side), hands, and any weapon.
  2. **Draft with AI:** attach the canon sheet and a pose reference (an A-pose figure) and ask for front, side, and back views. In Krita AI Diffusion, pose control does this well. Expect the views not to line up.
  3. **Align in Krita:** place the guides from the spec and use the Transform tool to scale and shift each view until the landmarks sit on the same guides.
  4. **Fix by hand:** redraw wherever the views disagree (belt height, sleeve length, mask shape). This is the step that makes the sheet usable.
  5. **Export** `source-art/concept/characters/<name>/<name>_turn_front.png`, `_side.png`, and `_back.png`.
- **Done when:** holding the front and side views next to each other, every landmark matches the guides, and the cloak-off version shows the full body.
- **Common mistakes:**
  - Accepting AI views with perspective (feet bigger than the head). Blender needs orthographic views.
  - Different canvas sizes per view.
  - Forgetting the cloak-off version, then guessing the body in Blender.
- **Claude can help:** Claude can check alignment by comparing landmark positions in the images you save, and set the images up in Blender (step 12).
- **Time:** 1–2 sessions per hero character; less for enemies.

### Step 11. Environment and prop sheets

- **Goal:** the drawings walkthroughs 06 and 10 build from.
- **Do this:**
  1. **The lantern** is the most important prop, because gameplay depends on it (walkthrough 10). One sheet shows:
     - the lantern design from front and side, with dimensions in centimeters;
     - its four states: lit, dimming, snuffed, and relit (the relight moment);
     - how it reads at gameplay distance: shrink it to 32 px and check that lit versus snuffed is obvious.
  2. **Kit elevation sheet:** front views (elevations) of the modular wall, arch, window, door, stair, and roof pieces, drawn over a **100 cm grid**, matching the kit rules in walkthrough 06. It's the modeling reference for the kit.
  3. **Market props:** stalls, awnings, crates, and hanging goods, with notes on which to buy on Fab and which to make.
  4. **The Vesper arena:** a top-down layout sketch plus one key frame, drawn with the arena size from walkthrough 06's metrics.
  5. **Use a 3D paintover for environments** (strongly recommended):
     - Block the scene in Blender or Unreal with the kit's blockout pieces.
     - Render a plain gray image from the game camera's height and angle.
     - Paint over it in Krita, or use it as a line-art or depth control image in Krita AI Diffusion.

     Perspective and scale then match the real game, which a from-scratch painting almost never does.
- **Done when:** the lantern sheet, kit elevation sheet, props list, and arena layout exist and are linked from walkthrough 06's metrics document.
- **Common mistakes:**
  - Environment paintings at impossible scales (doors 5 m tall, streets 50 m wide) that the kit can't reproduce.
  - A lantern that only reads close up.
- **Claude can help:** through the Blender MCP, Claude can build the gray blockout scenes for 3D paintovers from your sketch, set the camera, and render them. It can also draw the 100 cm grid overlay image for the elevation sheet.
- **Time:** 2–4 sessions.

### Step 12. Load turnarounds into Blender

- **Goal:** Blender scenes set up to model directly over the turnarounds (walkthrough 04).
- **Do this:**
  1. In Blender, switch to the **Front** orthographic view (**Numpad 1**). In Object Mode, use **Add > Image > Reference** and pick `<name>_turn_front.png`. Blender aligns the image to the current view.
  2. Switch to the **Right** view (**Numpad 3**) and add the side image the same way.
  3. For each image empty, in its **Object Data** properties:
     - **Depth: Front** with a low **Opacity**, which the Blender manual suggests for modeling references;
     - **Show In:** Orthographic only, so it doesn't clutter the perspective view.
  4. **Scale:** set each image so the character's height, from the sole guide to the top-of-head guide, equals the design height in meters (for example 1.85 m). Put the soles on the grid floor (Z = 0), then line up the side view with the front.
  5. Save as `source-art/blender/characters/<name>/<name>_model.blend`.
- **Done when:** front and side references line up in Blender at real-world height.
- **Common mistakes:**
  - References at arbitrary sizes, so the model comes out 3 m tall.
  - Front and side images offset vertically by a few centimeters.
- **Claude can help:** through the Blender MCP, Claude can add, scale, and align the reference empties to your exact height, which is quick and precise.
- **Time:** 20 minutes per character.

### Step 13. Records: prompts, AI use, and the legal basics

- **Goal:** you can answer "where did this come from?" for any image, and fill in Steam's AI questions honestly (walkthrough 20).
- **Do this:**
  1. **Prompt logs:** the sidecar files from step 9.
  2. **AI usage log** `docs/art/ai-usage-log.md`: one line per batch. Record the date, tool and model, what it was for, and whether anything from it might ship in the game or its marketing. The Krita plugin writes a metadata tag into images marking them as AI-generated; Google's outputs carry a SynthID watermark and C2PA metadata. Leave those in place.
  3. **Copyright, briefly:**
     - The US Copyright Office's 2025 report says AI output is protectable only where a human determined enough expressive elements, for example through visible human work, creative selection and arrangement, or modification. Prompts alone aren't enough.
     - Your paintovers and hand-made models are your authored work; the raw AI images may not be protected at all.
     - Concept art is internal reference, so that's usually fine. The game itself is built by hand.
  4. **Steam:**
     - Valve rewrote its AI disclosure rules on 2026-01-16. The Content Survey focuses on AI-generated content **that ships with your game and is consumed by players** (art, sound, text), and on anything generated live while the game runs.
     - Press reports say store pages and marketing also need disclosure.
     - Efficiency tools used during development aren't the focus.
     - AI concept art used only as internal reference is probably outside what Steam asks about, but that isn't stated explicitly.

     `VERIFY:` read Valve's current Content Survey text before you fill it in (walkthrough 20), and don't ship raw AI images, including in capsule art or trailers, without deciding how you'll disclose them.
- **Done when:** the logs exist and are up to date for everything made so far.
- **Common mistakes:**
  - Letting an AI image slip into a texture or store asset without noticing.
  - Deleting metadata that marks AI images.
- **Claude can help:** Claude can keep the usage log from your notes, check it against the concept folders, and later draft the Steam survey answers from it (walkthrough 20).
- **Time:** 5 minutes per session, and it saves days later.

---

## Vertical slice checklist

- [ ] `docs/art/style-guide.md` with palette, rules, values, shape language, readability rules, prompt vocabulary, and tool choice
- [ ] Krita 5.3 with the Wraith palette and the paintover template (value and palette check layers)
- [ ] Reference folders and BeeRef boards for architecture, costume, lighting, and snow, with `reference-sources.csv` complete
- [ ] AI tool chosen; local Krita AI Diffusion with FLUX.2 [klein] 4B working, or consciously skipped
- [ ] Lantern Market key frames: street, market square, Vesper arena (palette-checked, approved, JPGs in `docs/art/`)
- [ ] Silhouette sheets pass the 64-pixel test for Wraith, Vesper, and all four archetypes
- [ ] Canon sheets v01+ for Wraith, Vesper, shielded cultist, Choir singer, snuffer, and heavy
- [ ] Turnarounds (front, side, back; A-pose; aligned guides) for Wraith (cloak on and off) and Vesper; simpler ones for the four enemies
- [ ] Lantern sheet with four states, readable at 32 px
- [ ] Kit elevation sheet on the 100 cm grid, matching walkthrough 06's kit rules
- [ ] Vesper arena layout and key frame
- [ ] Turnarounds loaded in Blender at real height for Wraith and Vesper
- [ ] Prompt logs and `docs/art/ai-usage-log.md` up to date

## Going further

- **3D-first concepting** for everything with architecture: kitbash in Blender, render, paint over. It's also great for camera angles in cutscenes (walkthrough 12).
- **AI 3D generation** (for example Hunyuan3D or Rodin through the Blender MCP's integrations, walkthrough 01) for rough proxies only. Their licenses vary, and Hunyuan3D's open license excludes the EU, UK, and South Korea.
- **Commissioning a human concept artist** for Wraith and Vesper's final canon sheets, if budget allows. Give them your style guide and silhouettes.
- **Character LoRAs**, once an AMD-friendly training path on Windows exists, or on a rented cloud GPU.

## References

**Krita and local generation**
- Krita: https://krita.org
- Krita 5.3.0 release notes: https://krita.org/en/posts/2026/krita-5.3.0-released/
- Krita AI Diffusion: https://github.com/Acly/krita-ai-diffusion
- ComfyUI: https://github.com/comfyanonymous/ComfyUI
- ComfyUI system requirements (AMD on Windows): https://github.com/Comfy-Org/docs/blob/main/installation/system_requirements.mdx
- ComfyUI portable for Windows: https://github.com/Comfy-Org/docs/blob/main/installation/comfyui_portable_windows.mdx
- AMD AI Bundle FAQ: https://www.amd.com/en/resources/support-articles/faqs/ai_bundle.html
- AMD ROCm (TheRock) supported GPUs: https://github.com/ROCm/TheRock/blob/main/SUPPORTED_GPUS.md
- FLUX.2 (including [klein]): https://github.com/black-forest-labs/flux2

**Hosted generators**
- Midjourney plans: https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans
- Midjourney terms of service: https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service
- ChatGPT Images 2.5: https://openai.com/index/introducing-chatgpt-images-2-5/
- OpenAI terms of use: https://openai.com/policies/row-terms-of-use/
- Gemini image generation: https://ai.google.dev/gemini-api/docs/image-generation
- Adobe Firefly plans: https://www.adobe.com/products/firefly/plans.html

**Model licenses**
- SDXL license: https://github.com/Stability-AI/generative-models/blob/main/model_licenses/LICENSE-SDXL1.0
- FLUX.1 [dev] license: https://github.com/black-forest-labs/flux/blob/main/model_licenses/LICENSE-FLUX1-dev
- Qwen-Image: https://github.com/QwenLM/Qwen-Image

**Reference boards**
- BeeRef: https://github.com/rbreu/beeref
- PureRef license: https://www.pureref.com/license.php
- Eagle pricing: https://en.eagle.cool/support/article/eagle-pricing

**Blender**
- Empties and reference images: https://docs.blender.org/manual/en/latest/modeling/empties.html

**Legal and Steam**
- US Copyright Office, Copyright and AI, Part 2: https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf
- Steam Content Survey: https://partner.steamgames.com/doc/gettingstarted/contentsurvey

**Learning**
- Krita manual (tools, filters, filter layers, palettes): https://docs.krita.org
- Krita AI Diffusion documentation (installation, control layers, regions): https://github.com/Acly/krita-ai-diffusion/tree/main/docs
