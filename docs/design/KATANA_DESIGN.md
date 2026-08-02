# THE FIVEFOLD BLADE — Ryuma's Signature Katana

> Design spec for the hero weapon: a genuinely beautiful, authentic katana whose **legend reads through restraint, not ornament.** Companion to [CHARACTER_DESIGN.md](CHARACTER_DESIGN.md) §0/§1 (the blade as a living progress bar) and [MAGIC_AND_DEMON.md](MAGIC_AND_DEMON.md) (what it holds).

**Status:** First pass (2026-07-31).

---

## Design philosophy — "overkill through perfection, not clutter"

The blade must look like it can wield **all four elements and the forbidden fifth** — *without* runes, spikes, glowing gems, or fantasy nonsense. The awe comes from:
- **A flawless, authentic katana silhouette** first — correct proportions, an elegant curve, master-forged quality. If the base shape isn't beautiful, no detail saves it.
- **One or two subtle, story-loaded details** that a careful eye reads as *"this is no ordinary steel."*
- **Latent, not active:** at rest it's a quiet masterpiece. The power *sleeps* in it. That restraint is what makes it feel dangerous — and it fits the story (it begins dormant and wakes across the game).

> Rule: if a detail doesn't come from the *forging* or the *story*, it doesn't go on the blade.

---

## The blade, part by part

### The steel & the hamon (this is the signature)
- A superb folded-steel blade with a fine **jihada** (grain) — think top-tier pattern-welded/damascus, but subtle.
- The **hamon** (temper line) is the magic tell: instead of a single tone, it holds a faint **iridescence that shifts through the four elemental hues** as light and angle change — **wind-pale white → water blue-teal → ember gold → storm violet.** At rest it just looks like an impossibly beautiful oil-sheen along the edge; in motion, the four colors flicker across it. *That* is how the eye reads "it holds every element" — no symbols needed.
- Base color of the steel: cool near-white, mirror-polished, so the hues have something to play across.

### The fragment seam (the fifth — the one story detail)
- A single **hairline seam of darker, near-black steel** runs through the blade where the **demon fragment** (the fifth power / bound soul) was fused in — like a healed fracture, elegant, not damage. A faint **warm inner light** lives deep in that seam, barely-there, easy to miss until you're looking.
- This is the *only* overtly "there's something more here" detail — and it's whisper-quiet. It's the mother in the steel. (See [MAGIC_AND_DEMON.md](MAGIC_AND_DEMON.md) §5.)

### The fittings (blackened iron — House Kurogane)
- **Tsuba (guard):** blackened iron, understated, with the **Kurogane crest — a broken blade reforged whole** — subtly worked into it. No filigree overload; clean and heavy.
- **Fuchi/kashira & menuki:** matching dark iron, minimal, premium.
- Everything metal is **Kurogane charcoal/near-black** — the smith-clan's signature.

### The handle (tsuka)
- **Deep charcoal/black silk ito** wrapped in a tight diamond pattern over **black rayskin (same)**.
- A **single crimson accent cord** — Ryuma's signature color (ties to [CHARACTER_DESIGN.md](CHARACTER_DESIGN.md) §1). One accent, not five. Restraint.

### The saya (scabbard)
- Matte black lacquer with the faintest four-hue shimmer in direct light echoing the hamon — so even sheathed, it hints.

---

## Dormant → Awakened (the progression, visually)

The "signature overkill" version above is the **fully-awakened, late-game** blade. Early on it's quieter — the same beautiful steel, powers asleep:
- **Prologue / start:** a superb but *plain* master-forged katana. The hamon is a normal (gorgeous) single tone; the fragment seam is dark and cold; no iridescence. It just looks like an heirloom.
- **Each element awakened** (Wind→Water→Fire→Lightning): that element's hue permanently joins the hamon's shimmer, and a subtle motif etches faintly into the blade near the habaki.
- **The fifth awakened:** the fragment seam warms and begins its faint inner glow.
- By endgame the full iridescent hamon + glowing seam = the signature blade — *earned*, so it never looks gaudy because the player watched it wake.

*(This is the "blade as a living progress bar" from [CHARACTER_DESIGN.md](CHARACTER_DESIGN.md) §0, specced out.)*

---

## Optional name

Nihonto are often named. A restrained, thematic option: **_Goryū_** ("five dragons/currents") — or keep it unnamed and simply "the Fivefold Blade." _[PROPOSED — open.]_

---

## Ready-to-run image prompt (photoreal, your locked look)

> Paste into Flux/your image tool. Portrait or 16:9.

**Full blade hero shot:**
"A single exquisite Japanese katana displayed diagonally, hero product shot, photorealistic, Unreal Engine 5 / octane render quality. A flawless mirror-polished folded-steel blade with a fine damascus grain; the temper line (hamon) shows a subtle shifting iridescence cycling through pale white, blue-teal, ember gold and storm violet like oil-sheen; a single hairline seam of dark near-black steel runs along the blade with a faint warm inner glow. Blackened iron guard (tsuba) with a minimal reforged-blade crest, dark iron fittings, handle wrapped in deep charcoal-black silk over black rayskin with one crimson accent cord. Elegant, restrained, legendary, NOT gaudy, no runes, no gems. Dramatic dark studio lighting, moody rim light, shallow depth of field, ultra-detailed, 8k. NOT anime, NOT cartoon."

**Close-up detail shot (hamon + seam):** same description, "extreme macro close-up of the blade surface showing the iridescent hamon and the glowing dark fragment seam, cinematic."

---

## For the 3D build
When you model this (see [../build/MASTER_ROADMAP.md](../build/MASTER_ROADMAP.md) Phase 2), the shape is a normal katana — the "magic" is **all in the materials**, not the geometry:
- Model a clean, beautiful katana.
- The iridescent hamon = a subtle **iridescent/color-shift material** along the edge (fresnel-driven color).
- The fragment seam = a thin dark material strip with faint emissive.
- Fittings = dark metal PBR; cord = crimson cloth.
- Build the **dormant** material first; the awakened hues turn on via material parameters as the story progresses — clean to drive from Blueprints later.
