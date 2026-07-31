# Character Art Path — Building Ryuma (learn character modeling)

**Decision (2026-07-31):** the user chose to **learn character modeling** and build the exclusive Ryuma from scratch in Blender, rather than use a placeholder or commission. Fully bespoke, hardest/longest route — accepted knowingly.

> Honest scope: a realistic, rigged game hero is ~7 stacked disciplines and a **months-long** learning journey. First attempts won't match the concept art — normal for every character artist. We go slow, celebrate small wins, and teach each discipline in turn. Placeholder Manny stays in the game so systems keep progressing.

**Key liberating fact:** animation lives on the **UE skeleton**, not the model. Everything animated on Manny now will play on the final Ryuma once he's skinned to the same skeleton. No animation work is wasted.

## Learning Order (front-load a win)
1. **The katana** — hard-surface modeling. Teaches Blender core tools (extrude, bevel, mirror, loop cuts) on a forgiving geometric object we need anyway. **First project.**
2. **Ryuma's body** — start from a base mesh, then sculpt forms (skip from-a-cube anatomy).
3. **Retopology + UVs** — clean, animation-ready topology; unwrap for texturing.
4. **Texturing** — skin, steel, fabric (Blender first; Substance later if wanted).
5. **Clothing** — kimono + haori (modeled in Blender; Marvelous Designer optional later).
6. **Rig & skin** — bind to the UE5 Manny skeleton so all animations apply.

## References
- Concept art: realistic, weathered dark indigo kimono + tattered charcoal haori, crimson cord, brow scar, tied-back black hair (see chat gallery).
- Katana modeling reference generated (side profile + hilt detail) — deep crimson tsuka wrap, dark iron tsuba, curved blade.
- TODO: generate a Ryuma orthographic model sheet (front/side, T-pose) before body modeling.

## Notes
- Tools: Blender (free) for modeling/sculpt/retopo/UV/texture. All free.
- Reality-check checkpoints: if a stage stalls for weeks, we reassess (simplify style, or use a base) rather than burn out.
- This reorders the project: character art becomes a primary focus for a while; animation resumes with a real figure once the body + rig exist (katana can be animated with much sooner).
