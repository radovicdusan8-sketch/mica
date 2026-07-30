# Animation Path — Hand-Animation via Blender → UE5

**Decision (2026-07-31):** Ryuma's animations will be **hand-crafted and exclusive** — no off-the-shelf packs. Tool: **Blender** (free, industry-standard, scalable), piped into UE5 with Epic's free addons. Chosen for long-term quality, flexibility, and scalability over the lower-friction in-engine Control Rig route.

> Reality check we agreed to: hand-animation is a real craft that takes practice. First clips will look stiff — that's normal. We go one small exercise at a time, and we keep building game *systems* with placeholder motion so the project never stalls waiting on final animation.

## The Pipeline
1. **Blender** — animate on Ryuma's actual UE5 Mannequin skeleton.
2. **UE to Rigify** (Epic addon) — converts the bare UE skeleton into a Rigify **control rig** for intuitive animating. Ships UE5 Mannequin templates. *(Watch version compatibility — install via Blender Extensions so it matches your Blender build.)*
3. **Send to Unreal** (Epic addon) — one-click export of finished animation onto Ryuma in the editor. No retargeting.

Fallback if the Epic addons lag the newest Blender: **Mr Mannequins Tools** (community, also UE-mannequin-native, no retargeting).

## Learning Roadmap (stages)
- **Stage 0 — Setup:** install Blender + the two Epic addons; confirm they're enabled.
- **Stage 1 — Prove the round-trip:** get the UE5 Manny into Blender, make a trivial pose change, Send to Unreal, see it on Ryuma. (Pipeline before artistry.)
- **Stage 2 — Fundamentals:** keyframes, timing & spacing, posing, the core animation principles — taught on tiny exercises.
- **Stage 3 — First real clip:** a samurai **idle** (breathing, weight, ready stance) — the most-seen animation in the game.
- **Stage 4 — Motion:** walk and run cycles with a grounded samurai gait.
- **Stage 5 — Action:** a single katana **slash**, then combos (feeds Milestone 1: The Blade).

## Notes
- We learn *fundamentals*, not just buttons — the user chose to become an animator.
- Placeholder Manny animations stay in the game meanwhile so combat/systems keep progressing.
- Versions to confirm at setup: Blender build ↔ UE to Rigify / Send to Unreal compatibility.
