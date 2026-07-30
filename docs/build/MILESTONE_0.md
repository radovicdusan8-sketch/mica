# Milestone 0 — First Steps

**Goal:** a character we can run, sprint, jump, and move a camera around a test level. Prove the setup works and learn the Unreal editor. No code, no art — we use Unreal's built-in template and default character ("Manny") as Ryuma's stand-in.

**Definition of done:** press Play, move around smoothly with keyboard + mouse, jump, and the camera follows nicely.

---

## Step 1 — Create the project
1. Open the **Epic Games Launcher** → **Unreal Engine** tab → **Library**.
2. Under **Engine Versions**, click **Launch** on **5.8**.
3. In the **Unreal Project Browser**: choose **Games** → **Third Person**.
4. Settings on the right:
   - **Blueprint** (not C++) — we start codeless.
   - **Target Platform:** Desktop
   - **Quality Preset:** Maximum
   - **Starter Content:** ON (gives us basic props/materials)
   - **Raytracing:** OFF for now (perf while learning)
   - **Project Location:** `C:\Claude\severed-blade`
   - **Project Name:** `SeveredBlade`
5. Click **Create**. The editor opens after a short build.

> Result on disk: `C:\Claude\severed-blade\SeveredBlade\SeveredBlade.uproject` (+ Content/, Config/). Our `.gitignore` already keeps the giant auto-generated folders out of git.

## Step 2 — Explore & press Play
- **Viewport navigation:** hold **right-mouse** and use **WASD** to fly the camera; scroll to zoom.
- Hit the big **Play** button (or **Alt+P**). Click into the game view.
- Controls: **WASD** move, **mouse** look, **Space** jump. Confirm it all works.
- **Esc** or **Stop** to exit play.

## Step 3 — Make it ours (movement & camera feel)
Open the character Blueprint: `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`.
- **Character Movement component:** tune *Max Walk Speed*, *Jump Z Velocity*, *Gravity Scale*, *Rotation Rate* for a weightier, more grounded feel (Wukong/Souls-like, not floaty).
- **Camera Boom (SpringArm):** adjust *Target Arm Length* and *Socket Offset* for a more cinematic over-the-shoulder framing.
- We'll iterate on numbers together until it *feels* right.

---

## Notes
- **Visual Studio** is only needed once we move to C++ (later milestones). Blueprints need none of it.
- Next milestone (**M1 — The Blade**): light/heavy sword attacks, combos, and a weighty dodge.
