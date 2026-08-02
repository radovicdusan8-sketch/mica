# CHARACTER DESIGN — Severed Blade

> Concrete design for the cast: silhouette, face, costume, palette, weapon, fighting style, personality/voice, arc, and a signature image — enough to feed concept art and the Blender/UE character pipeline. Built on the [Story Bible](STORY_BIBLE.md) §5/§5b/§10.

**Status:** First design pass (2026-07-31). Leads (Ryuma, Sadao, Kaito, Hidetora, Kaede) in full depth; supporting cast in solid blocks. Iterating outward.

**Art direction (locked):** characters are **grounded and realistic — AAA, Nioh / Ghost of Tsushima**, dropped into a painterly, stylized world. Real fabric, real weight, real faces. No stylized proportions on the people.

---

## 0. The Visual Language of the Clans *(shared reference)*

Every costume, crest, and palette should tell the player *which power and which allegiance* they're looking at, at a glance. Elements read as color + material + motif.

| Faction | Element | Palette | Materials & motif | Silhouette cue |
|---|---|---|---|---|
| **Kurogane** (heroes' clan, smiths) | — (gifted line) | charcoal, black-iron, muted steel-blue | blackened iron, folded-steel sheen; **crest: a broken-then-reforged blade** | disciplined, armored-practical |
| **Sōra** — Wind | 🌪️ | whites, pale grey, sky-blue | layered light fabric, feathers, tiny bells | long, trailing, always moving |
| **Nagi** — Water | 🌊 | deep blue, teal, sea-green | lacquer, netting, wrapped cloth, rope | fluid, layered, weighted hems |
| **Kaen** — Fire | 🔥 | crimson, ember-orange, black | scorched leather, heavy iron plate | broad, heavy, furnace-solid |
| **Ikazuchi** — Lightning | ⚡ | storm-violet, white, tarnished gold | ragged ascetic robes, prayer-cord, ritual scars | gaunt, sharp, weathered |
| **Kiri** — the Mist (hidden enemy) | (thin/none) | fog-grey, muted taupe, off-white | plain, understated, *forgettable*; **hidden crest: a coiled mist-spiral** | deliberately unremarkable |

**Kiri's design doctrine is the villain's whole strategy:** they dress to be *overlooked*. Sadao wears Kurogane charcoal, not Kiri grey — the grey only ever surfaces in tiny, missable details until the reveal. When you design a Kiri agent, design them to disappear.

**Ryuma's blade is a living progress bar:** bare, unadorned steel at the start; with each element awakened, a motif and a cold light bleed into the steel (wind-etch, water-hamon, ember-glow, storm-arc). By Act III it is unmistakably legendary. The **demon fragment** shows as a seam of darker metal with a faint, watchful warmth.

---

## 1. RYUMA — the Protagonist *(the Severed Blade)*

**One-line:** a dismissed younger son, quiet and deadly, walking his father's last road alone. *Zoro-like: stoic strength over swagger.*

- **Build & silhouette:** lean, athletic, mid-20s; economical stance, weight low. Reads as *controlled*, not showy. Signature silhouette = single katana worn edge-up, and the hawk **Kaze** often on his shoulder or wheeling above.
- **Face:** grounded, handsome-but-tired; dark eyes that hold grief he won't voice. Dark hair pulled back, a few loose strands. A small, old scar (training, from his father) he touches when he thinks of home. Ages subtly across the game — harder eyes by Act III.
- **Costume:** Kurogane charcoal and muted steel-blue; practical travelling swordsman's layers — worn haori, wrapped forearms, light armor at shoulder and shin. The **reforged-blade crest** at his back, faded from the road. Deliberately *plain* early — he is powerless and exiled — accumulating small tokens (teacher's charms, a Wind bell, a Water cord) as trophies of each element, so his outfit visually logs his journey.
- **Weapon & style:** the one-of-one Fivefold katana. Fighting style **evolves with the story** — pure disciplined swordsmanship at first (no magic, the Prologue state), then Wind (reach/mobility) → Water (parry/flow) → Fire (aggression) → Lightning (speed) layered in, player-shaped via the skill trees. Grounded, weighty, Souls/Nioh-legible animation.
- **Personality & voice:** few words, dry warmth underneath. Not cold — *contained.* Carries guilt (he left, he trusted Sadao) like a stone. Speaks most freely to Kaze and, later, Kaito.
- **Arc:** powerless exile → legend of the road → the man who finishes his father's sentence and reclaims a broken clan. His growth is *earned restraint* — the demon climax turns on him choosing not to burn his mother for power.
- **Signature image:** kneeling in the burning house, gripping his dying father's hand — everything gone still.

### 1a. Ryuma — reference & concept prompts *(for image gen → Blender/UE)*

**Using your own picture:** attach it as the **reference / input image** in Flux (image-to-image / character reference) so his **face and likeness stay consistent** while the prompt sets the outfit, mood, and pose. Add a line like *"keep the face and likeness from the reference image"* to either prompt.

**PROMPT A — cinematic "cold aura" hero shot** *(for vibe / approval):*
> "Full-body cinematic character portrait of a cold, stoic lone samurai radiating a quiet, dangerous, effortless aura — utterly composed and unbothered. Late twenties, lean and battle-worn; calm, piercing dark eyes with an ice-cold unreadable expression; tied-back black hair, faint scar across the brow, light stubble. He stands relaxed but perfectly centered, one hand resting on the katana at his hip. Outfit — dark, understated, functional, weathered: a deep indigo kimono, a layered tattered charcoal-grey haori with a high collar, cloth forearm wraps, dark hakama, a single crimson accent cord at the waist (his only splash of color), a beautiful understated katana at his hip. Muted cold palette of charcoal, indigo and ash. Drifting mist, wind moving the haori, dramatic cinematic rim light, moody dark background, shallow depth of field. Photorealistic, Unreal Engine 5 / Ghost of Tsushima / Nioh quality, hyper-detailed realistic skin and fabric, 8k. NOT anime, NOT cartoon, NOT cel-shaded. [Keep the face and likeness from the reference image.]"

**PROMPT B — T-pose model sheet** *(the one you actually build from — this is what makes Blender/UE easier):*
> "Character model sheet / turnaround reference for 3D modeling: the SAME character shown in three matching views side by side — front view, side (profile) view, and back view — standing in a straight, symmetrical A-pose (arms slightly out from the body), full body head-to-toe in frame. Neutral flat light-grey background, even flat studio lighting, NO dramatic shadows, NO perspective distortion (orthographic, straight-on). A lean, battle-worn stoic samurai in his late twenties: deep indigo kimono, layered charcoal-grey haori with a high collar, cloth forearm wraps, dark hakama, single crimson waist cord, katana at hip; tied-back black hair, faint brow scar. Identical, consistent design across all three views. Photorealistic, clean, sharp, hyper-detailed, technical design-sheet style — NOT a dramatic hero shot, NOT anime, NOT cartoon. [Keep the face and likeness from the reference image.]"

**Why Prompt B is set up this way (and how to use it in Blender):**
- **A/T-pose** → required later for clean **rigging** (arms out so the shoulder/elbow bones weight properly).
- **Flat grey background + even lighting** → no baked-in shadows, so it works as honest **color/texture reference** and cuts out cleanly.
- **Orthographic front + side** → in Blender, `Add → Image → Reference` (or N-panel → Background) and place the **front image in Front view (Numpad 1)** and the **side image in Right view (Numpad 3)**, aligned — then you **model directly over them** like tracing. This is the single biggest "easier in Blender" trick.
- Generate it **tall / portrait** (e.g. 1024×1536+) so the full body has resolution.
- *AI caveat:* getting all three views perfectly consistent is hard; if it struggles, generate **front** and **side** as two separate clean images at the same settings — those two are all you need as Blender reference planes.
- **For UE:** this same sheet is your texturing target — match his canon palette (indigo/charcoal + one crimson cord) so the in-engine material lines up.

**One-line:** the family's dearest friend and secret destroyer — a House Kiri agent who wore a good man's face for a lifetime. **The design brief is the whole twist: he must never read as the villain.**

- **Build & silhouette:** dignified elder, warm and open; the posture of a man who puts others at ease. Nothing sharp, nothing looming. If you put him in a lineup, a first-time player should pick *anyone* else as the antagonist. That is the design succeeding.
- **Face:** kind, weathered, laugh-lined; genuinely warm smile; soft, attentive eyes. Grandfatherly / favorite-uncle energy. **Everything is engineered for trust.** The only tell — held back for re-watches — is a stillness that comes over him when no one's looking.
- **Costume:** **Kurogane charcoal**, an elder councilman's robes — embedded, belonging, unremarkable. The **Kiri mist-spiral** exists only in places you won't look until told: the inner lining, a cord-end, the underside of a seal. Post-reveal wardrobe beat: the grey *comes forward* — same man, Kiri colors surfacing — and the warm smile, unchanged, now reads as a mask.
- **Weapon & style:** he rarely fights, and that's characterization — he *has people for that* (mercenaries, the Ironhound, the Enforcer). When the finale forces him, he's revealed as quietly, horribly competent — patient, efficient, no wasted motion; a duelist who hid his skill for decades the way he hid everything.
- **Personality & voice:** warm, wise, self-deprecating, endlessly reasonable. Gives good counsel. *Means* his kindnesses, which is what makes him monstrous. Post-reveal he does not rant — he explains, calmly, that he *is* the strong hand the realm needed, and grieves that it cost so much. Conviction, not cackling.
- **Arc (for the player):** trusted ally → uneasy absence (the letters) → the author of everything → and beneath even that, not a Kurogane at all, but Kiri. Two-stage detonation: **murderer** (reunion), **outsider** (finale).
- **Signature image:** first to the burning house, weeping, pulling Ryuma from the flames — the exact moment he erases himself from suspicion.

---

## 3. KAITO — the Brother *(the exiled heir)*

**One-line:** the golden son the world branded a mother-killer — now a bitter, fearsome rogue swordsman, certain his blood abandoned him.

- **Build & silhouette:** taller, broader, harder than Ryuma — was the clan's brightest blade. Ronin silhouette: stripped of clan finery, layered rags-over-quality, a bigger, rougher weapon presence. Reads dangerous before he speaks.
- **Face:** the family resemblance to Ryuma, weathered years past his age — exile-lean, scarred, a beard grown in. Eyes that have decided the world is against him. Where Ryuma contains grief, Kaito wears contempt over his.
- **Costume:** the ghost of Kurogane charcoal, faded and repaired with mismatched Water-blue and road-grey scavenged from wherever he hid. No crest — he tore it off. Deliberately *de-heraldried*: a man who belongs to no house now.
- **Weapon & style — Fire, heir-awakened, exile-hardened:** Kaito was awakened to **Fire** in his heir-training (the family's flame — Hidetora carried it, Genta teaches it) and years of bitterness forged it into something wrathful and merciless — aggressive, punishing, all-offense. *(Respects the magic rules: his element was opened by a master in youth, then honed alone. See [MAGIC_AND_DEMON.md](MAGIC_AND_DEMON.md) §1.)* This sets the **reunion duel** as fire-against-fire — Ryuma's disciplined, teacher-taught flame vs. Kaito's raw, furious one.
- **Personality & voice:** clipped, cutting, guards a deep wound with anger. Tests everything and everyone. Slowly, painfully, lets Ryuma back in — the thaw is the heart of the game.
- **Arc:** bitter loner → forced ally (the duel that becomes a back-to-back stand) → brother restored → co-heir who stands with Ryuma in their father's seat, vindicated at last.
- **Signature image:** the moment the fragment's truth lands and the contempt breaks — for the first time in years, Kaito is just a son who lost his mother.

---

## 4. HIDETORA — the Father *(Master of Kurogane)*

**One-line:** aging clan-lord, two-element master, Ryuma's only teacher — a beloved, just man murdered the night he learned the truth.

- **Build & silhouette:** broad, upright, age not yet bent him; the bearing of a lord who still leads from the front. A greatsword-katana presence, unhurried.
- **Face:** grey-streaked, strong-jawed, kind but weathered by grief (Kaede's death never left him). Warm to his son, iron to the council. A face the player should *miss* after the fire.
- **Costume:** the fullest expression of **Kurogane** heraldry — blackened iron plate over charcoal, the reforged-blade crest proud and unfaded. Ceremonial and martial at once; the standard the whole clan's look descends from.
- **Weapon & style:** master of **Fire & Lightning** — his brief playable/demo moments (Act 0 training) show controlled, awesome two-element mastery, the ceiling Ryuma is climbing toward. Deliberately makes the player go *"I want that."*
- **Personality & voice:** warm, exacting, principled; believes in Ryuma against the council. Carries a private investigation and a private grief he won't burden his son with — which gets him killed.
- **Arc:** the tutorial-father you bond with → the growing doubt → the man who dies with the truth half-spoken. His absence powers every teacher's aid and the whole road.
- **Signature image:** ignition — Fire in one hand, Lightning in the other — teaching his son what the world can be, in the last good days.

---

## 5. KAEDE — the Mother *(the demon in the blade)*

**One-line:** murdered before the story begins; her bound spirit is the forbidden fifth power — and, in the end, the witness that wins.

- **Build & silhouette (in memory / spirit form):** elegant, still, composed; seen in warm flashback and as a cold, luminous spirit-form once bound. Two visual registers — **living warmth** (golden, soft) and **bound spirit** (pale, drifting, edged with the demon's dark seam).
- **Face:** where Kaito and Ryuma's features come from; intelligent, perceptive — a woman who *notices* (it's what got her killed). Serene in memory, sorrowful as a spirit.
- **Costume:** **maple-motif** — Kaede means "maple"; autumn reds and falling-leaf patterns thread her robes, tying to "The Night of Falling Leaves." As a bound spirit, the reds desaturate toward ash, relit only at her final act.
- **"Weapon"/manifestation:** the demon power — when Ryuma channels her, spectral maple-light and a drifting figure move through his strikes; immense, beautiful, *costly.* Overuse frays her toward loss.
- **Personality & voice:** warm, sharp, protective; even bound and eroding, she is *herself* — which is why the twist works: she chooses truth over power because she is still a mother, not a weapon.
- **Arc:** the original wound (murdered, framed on her son) → the secret in the steel → the witness who clears Kaito and damns Sadao → peace, passing on, lost a second time.
- **Signature image:** her spirit rising over the council, speaking the truth she died holding — the "demon" the clan feared becoming their salvation.

---

## 6. OLD TOMOE — the Swordsmith *(the hub / keeper of the secret)*

- **Look:** stooped, powerful forearms, burn-scarred hands, soot-creased face; leather apron over charcoal. Older than Hidetora, sharp-eyed.
- **Role & style:** the game's **hub character** — awakens the blade's powers, sells/forges gear, dispenses lore and guilt. Non-combatant. Keeper of the deepest secret (he helped seal Kaede).
- **Personality:** gruff, grieving, evasive when pressed about the fragment; loyal to the family unto the taboo. Warms to Ryuma as the road goes on.
- **Signature image:** the forge-light on his face as he first *recognizes* what Ryuma's plain katana truly is.

---

## 7. AYAME — the Spy *(the truth from within)*

- **Look:** Kurogane household dress worn to blend, practical underneath; quick, watchful, keeps to edges. Carries a token of Kaede's (she was her handmaid). Later, prison-worn.
- **Role & style:** stealth/intel NPC; feeds Ryuma the truth by Kaze against Sadao's letters. Not a duelist — survives by wits and nerve. **Captured mid-game, freed by the brothers in the finale.**
- **Personality:** fierce, loyal, dry-humored under pressure; Ryuma's last tie to the good days and to his mother. Never believed Kaito's guilt.
- **Signature image:** loosing Kaze from a high window under Sadao's very roof, a coded truth tied to its leg.

---

## 8. THE FOUR TEACHERS

Each is a living chapter of Hidetora's life, and helps *because of him.* Grounded, distinct, elemental.

- **🌪️ HAZUKI — Wind (Takanoha).** Blind bell-keeper; youth-rival turned life-debt. Pale Sōra layers, feathered mantle, milk-blind eyes, bells woven into her hair; "sees" by wind — stance always subtly reacting to air. Serene, wry, sad. Teaches *Severing Gale*. **First to crack the lie** about Kaede.
- **🌊 ISEN — Water (Ukishima).** War-comrade turned soul-ferryman. Weathered boatman in Nagi teal and oilcloth, a ferryman's pole he wields like a blade, rope-wrapped hands. Quiet, penitent, watchful. Teaches *Returning Tide*. Reveals the father *suspected betrayal.*
- **🔥 GENTA — Fire (Homura).** Hidetora's sworn brother; the one who **ran.** Big, scarred, ember-eyed, a furnace-lord gone to drink — crimson and soot, a heavy chained blade. Loud grief, self-loathing, redemptive fury. Teaches *Ember Fang.* Confesses the night he fled — the family's flame he now hands to Ryuma (and which Kaito also carries).
- **⚡ RAIZŌ — the Hermit, Lightning (Narukami).** Hidetora's exiled master; last who knows the soul-art. Gaunt Ikazuchi ascetic, storm-violet rags, ritual scars, tarnished-gold cord; still and sudden like lightning. Grave, guilt-ridden, cryptic. Teaches *Thunderstep.* Gives the **second fragment** and points to Kaito.

---

## 9. RECURRING CAST

- **SŌJIRŌ AMANO — "the Laughing Blade" (Rival).** Grinning wandering duelist who fights for joy. Bright, flamboyant against the grimness — a splash of color, loose stylish layers, a fine sword worn with swagger. Recurs (Sakaimichi → Higan → decisive duel at Shirasagi), likely an ally by the end. *Very Zoro-rival energy* — Ryuma's growth mirror.
- **KUROBA — "the Ironhound" (Hunter).** Sadao's relentless tracker. Cold, tireless, armored in dark iron and hunting leathers, scent-hound motif, a brutal utilitarian weapon. Introduced at Kareno, last stand at Sekimon. A recurring dread, not a talker.
- **THE MYSTERIOUS FIGURE.** Hooded, glimpsed across cities; delivers the second fragment at Narukami. **Recommended identity/thread:** the one who has tried for years to get the truth to the family — possibly the sender of **the note** that killed Hidetora with knowledge. Keep the silhouette consistent and unreadable until reveal. *(Open.)*
- **KAZE — the Loyal Hawk.** Ryuma's messenger hawk, his father's boyhood gift. Real raptor weight and behavior — a companion, not a cartoon. Carries both Sadao's lies and Ayame's truth. Ties to the hawks of Takanoha.

---

## Open Threads (character-level)
- **The Mysterious Figure's true identity** (and whether they sent the fatal note).
- **Ayame & Ryuma** post-rescue — deeper bond or steadfast loyalty (unforced).
- **Sadao's fighting style specifics** for the forced finale duel — a hidden two-element master? (A chilling option: the "friend" secretly holds two elements no one knew.)
- **Full costume turnarounds & expression sheets** — next step per character once looks are approved (ties to `docs/build/CHARACTER_ART_PATH.md`).
