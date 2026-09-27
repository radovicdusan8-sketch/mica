# 07. Lighting and Rendering

> **Written for:** Unreal Engine 5.8 (5.8.3): Lumen with hardware or software ray tracing, MegaLights (production-ready in 5.8), Virtual Shadow Maps, Substrate, and TSR. The AMD FSR plugin for UE 5.8 (FidelityFX SDK 2.3: FSR 4.1.1 upscaling and ML frame generation 4.0.1). DaVinci Resolve (free) for grading. Repo tools `tools/art/lut_tool.py` and `tools/art/palette_ratio.py`.
> **Facts checked:** 2026-09-27. Epic's and AMD's sites were blocked from this environment, so their facts come from search excerpts of official pages and from AMD's and Intel's GitHub repositories. Unconfirmed items are marked `VERIFY:`.

## What this covers

This walkthrough lights Wraith's night scenes:

- the project's rendering settings: Lumen, hardware ray tracing on the RX 9060 XT, and MegaLights for many lanterns;
- exposure locked so darkness stays dark;
- the moon and sky;
- lantern lights in Lantern gold;
- violet spirit accents that obey the palette rules;
- lantern glow in volumetric fog;
- post-processing, and color grading to the README palette with a LUT made in DaVinci Resolve;
- upscaling with TSR or AMD FSR instead of DLSS;
- scalability presets for weaker PCs.

The running example is the Lantern Market and the Vesper arena.

## Why it matters for Wraith

- **Light is a game mechanic.** Lanterns make areas safe, and where they go out the dead rise (walkthrough 10). The player must read "lit" versus "dark" instantly. Unreal's automatic exposure is designed to brighten dark scenes, which would quietly erase that difference, so it gets locked.
- **The palette lives in the lights.** Most of the 20% Lantern gold and 10% Spirit violet on screen comes from light color and emissive glow. "Warm light means the living, violet means the dead" is a lighting rule before it's a texture rule.
- **Many small shadowed lights.** A market street can hold dozens of lanterns. MegaLights is built for large numbers of shadowed lights, and it's production-ready in 5.8.
- **Fights must read in the dark.** Characters must read by silhouette (README), so arenas are lit to separate enemies from the background.
- **AMD hardware.** DLSS is NVIDIA-only. Your upscalers are TSR (built in) and AMD FSR 4, which runs on RDNA 4.
- **Budget.** Lighting and fog are this game's biggest GPU costs. Choices made here decide much of walkthrough 17.

## Tools

| Tool | What it's for | Cost | Commercial license OK? | AMD notes |
|---|---|---|---|---|
| Unreal Engine 5.8: Lumen, MegaLights, Virtual Shadow Maps, TSR | Lighting, shadows, anti-aliasing and upscaling | Free (engine royalty terms in walkthrough 01) | Yes | Hardware ray tracing needs an RX 6000 series or newer; the RX 9060 XT qualifies. A forum thread from the 5.6 era reported crashes with hardware ray tracing on RX 90xx cards. Keep the driver current and test (step 1). |
| AMD FSR plugin for Unreal (FidelityFX SDK 2.3) | Upscaling (FSR 4 on RDNA 3 and 4, FSR 3 fallback elsewhere); optional frame generation | Free; about a 1.9 GB download | `VERIFY:` the plugin's license text in the download | Built for AMD: FSR 4 machine-learning upscaling runs on your card |
| Intel XeSS plugin (optional) | A second upscaler option for players | Free | `VERIFY:` license in the repo | XeSS upscaling runs on any GPU with Shader Model 6.4 (DP4a), including AMD |
| NVIDIA DLSS | — | — | — | **NVIDIA-only.** It can't run on your PC, so you can't test it. Skip it for now. |
| DaVinci Resolve (free version) | Grading screenshots and exporting a `.cube` LUT | Free; the paid Studio version isn't needed | Yes. `VERIFY:` Blackmagic's current terms for the free version | `VERIFY:` AMD GPU support on Windows in the current version |
| `tools/art/lut_tool.py`, `tools/art/palette_ratio.py` | Converting `.cube` to Unreal's LUT format; checking the 70/20/10 ratio | Free (in this repo; need Python and Pillow) | Yes | None |

## Before you start

- **Walkthroughs done:** 01. **Useful first:** 06 (a street section built from the kit, with materials, and fog), 03 (the Lantern Market key frames as lighting targets).
- **Read ahead:** 10's lantern states (lit, dimming, snuffed). This walkthrough sets how each state looks; walkthrough 10 builds the logic.
- **Install Python's Pillow** for the tools: `pip install pillow`.
- **Physical light units, briefly.** Unreal can use real-world units:
  - **lux** for sun and moon (directional lights);
  - **candela** for point and spot lights (how bright a light looks from one direction);
  - **EV100** for exposure (the camera's brightness setting, like a photographer's exposure value).

  Using real units makes lights behave predictably together; you then tune by eye.

---

## Steps

### Step 1. Set the project's rendering features

- **Goal:** the project uses Lumen, hardware ray tracing (if stable on your card), MegaLights, Virtual Shadow Maps, Substrate, and TSR.
- **Do this:** open **Edit > Project Settings > Engine > Rendering** and check or set:
  1. **Dynamic Global Illumination Method: Lumen** and **Reflection Method: Lumen**. These are the defaults in new projects.
  2. **Shadow Map Method: Virtual Shadow Maps.** This is the default.
  3. **Hardware Ray Tracing > Support Hardware Ray Tracing:** on. The editor also asks to enable **Support Compute Skin Cache**; accept, and restart.
  4. **Lumen > Use Hardware Ray Tracing when available:** on. Hardware ray tracing is higher quality but costs more. Software ray tracing is Lumen's fastest mode and the fallback; it needs **Generate Mesh Distance Fields** (on by default) and Shader Model 6.
  5. **Direct Lighting > MegaLights:** on. It's production-ready in 5.8. Hardware ray tracing is recommended for it, but not required.
  6. **Anti-Aliasing Method: Temporal Super-Resolution (TSR).** This is the default.
  7. **Default Settings > Extend default luminance range in Auto Exposure settings:** make sure it's on. It makes exposure settings use EV100, which step 3 relies on. `VERIFY:` its default in 5.8.
  8. **Substrate** is already on in new 5.8 projects (walkthrough 06).

  Tip: hover over any setting to see the console variable behind it. Those are the names to use if Claude edits `WraithGame/Config/DefaultEngine.ini` for you.
- **Stability check on the RX 9060 XT.** After enabling hardware ray tracing, open your busiest test map and fly around for 10 minutes. If the editor crashes or shows corrupted lighting:
  1. update the AMD driver;
  2. if that doesn't help, switch **Use Hardware Ray Tracing when available** off (software Lumen);
  3. write down which driver and engine versions misbehaved.
- **Done when:**
  - the settings are saved and the editor restarts cleanly;
  - **View Mode > Lumen > Overview** shows Lumen working;
  - the 10-minute stability test passes.
- **Common mistakes:**
  - Turning features on without restarting.
  - Assuming hardware ray tracing is always better. Measure both in step 13 and keep the faster one that looks acceptable.
- **Claude can help:** Claude can make these changes in `Config/DefaultEngine.ini` and show you the diff, if you give it the console-variable names from the tooltips. It can't see the editor to confirm them; you check after the restart.
- **Time:** 30 minutes, plus the stability test.

### Step 2. Build a look-development map

A **look-development (lookdev) map** is a small test scene where you decide how things should look, before applying those decisions to real levels.

- **Goal:** one small, repeatable place to make every lighting decision.
- **Do this:**
  1. Create `/Game/Wraith/Dev/L_LookDev_Night` with:
     - a 20 m street section built from the kit (walkthrough 06), with snow and stone materials;
     - two lanterns;
     - the template character (later Wraith and an enemy);
     - a placeholder "spirit" (a sphere with a violet emissive material);
     - one covered area.
  2. Add a **Post Process Volume** with **Infinite Extent (Unbound)** turned on, so it affects the whole map.
  3. Put the Lantern Market key frames from walkthrough 03 on flat planes behind the camera's start position, with an **unlit** material, so you can compare the render to the target at a glance.
  4. Add a small row of reference spheres on a pedestal: dark stone, snow-white (albedo about 0.8), and a mid-gray. They show exposure problems immediately.
- **Done when:** the map loads in seconds and contains every element you'll light.
- **Common mistakes:** doing lookdev in the full level, where every change is slow and many things change at once.
- **Claude can help:** through the Unreal MCP, Claude can assemble the map from a list: place the kit pieces, lanterns, spheres, and the Post Process Volume.
- **Time:** 1 hour.

### Step 3. Lock exposure so darkness stays dark

**Exposure** is how bright the camera makes the scene. Unreal's default **auto exposure** (eye adaptation) brightens dark scenes, like your eyes do at night. For Wraith that's a problem: dark zones would slowly brighten until they no longer read as dangerous.

- **Goal:** a fixed exposure per area, so lit and dark read the same way every time.
- **Do this:**
  1. In the unbound Post Process Volume, go to **Exposure** and set **Metering Mode: Auto Exposure Histogram**.
  2. Set **Min EV100** and **Max EV100** to the **same value**. Equal values mean the exposure can't adapt. Start at **EV100 = 2** and set **Exposure Compensation** to 0.

     Where that number comes from: a stone surface lit to about 5 lux by a lantern, with 30% reflectance, has a luminance of about 0.48 cd/m². That's roughly EV100 2 in the standard exposure formula. It's a starting point, not a rule.
  3. Tune by eye against your key frames, but change **lights**, not exposure, to fix most problems. Keep exposure the same across the whole outdoor district.
  4. For interiors or special spaces (the covered market, the Vesper arena), add a bounded Post Process Volume with its own locked EV100 and a **Blend Radius** of a few meters, so the change is smooth.
  5. **Dark zones never get brighter exposure.** Players see in them through fog and silhouettes (step 7), Wraith's own violet glow, and enemies' emissive details.
- **Done when:** walking between lit and dark areas doesn't change the brightness of the lit areas. The reference spheres look the same in every lit area of the lookdev map.
- **Common mistakes:**
  - Leaving auto exposure on and wondering why dark zones "wash out" after a second.
  - Fixing a too-dark scene by raising exposure. That lifts everything, including the darkness you need. Add or brighten lights instead.
- **Claude can help:** Claude can set Post Process Volume values through the Unreal MCP and keep a table of the chosen EV100 per area in `docs/design/lighting.md`.
- **Time:** 30 minutes, then ongoing.

### Step 4. The moon and the sky

- **Goal:** a very dark sky (Grave `#0B090C` in the palette means "night sky, deep shadow"), with just enough cold moonlight to read shapes.
- **Do this:**
  1. **Directional Light** (the moon):
     - Intensity: start around 0.5–2 lux. Real moonlight is much dimmer, but game nights are artistically brighter so players can see.
     - Color: a pale, cool, desaturated tint.
     - A low angle, so buildings throw long shadows.
     - Cast Shadows on.
  2. **Sky Light:**
     - **Real Time Capture** on.
     - A low intensity that lifts shadows only slightly.
     - **Lower Hemisphere Is Solid Color** set to near-black, so the ground doesn't glow from below.
  3. **Sky:** either a Sky Atmosphere with the moon as its atmosphere light, or a simple dark sky-sphere material with faint stars. Fog and snow hide most of the sky, so keep it cheap.
  4. Check the snow sphere: in pure moonlight it should read as dim, cold gray-blue, clearly darker than anything a lantern touches.
- **Done when:** with all lanterns off, the lookdev street is dark and cold, but you can still see the shapes of buildings and the character.
- **Common mistakes:** moonlight bright enough to compete with lanterns. The moon is there to show shapes, not to light the scene.
- **Claude can help:** Claude can set these values through the Unreal MCP and take screenshots for comparison.
- **Time:** 30 minutes.

### Step 5. Lantern lights

- **Goal:** a reusable lantern light setup that looks right, casts soft shadows, glows in fog, and stays cheap even with dozens of lanterns.
- **Do this:** set the Point Light inside your lantern Blueprint (the lantern's gameplay comes in walkthrough 10) to these starting values:

  | Setting | Starting value | Why |
  |---|---|---|
  | Intensity Units | Candela | Physical units, predictable with locked exposure |
  | Intensity | 20 cd | A small flame lantern; tune by eye |
  | Light Color | `E0A24A` in the color picker's **Hex sRGB** field | Exactly Lantern gold; the picker also has a linear hex field, so use the sRGB one |
  | Use Inverse Squared Falloff | On | Physical falloff |
  | Attenuation Radius | 800–1200 cm | Small pools of light make lit and dark zones readable, and limit overlap (cheaper and less noisy) |
  | Source Radius | 3–5 cm | Soft, believable shadow edges |
  | Cast Shadows / Cast Volumetric Shadow | On / On | Shadows are what make lanterns feel real |
  | Volumetric Scattering Intensity | 1–4 | The halo in fog (step 7) |
  | MegaLights Shadow Method | Ray Tracing (the default) | Fixed cost per light. The Virtual Shadow Map option costs significantly more per light. |

  Then:
  1. **Glass.** The lantern glass's emissive material (walkthrough 06) should look like the source of the light, but it isn't what lights the scene. Lumen treats small, bright emissive surfaces as a noisy light source, so real lights do the lighting and emissives only glow.
  2. **Flicker.** A slow, subtle intensity variation (±5–10%) sells a flame. Drive it from the lantern's code (walkthrough 10) with a shared noise curve, updated about 10–20 times a second, not every frame. Don't use light functions for flicker: they aren't supported in volumetric fog for point and spot lights, so the halo wouldn't flicker. `VERIFY:` this limit is from an older version of Epic's volumetric fog page.
  3. **States for walkthrough 10.** Save three presets:
     - **Lit:** the values above.
     - **Dimming:** intensity falling over a few seconds, with the color shifting slightly deeper toward red-orange.
     - **Snuffed:** light off, glass emissive near black.
  4. **Many lanterns.** MegaLights cost stays roughly constant as you add lights, but noise grows when many lights overlap one pixel. A strong light hidden behind a wall can still "steal" samples. Keep radii tight, and don't stack lanterns close together.
- **Done when:** a street with 10–20 lanterns looks right, the halos show in fog, and `stat gpu` shows no large cost jump from adding lanterns.
- **Common mistakes:**
  - Huge attenuation radii. They blur the lit/dark boundary that gameplay depends on, and they add noise.
  - Very bright emissive glass used as the light source.
  - Every lantern ticking its own flicker every frame.
- **Claude can help:** Claude can apply a preset to every lantern in a level at once through the Unreal MCP, and write the flicker and state code in walkthrough 10.
- **Time:** 1 hour.

### Step 6. Violet accents for the dead

The rule: violet belongs to the dead (spirits, Wraith's powers, violet cracks), and must never fall on anything living.

- **Goal:** violet appears exactly where the art rules say, and never spills onto living characters.
- **Do this:**
  1. Make most violet **emissive, not light**: Wraith's powers, cracks, spirit forms, and the eyes and runes of dead enemies. The VFX come in walkthrough 14. Emissive glows in fog and bloom without lighting nearby living things.
  2. Where a real violet light is needed (a spirit hovering in a dark alley):
     - `9B6BFF` in the **Hex sRGB** field;
     - a small attenuation radius (100–300 cm) and low intensity;
     - shadows off for small ones;
     - never next to a living character.
  3. **Niagara lights:** a particle system can emit lights from its Light Renderer. Enable **Allow Mega Lights** there, keep particle lights few and small, and let only a handful cast shadows.
  4. **Wraith is readable in darkness** because of his own faint violet glow. That's allowed, because Wraith is dead. Make it subtle and constant, so the player always sees their character in dark zones without brightening the zone.
- **Done when:**
  - in the lookdev map, violet only appears on dead things;
  - a living character standing next to the spirit placeholder shows no violet light on them;
  - Wraith stays visible in a dark zone.
- **Common mistakes:**
  - Violet fill lights for "mood" that tint everything, which breaks the palette rule.
  - Too much violet overall. It's 10% of the frame, not 30%.
- **Claude can help:** Claude can audit a level through the Unreal MCP: list every light with a violet-ish color, and flag any whose radius reaches a living character's spawn point or path.
- **Time:** 30–60 minutes.

### Step 7. Lantern glow in volumetric fog, and readable silhouettes

- **Goal:** light hangs in the air around lanterns, and enemies stand out as dark shapes against it.
- **Do this:**
  1. With walkthrough 06's Exponential Height Fog and **Volumetric Fog** on, keep the global fog density low and raise **Volumetric Scattering Intensity** on individual lights instead. Epic's guidance is exactly this: low global density, stronger per-light scattering.
  2. **Scattering Distribution** around 0.2–0.6 gives halos that brighten when you look toward a lantern.
  3. **Backlight the arenas:** place a lantern or two behind the far side of each arena, from the player's usual camera direction. Enemies between the camera and the lit fog become readable silhouettes, which is exactly the README's rule.
  4. Check cost: volumetric fog resolution is set by `r.VolumetricFog.GridPixelSize` and `r.VolumetricFog.GridSizeZ`. Leave the defaults for now; step 12 lowers them on low settings. `VERIFY:` the default values in your engine's `Engine/Config/BaseScalability.ini`.
- **Done when:** in every arena, from the usual camera angle, enemies read as clear silhouettes against glowing fog.
- **Common mistakes:**
  - Raising fog density to get more glow, which hides enemies.
  - Relying on IES light profiles for fog shapes; they may not affect volumetric fog.
- **Claude can help:** Claude can set scattering values in bulk and take comparison screenshots through the MCP.
- **Time:** 1 hour per arena, spread over the art pass.

### Step 8. Lumen settings for night

- **Goal:** clean indirect light at a sane cost, with darkness preserved.
- **Do this:** in the unbound Post Process Volume's **Lumen Global Illumination** section:
  1. **Final Gather Quality:** start at the default. Raise it only if you see blotchy noise in dark corners near lanterns; higher values greatly increase GPU cost.
  2. **Lumen Scene Lighting Quality** and **Lumen Scene Detail:** start at the defaults.
  3. **Skylight Leaking:** keep it at 0 outdoors so darkness stays dark. In the covered market's own volume, a small value keeps corners from turning pure black. It's a non-physical art control, which is fine.
  4. Look at **View Mode > Lumen > Lumen Scene** to see what Lumen "sees". Small meshes are culled from the Lumen Scene, which is another reason small emissive glass shouldn't be your light source.
  5. **Lumen Lite**, new in 5.8, is a cheaper, medium-quality GI mode. Epic says it's about twice as fast as Lumen High, it's the default on current handhelds, and it's supported on PC. It's a candidate for your Low and Medium settings (step 12). `VERIFY:` how to enable it and its console variable.
- **Done when:** the lookdev street has no distracting GI noise at your target settings, and `stat gpu` shows Lumen's cost.
- **Common mistakes:** maxing every quality slider "because the RX 9060 XT can take it". Walkthrough 17 needs that headroom for fights with many enemies and effects.
- **Claude can help:** Claude can set values and read back `stat gpu` output that you paste in, then suggest what to try next.
- **Time:** 30–60 minutes.

### Step 9. Post-processing: the base look

- **Goal:** restrained post-processing that supports readability in fights.
- **Do this:** in the unbound Post Process Volume, start from these values:

  | Setting | Starting point | Reason |
  |---|---|---|
  | Bloom | Standard method, low intensity | Lanterns glow without smearing the frame |
  | Lens Flares | Off | Distracting in combat |
  | Vignette | 0.3–0.4 | Frames the action and darkens the corners |
  | Film Grain | Very subtle | Hides banding in dark gradients; too much reads as noise |
  | Chromatic Aberration | 0 | Blurs silhouettes |
  | Motion Blur | Low, and a player toggle later (walkthrough 13) | Fast combat plus heavy blur is unreadable, and some players get motion sick |
  | Local Exposure | A slightly lower Highlight Contrast | Keeps lantern hotspots from burning out while shadows stay deep. `VERIFY:` the exact setting names in 5.8. |
  | Depth of Field | Off in gameplay | Cutscenes use it (walkthrough 12) |

- **Done when:** the lookdev screenshot looks close to your key frame in contrast and mood, before any color grading.
- **Common mistakes:** stacking effects to get a "cinematic" look. Grading (step 10) does that job better, without hurting readability.
- **Claude can help:** Claude can apply the table through the Unreal MCP and keep the values in `docs/design/lighting.md`.
- **Time:** 30 minutes.

### Step 10. Grade to the palette with a LUT

A **LUT (lookup table)** is a color-remapping table. Unreal applies a 256 × 16 LUT texture as the last color step. You can grade screenshots in a real grading tool and bring the result back as a LUT.

- **Goal:** the final frame matches the README palette and your key frames, and `palette_ratio.py` confirms roughly 70/20/10.
- **Do this:**
  1. **Small in-engine adjustments first**, in the Post Process Volume's **Color Grading** section:
     - global saturation slightly below 1;
     - shadows nudged toward cold slate;
     - highlights nudged slightly warm.

     Small moves only; the palette mostly comes from materials and lights.
  2. **Take reference screenshots.** In each key view, open the console and type `HighResShot 1`. The screenshots go to `WraithGame/Saved/Screenshots/`. Take 3–5 views: a lit street, a dark zone, the Vesper arena, and a character close-up.
  3. **Grade in DaVinci Resolve** (free):
     - Import the screenshots.
     - Grade them together on the Color page with lift, gamma, gain, curves, and hue-versus-saturation, comparing against the key frames.
     - Use **only global color operations**. Windows, masks, qualifiers, blur, and vignettes can't be represented in a LUT.
  4. **Export a LUT:**
     - Right-click the graded clip on the Color page and choose **Generate LUT > 33 Point Cube**.
     - Save it as `source-art/lighting/Grade_Wraith_v01.cube`.

     `VERIFY:` the menu wording in your Resolve version.
  5. **Convert it** with the repo tool:
     ```powershell
     python tools/art/lut_tool.py from-cube source-art/lighting/Grade_Wraith_v01.cube source-art/lighting/T_LUT_Wraith_v01.png
     ```
     `python tools/art/lut_tool.py neutral LUT_Neutral.png` writes the identity LUT if you ever need to start over. The tool is tested: an identity `.cube` reproduces the neutral LUT exactly.
  6. **Import** `T_LUT_Wraith_v01.png` into `/Game/Wraith/Environments/Shared/Lighting/`. In the texture's settings, set **Texture Group (LOD Group)** to **ColorLookupTable**, which is Epic's documented setting for LUTs. `VERIFY:` also no mipmaps and uncompressed, if the group doesn't already set that.
  7. In the Post Process Volume, set **Color Grading > Misc > Color Grading LUT** to the texture, with intensity 1.
  8. **Check the ratio** on fresh screenshots of each key view:
     ```powershell
     python tools/art/palette_ratio.py WraithGame/Saved/Screenshots/WindowsEditor/HighresScreenshot00000.png --mask ratio_mask.png
     ```
     Look at the mask image. Gold should sit on lanterns and living things, violet on the dead, and nearly everything else should be dark base. `VERIFY:` the screenshot file names and folder on your machine.
- **Done when:** the graded key views sit near 70/20/10, they match your key frames, and dark zones still read as dangerous.
- **Common mistakes:**
  - Grading to fix bad lighting. If the ratio is off by a lot, fix lights and materials first.
  - Exporting a LUT from a grade that uses windows or qualifiers. They silently don't carry over.
  - Forgetting the LUT texture's group setting, which gives banding or wrong colors.
- **Claude can help:** Claude runs both tools, reads the mask images (it can view PNGs), and suggests which lights or materials push the ratio off. Grading in Resolve is yours.
- **Time:** 1–2 sessions.

### Step 11. Upscaling: TSR and FSR, not DLSS

**Upscaling** renders at a lower resolution and reconstructs a sharp full-resolution image. It's one of the biggest performance levers you have.

- **Goal:** TSR as the default, AMD FSR 4 as an option, and a clear plan for other vendors.
- **Do this:**
  1. **TSR (default):**
     - TSR is designed for 25–200% screen percentage.
     - Epic says it gets close to native 4K from a 1080p input (50%).
     - Starting points: about 67% for 1440p output, 50% for 4K, and 75–100% for 1080p.
     - Set it with `r.ScreenPercentage` for testing. The settings menu exposes it later (walkthrough 13).

     `VERIFY:` Epic's screen-percentage mode settings in 5.8.
  2. **Install the AMD FSR plugin** (based on AMD's plugin README):
     1. Download the Unreal plugin from GPUOpen: https://gpuopen.com/learn/ue-fsr/ (about 1.9 GB; it covers UE 5.3–5.8).
     2. Extract it, take the folder for 5.8, and copy its `FSR` folder into `C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Marketplace\`. That needs administrator rights.
     3. In the editor, go to **Edit > Plugins**, enable **FSR**, and restart.
     4. FSR needs TSR as the anti-aliasing method and temporal upsampling on (`r.AntiAliasingMethod 4`, `r.TemporalAA.Upsampling 1`).
     5. Turn it on under **Project Settings > FSR Upscaling > Enabled**, or with `r.FidelityFX.FSR.Enabled 1`.
     6. Choose the quality mode with `r.FidelityFX.FSR.QualityMode`:
        - 0: Native AA
        - 1: Quality (1.5×)
        - 2: Balanced (1.7×)
        - 3: Performance (2×)
        - 4: Ultra Performance (3×)

        It overrides `r.ScreenPercentage`.
     7. Optional sharpening: `r.FidelityFX.FSR.Sharpness` (default 0).

     On your RX 9060 XT the plugin uses **FSR 4** (machine-learning upscaling); on other cards it falls back to FSR 3.

     Record this install in `CLAUDE.md`'s setup notes. Plugins in the engine folder aren't in your repo, so a new PC needs them installed again. `VERIFY:` whether the plugin also works from the project's `Plugins/` folder, which would keep it in the repo.
  3. **Frame generation** creates extra in-between frames:
     - Turn it on with `r.FidelityFX.FI.Enabled 1`, plus the swapchain override the plugin describes.
     - ML frame generation needs an RX 9000 card and Windows 11. AMD measures its cost at about 2.1 ms at 1440p on an RX 9060 XT.
     - It adds input latency, which matters in a timing-based brawler. **Keep it off by default** and offer it as an option. Pair it with the Anti-Lag 2 plugin if you ship it.
  4. **Other vendors:**
     - **Intel XeSS** runs on AMD cards too, via its plugin (`r.XeSS.Enabled`). One of its components had a problem on 5.8.0–5.8.1, fixed in 5.8.2 and later.
     - **DLSS** can't be tested on your PC; consider it later with a tester who owns an NVIDIA card (walkthroughs 17 and 20).
     - **Enable only one third-party upscaler at a time.**
- **Done when:** you can switch between TSR and FSR in a packaged test build, both look acceptable at your target resolution, and you've written down the frame times for each (walkthrough 17 formalizes this).
- **Common mistakes:**
  - Installing FSR before setting TSR as the anti-aliasing method.
  - Two upscalers enabled at once.
  - Turning frame generation on and judging combat feel with it.
  - Forgetting the plugin on a new PC, after which the project won't open with FSR enabled.
- **Claude can help:** Claude can set and toggle the console variables, write a small debug menu or console command to switch upscalers, and record measurements. Downloading and copying the plugin into Program Files is yours.
- **Time:** 1 hour.

### Step 12. Scalability presets for weaker PCs

**Scalability** is Unreal's system of quality levels: Low (0), Medium (1), High (2), Epic (3), and Cinematic (4). The levels are grouped into categories that the settings menu exposes: view distance, anti-aliasing, shadows, global illumination, reflections, post-processing, textures, effects, foliage, and shading. They're the `sg.*` console variables, such as `sg.ShadowQuality 2`.

- **Goal:** each quality level looks like Wraith and runs well. Low must still keep lit versus dark readable.
- **Do this:**
  1. **Read Epic's defaults** in `C:\Program Files\Epic Games\UE_5.8\Engine\Config\BaseScalability.ini`. It's a reference only; never edit engine files.
  2. **Override only what you change**, in `WraithGame/Config/DefaultScalability.ini`, using the same section names. For example:
     ```ini
     ; WraithGame/Config/DefaultScalability.ini
     ; Only list what you change; everything else comes from BaseScalability.ini.
     ; Before adding a variable, search BaseScalability.ini for it. If Epic sets it in a
     ; different group, set yours in that same group, or the two will fight.

     [ShadowQuality@0]
     r.MegaLights.Allow=0

     [EffectsQuality@0]
     r.VolumetricFog=0

     [EffectsQuality@1]
     r.VolumetricFog.GridPixelSize=16
     ```
     `VERIFY:` which groups Epic's file uses for these variables, and pick values from your own measurements in walkthrough 17. On the lowest level, turning MegaLights off means lanterns fall back to standard lights, so check that lit versus dark still reads.
  3. **Candidates for Low and Medium:** Lumen Lite instead of full Lumen (step 8), lower volumetric fog resolution, fewer shadow-casting lanterns, lower screen percentage with TSR or FSR, and fewer snow particles (walkthrough 06).
  4. **In the game,** the settings menu (walkthrough 13) calls `UGameUserSettings`. It has functions to set the overall scalability level and to run a hardware benchmark that picks a starting level; walkthrough 13 wires them up.
  5. **Test each level** on your PC with `sg.*` commands in a packaged build, in the busiest fight of the Lantern Market. The editor's **Settings > Engine Scalability Settings** only changes the editor viewport.
- **Done when:** all four levels are playable, each has recorded frame times (walkthrough 17), and Low still shows clear lantern pools and dark zones.
- **Common mistakes:**
  - Copying all of BaseScalability.ini into your project, so you stop receiving engine fixes.
  - Setting the same variable in two groups.
  - Letting Low become flat and bright, which breaks the core mechanic's readability.
- **Claude can help:** Claude can search BaseScalability.ini, write the override file, and explain each variable. You run the tests and paste the numbers.
- **Time:** 1–2 sessions, repeated in walkthrough 17.

### Step 13. Light the Lantern Market and the Vesper arena

- **Goal:** the real level, lit to the lookdev standard, on palette and on budget.
- **Do this, in this order:**
  1. Lock exposure (step 3).
  2. Moon and sky (step 4).
  3. Lanterns at the blockout's marked positions, which are walkthrough 10's gameplay positions (step 5).
  4. Fog glow and backlighting in every arena (step 7).
  5. Violet accents on the dead (step 6).
  6. Local Post Process Volumes for the covered market and the Vesper arena, each with locked exposure and a blend radius.
  7. The base post-processing and LUT (steps 9–10).
  8. Palette check on three key views with `palette_ratio.py`.
  9. **Hardware vs. software Lumen:** measure `stat gpu` in the busiest fight with each, and keep the faster one that looks acceptable. Write both results in `docs/design/lighting.md`.
  10. **Darkness playtest.** Can a first-time player see enemies in dark zones, and tell lit from dark instantly? If not, change fog and backlighting, not exposure.
- **Done when:** the level matches the key frames, passes the palette check and the darkness playtest, and its GPU cost is recorded.
- **Common mistakes:**
  - Lighting before the blockout is final, so you relight after every layout change.
  - Each area getting its own look until the district feels like five different games. Keep one exposure, one LUT, and local volumes only where they're needed.
- **Claude can help:** Claude can place and configure lanterns from the blockout markers through the Unreal MCP, run the palette checks, and keep `docs/design/lighting.md` current.
- **Time:** 2–4 sessions.

---

## Vertical slice checklist

- [ ] Rendering features set: Lumen (hardware ray tracing if stable), MegaLights, Virtual Shadow Maps, Substrate, TSR; 10-minute stability test passed on the RX 9060 XT
- [ ] `L_LookDev_Night` with kit street, lanterns, reference spheres, spirit placeholder, and key frames on planes
- [ ] Exposure locked (Min EV100 = Max EV100) outdoors, with bounded volumes for the covered market and the Vesper arena
- [ ] Moonlight and dark sky set; the street is readable but dark with lanterns off
- [ ] Lantern light preset (Lit, Dimming, Snuffed) in Lantern gold `E0A24A`, candela units, tight radius
- [ ] Violet only on the dead; Wraith's subtle glow keeps him visible in dark zones
- [ ] Lantern halos in volumetric fog; every arena backlit so enemies read as silhouettes
- [ ] Post-processing base look (table in step 9) applied
- [ ] `T_LUT_Wraith_v01` graded in Resolve, converted with `lut_tool.py`, applied; key views near 70/20/10 with `palette_ratio.py`
- [ ] TSR default; FSR plugin installed and tested; frame generation off by default; the engine-folder plugin noted in `CLAUDE.md`
- [ ] `DefaultScalability.ini` with tested Low, Medium, High, and Epic; Low keeps lit and dark readable
- [ ] Lantern Market and Vesper arena lit, palette-checked, and darkness-playtested; hardware vs. software Lumen costs recorded in `docs/design/lighting.md`

## Going further

- **MegaLights debug views** (new in 5.8) show where lights overlap and steal samples. Use them to tidy lantern placement.
- **Per-area weather and lighting presets:** store Post Process Volume and fog values per district in Data Assets, so later districts start from a tested look.
- **Cinematic lighting** for cutscenes (walkthrough 12): extra lights that only exist in a sequence, and depth of field.
- **HDR output** for players with HDR displays. Test it once the SDR look is locked.
- **DLSS** for NVIDIA players, only if you have someone to test it.

## References

**Epic Games** (5.8 documentation)
- Lumen technical details: https://dev.epicgames.com/documentation/unreal-engine/lumen-technical-details-in-unreal-engine
- Lumen global illumination and reflections: https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
- Lumen performance guide: https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-performance-guide-for-unreal-engine
- Hardware ray tracing: https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-ray-tracing-in-unreal-engine
- MegaLights: https://dev.epicgames.com/documentation/en-us/unreal-engine/megalights-in-unreal-engine
- Physical lighting units: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-physical-lighting-units-in-unreal-engine
- Auto exposure: https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-exposure-in-unreal-engine
- Emissive materials: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-emissive-material-input-in-unreal-engine
- Volumetric fog: https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-fog-in-unreal-engine
- Local Fog Volumes: https://dev.epicgames.com/documentation/en-us/unreal-engine/local-fog-volumes-in-unreal-engine
- Color grading and the filmic tonemapper: https://dev.epicgames.com/documentation/en-us/unreal-engine/color-grading-and-the-filmic-tonemapper-in-unreal-engine
- Lookup tables for color grading: https://dev.epicgames.com/documentation/unreal-engine/using-lookup-tables-for-color-grading-in-unreal-engine
- Post-process effects: https://dev.epicgames.com/documentation/en-us/unreal-engine/post-process-effects-in-unreal-engine
- Temporal Super Resolution: https://dev.epicgames.com/documentation/en-us/unreal-engine/temporal-super-resolution-in-unreal-engine
- Screen percentage with temporal upscale: https://dev.epicgames.com/documentation/en-us/unreal-engine/screen-percentage-with-temporal-upscale-in-unreal-engine
- Scalability reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-reference-for-unreal-engine
- Scalability and device profiles in Lyra: https://dev.epicgames.com/documentation/unreal-engine/scalability-and-device-profiles-in-lyra-sample-game-for-unreal-engine
- Unreal Engine 5.8 release notes: https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes

**AMD and Intel**
- FSR plugin for Unreal Engine: https://gpuopen.com/learn/ue-fsr/
- FSR plugin update for UE 5.8: https://gpuopen.com/learn/amd-fsr-plugin-updated-for-unreal-engine-58/
- FidelityFX SDK (FSR 4, frame generation): https://github.com/GPUOpen-LibrariesAndSDKs/FidelityFX-SDK
- Anti-Lag 2 SDK: https://github.com/GPUOpen-LibrariesAndSDKs/AntiLag2-SDK
- Intel XeSS plugin for Unreal: https://github.com/GameTechDev/XeSSUnrealPlugin

**Grading**
- DaVinci Resolve: https://www.blackmagicdesign.com/products/davinciresolve

**Recommended learning channels**
- Unreal Engine on YouTube (official; Lumen and MegaLights talks): https://www.youtube.com/@UnrealEngine
- Epic Developer Community learning library: https://dev.epicgames.com/community/unreal-engine/learning
