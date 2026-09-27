# 01. Project Setup

> **Written for:** Unreal Engine 5.8 (5.8.3 hotfix), Visual Studio 2026 Community, Git for Windows 2.55 (includes Git LFS), Claude Code (native Windows installer), Blender 5.2 LTS (5.2.2), MCP for Blender 2.1.1, and Epic's Unreal MCP plugin (Experimental, ships with 5.8).
> **Facts checked:** 2026-09-27. Several vendor sites (Epic, Microsoft, Blender, AMD, Perforce) couldn't be read directly while this was written, so some facts come from search excerpts or secondary sources. Those are marked `VERIFY:` with what to check.

## What this covers

This walkthrough takes you from an empty PC to a working toolchain. You install Unreal Engine 5.8 and Visual Studio 2026 and create the `WraithGame` C++ project inside this repo with the README's folder structure. You set up version control with an off-site copy and prove it with a restore test. Then you connect Claude Code to the repo, to Blender, and to the Unreal Editor through MCP servers, proving each with a small test task. It ends with a smoke test that sends a lantern post blockout from Blender into Unreal: the first real piece of the Lantern Market.

## Why it matters for Wraith

- **Friction adds up.** You work part-time. A toolchain that breaks now and then costs whole sessions, and a lost file can cost weeks. An hour spent here saves dozens later.
- **C++ from day one.** Combat, GAS, spirit switching, and the lantern system are C++ systems (README, section 6). Starting as a C++ project proves Visual Studio, Live Coding, and command-line builds before you depend on them. Command-line builds also let Claude compile the game and read the errors itself.
- **The repo will be mostly art.** Megascans, `.blend` files, Substance projects, Marvelous Designer cloth, mocap, and Japanese voice recordings are large binary files. The version control choice decides your storage costs and how fast everything feels for years.
- **Claude is part of the toolchain.** Later walkthroughs assume Claude can build the C++ code and drive Blender and the Unreal Editor through MCP. Prove that here on throwaway tasks, not in the middle of the Vesper fight.
- **AMD hardware.** Nothing in this walkthrough needs NVIDIA or CUDA. The NVIDIA-only feature you'll run into (DLSS) comes up in walkthrough 07, where TSR and AMD FSR replace it.

## Tools

| Tool | What it's for | Cost | Commercial license OK? | AMD notes |
|---|---|---|---|---|
| Unreal Engine 5.8 (through the Epic Games Launcher) | The engine and editor | Free to use. 5% royalty on gross revenue above the first US$1 million per product. The rate drops to 3.5% under "Launch Everywhere with Epic" if the game comes out on the Epic Games Store at the same time as, or before, other PC stores. No royalty on Epic Games Store sales. | Yes, under the Unreal Engine EULA | DirectX 12 on AMD works. Lumen hardware ray tracing needs an AMD RX 6000 series or newer, which the RX 9060 XT is. DLSS is NVIDIA-only; use TSR (built in) or AMD's FSR plugin for 5.8 (walkthrough 07). |
| Epic Games Launcher | Installs Unreal; gives access to Fab | Free | n/a | None |
| Visual Studio Community 2026 | C++ compiler, debugger, and IDE | Free | Yes for an individual. Microsoft: "Any individual developer can use Visual Studio Community to create their own free or paid apps." | None |
| JetBrains Rider (optional alternative IDE) | C++ IDE with strong Unreal support | Free only for non-commercial use. Wraith is commercial, so it needs a paid license. `VERIFY:` current price (JetBrains raised prices in October 2025). | Only with a paid license | None |
| Git for Windows (includes Git LFS) | Version control on your PC | Free, open source | Yes | None |
| GitHub (recommended host) | Off-site copy of the repo | Free and Pro plans include 10 GiB of LFS storage and 10 GiB of LFS bandwidth per month; above that it's metered. `VERIFY:` current prices. A 2024 GitHub announcement listed $0.07 per GiB-month for storage and $0.0875 per GiB for bandwidth. | Yes | None |
| Azure DevOps (free alternative host) | Off-site copy of the repo | Free for the first 5 users. Microsoft says it offers Git LFS "for free". | Yes | None |
| Perforce P4, formerly Helix Core (alternative) | Version control built for large binary files | Free for up to 5 users and 20 workspaces. P4 Cloud hosting is $39 per user per month. | `VERIFY:` no explicit statement on commercial use of the free tier was found | None |
| Claude Code | AI coding agent in your terminal | Needs a Pro, Max, Team, Enterprise, or Console (API) account; the free plan doesn't include it. At the time of writing, Pro was $20/month ($17/month billed annually) and Max was $100 or $200/month. `VERIFY:` prices at https://claude.com/pricing | Yes. `VERIFY:` Anthropic's current consumer terms on ownership of outputs. | None |
| Blender 5.2 LTS | 3D modeling; the Blender MCP drives it | Free (GPL) | Yes. Blender's license page: what you create with Blender is your sole property. | Cycles renders on the RX 9060 XT through HIP, supported since Blender 4.4. Hardware ray tracing (HIP RT) is on by default since 5.1. |
| uv | Runs the Blender MCP server | Free (MIT or Apache-2.0) | Yes | None |
| MCP for Blender, by ahujasid (formerly "blender-mcp") | Lets Claude Code control Blender | Free (MIT). Optional paid "Premium" and third-party AI services, none needed here. | Yes | None |
| Unreal MCP, by Epic (Experimental) | Lets Claude Code control the Unreal Editor | Ships with the engine; no separate price found | Yes, as part of the engine. `VERIFY:` no extra terms. | None |
| AMD Software: Adrenalin Edition | GPU driver | Free | n/a | Required. The first driver whose release notes list the RX 9060 XT is 25.6.1, so use that or newer. |

## Before you start

**Accounts.** You need an Epic Games account (free), a GitHub account (you have one, since this repo lives there), and a Claude subscription (Pro or higher).

**Disk space.** Put everything on an NVMe SSD. Approximate sizes:

| Item | Rough size | Source |
|---|---|---|
| Unreal Engine 5.8, minimal install | About 30–40 GB | Third-party estimate. Epic doesn't publish sizes. The launcher shows the real number before you confirm. |
| Unreal editor debug symbols (optional) | Roughly doubles the engine's size | Third-party estimate. Skip them for now. |
| Visual Studio 2026 with the C++ game workloads | Typical installs are 20–50 GB | Microsoft's system requirements. The installer shows the exact total. |
| Blender 5.2 | About 350 MB installer | blender.org |
| AMD FSR plugin (later, in walkthrough 07) | About 1.9 GB download | AMD GPUOpen |
| The WraithGame project and Unreal's caches | Grows to tens of GB over time | Your own measurements |

**Recommendation:** have at least 250 GB free before you start. That number is a round-up of the table above, not an official figure.

**Walkthroughs to do first:** none. Read `README.md` and Milestone 1 in [`../ROADMAP.md`](../ROADMAP.md).

**Total time:** roughly 6–10 hours of hands-on work over two to four sessions, plus download time.

---

## Steps

### Step 1. Prepare Windows, the AMD driver, and the repo location

- **Goal:** Windows and the GPU driver are current, there's enough fast disk space, and you've picked a safe location for the repo.
- **Do this:**
  1. Run **Settings > Windows Update > Check for updates**, install everything, and reboot.
  2. Install the latest **AMD Software: Adrenalin Edition** from https://www.amd.com/en/support/download/drivers.html. Pick the RX 9060 XT manually or use AMD's auto-detect tool, then reboot. Epic's guidance is to use the "latest stable releases from each card manufacturer".
  3. Check free space on your SSD in File Explorer's **This PC** view (see the table above).
  4. Pick a short folder path for the repo with no spaces, such as `C:\Dev\Wraith` or `D:\Wraith`. **Don't** use Documents or Desktop, which Windows 11 often syncs to OneDrive. OneDrive syncing an Unreal project causes locked files and slowdowns.
  5. Optional, but recommended because Unreal paths get deep: enable Windows long-path support. In **PowerShell as Administrator**, run:
     ```powershell
     New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
     ```
     Reboot afterwards. This only helps programs that opt in to long paths, so keep the repo path short anyway.
- **Done when:** AMD Software shows a driver version of 25.6.1 or newer, you have 250 GB or more free on an SSD, and you've written your repo path down.
- **Common mistakes:**
  - Putting the repo inside a OneDrive-synced folder. Move it.
  - Installing on a hard disk drive. Shader compiles and editor loads become very slow.
  - Skipping the reboot after the driver install.
- **Claude can help:** Manual. Windows Update and the AMD installer are GUI tools. Once Claude Code is installed (step 6), it can check disk space and the long-path registry value for you.
- **Time:** 30–60 minutes, mostly waiting on downloads.

### Step 2. Start the Unreal Engine 5.8 download

The engine is the biggest download, so start it first and do steps 3–7 while it runs.

- **Goal:** Unreal Engine 5.8 (the newest 5.8.x hotfix) is installed with only the parts you need.
- **Do this:**
  1. Download the Epic Games Launcher from https://www.unrealengine.com/download, install it, and sign in.
  2. Go to **Unreal Engine > Library**. Next to **Engine Versions**, click **+**, choose the newest **5.8.x** release (5.8.3 at the time of writing), and click **Install**. `VERIFY:` exact launcher labels.
  3. Choose an install folder on your fast SSD. The default, `C:\Program Files\Epic Games\UE_5.8`, is fine if C: has room.
  4. In the **Options** dialog:
     - **Keep:** Core Components (required), and Templates and Feature Packs (needed for the Third Person template).
     - **Skip for now:** Starter Content. It isn't needed; the gray box uses Unreal's basic shapes.
     - **Skip for now:** Editor symbols for debugging. They're large. You can add them later from the engine tile's **Options** without re-downloading the engine.
     - **Optional:** Engine Source. It's useful for reading engine code while you learn, but it can't be used to rebuild the engine.
     - **Target platforms:** you only need Windows. Untick Android, iOS, Linux, and any others. `VERIFY:` which platforms are ticked by default in 5.8.
  5. Read the size the dialog shows before you confirm.
- **Done when:** the Library shows a 5.8.x tile with a **Launch** button.
- **Common mistakes:**
  - Ticking every platform and the debug symbols, which can push the install past 100 GB.
  - Installing a **Preview** build. Previews are for testing, never for your real project.
  - Mixing hotfix versions later. Stay on 5.8.x for the whole vertical slice.
- **Claude can help:** Manual. Claude can't click in the Epic Games Launcher.
- **Time:** 15 minutes hands-on, plus 1–4 hours of download depending on your connection.

### Step 3. Install Visual Studio 2026 Community

- **Goal:** the C++ compiler and IDE that Unreal 5.8 expects are installed.
- **Do this:**
  1. **`VERIFY:` first.** Open Epic's page "Setting Up Visual Studio Development Environment for C++ Projects in Unreal Engine" for 5.8 (link in References) and check the recommended Visual Studio version and components. While this was being written, Epic's page couldn't be opened. Secondary sources, including an Epic community tutorial, say:
     - Unreal 5.8 officially supports and recommends **Visual Studio 2026**.
     - Visual Studio 2022 will not work with 5.8, because 5.8 expects the v145 MSVC toolset that ships with VS 2026.

     If Epic's page says something different, follow Epic.
  2. Download **Visual Studio Community 2026** from https://visualstudio.microsoft.com/vs/community/ and run the installer.
  3. On the **Workloads** tab, tick **Desktop development with C++** and **Game development with C++**.
  4. In the right-hand panel, under **Game development with C++**, tick the Unreal items. In VS 2022 they're named:
     - "Visual Studio Tools for Unreal Engine"
     - "Unreal Engine Test Adapter"
     - "Visual Studio debugger tools for Unreal Engine Blueprints"
     - a Windows SDK

     `VERIFY:` the names in VS 2026.
  5. Check **Total space required** at the bottom of the installer, then install.
  6. You get a safety net later: Unreal generates a `.vsconfig` file next to the project's solution. The first time you open the solution (step 9), Visual Studio may offer **Install Missing Feature(s)** in Solution Explorer. Accept it.
- **Done when:** Visual Studio 2026 opens, and the Visual Studio Installer shows both workloads as installed.
- **Common mistakes:**
  - Installing VS 2022 for Unreal 5.8.
  - Installing only "Desktop development with C++" and missing the Unreal integrations.
  - Running out of space on C:. Some Visual Studio components always install to C:, even if you move the IDE.
- **Claude can help:** Mostly manual, because the installer is a GUI. Claude can explain what any component does, or write a `.vsconfig` you can import through **Visual Studio Installer > More > Import configuration**. The one Unreal generates in step 9 is the more reliable choice.
- **Time:** 30–90 minutes, mostly download.

### Step 4. Choose version control

**Version control** keeps every version of every file, so you can undo mistakes and restore the project on a new PC. Games make it harder than normal software because most files are large binaries (`.uasset`, `.blend`, textures, audio) that can't be merged like code.

| | Git + Git LFS | Perforce P4 |
|---|---|---|
| **How it handles big files** | Git stores text. Git LFS (Large File Storage) keeps big files on the server and puts small "pointer" files in Git history. | Built for big binaries from the start |
| **Cost for a solo dev** | Git is free. Hosting: GitHub Free includes 10 GiB of LFS storage and 10 GiB of bandwidth per month, then charges per GiB. Azure DevOps offers LFS for free. | The P4 Server is free for up to 5 users and 20 workspaces, but you run it yourself: on your PC, a NAS, or a cloud VM you pay for. P4 Cloud costs $39 per user per month. |
| **Setup effort** | Low: install Git, add two config files, push | Medium to high: install and run a server, set up a depot or stream, a typemap, and a workspace, then plan backups |
| **What you already know** | You're a programmer, so probably Git | New concepts: depots, streams, workspaces, changelists, typemaps, checkout |
| **Unreal Editor integration** | The built-in Git provider is labeled beta. A community plugin (Project Borealis) is better but you have to compile it. Many solo devs just run Git outside the editor. | First-class and supported by default: check out, lock, and submit from inside the editor |
| **File locking** (stopping two people editing the same asset) | Optional (`git lfs lock`). You don't need it while solo. | Built in |
| **Off-site backup** | Automatic every time you push to a host | Your job, unless you pay for P4 Cloud |
| **Working with Claude Code** | Natural: Claude uses Git all the time (status, diff, commit, branches) | Claude can run the `p4` command line, but most Claude Code workflows assume Git |
| **Gotchas** | Every pushed version of a large file counts toward storage (a 500 MB file pushed twice uses 1 GB). GitHub blocks files over 100 MiB without LFS, and LFS files over 2 GB on Free and Pro plans. | A server you have to keep running and back up |

**Recommendation: Git + Git LFS, hosted on GitHub, where this repo already lives.**

- You already know Git, and Claude Code works best with it.
- Pushing gives you an off-site copy with no server to run.
- File locking doesn't matter while you're solo.
- Costs are small and visible: the first 10 GiB of LFS are free, then you pay per GiB with a budget cap you set.

**Two things to know before you commit to it:**

- If you'd rather pay nothing for storage, **Azure DevOps** offers Git LFS for free. The workflow is identical; only the remote URL changes. Two Azure limits: repos with LFS files can't use SSH (use HTTPS), and each LFS upload has a one-hour limit.
- Switch to **Perforce** if, later on:
  - artists join and edit the same assets as you,
  - history grows past a few hundred GB, or
  - Git operations get painfully slow.

  Starting a Perforce depot from a snapshot of the current files is straightforward; the Git history can stay archived.

**What goes in the repo.** Commit everything you'd need to rebuild the game:

- `Source/`, `Config/`, `Content/`, and the `.uproject` file
- plugin source
- the source art you'd need to re-export: `.blend`, `.spp`, Marvelous Designer projects, cleaned mocap
- final voice takes and music

Never commit the folders Unreal regenerates: `Binaries/`, `Intermediate/`, `Saved/`, and `DerivedDataCache/`.

If storage costs start to matter, keep very large raw captures (phone mocap videos, raw voice recording sessions) in a separately backed-up folder outside the repo, and commit only the cleaned results. That's a trade-off against the README's layout, which puts raw mocap in `source-art/mocap`, so it's your call.

- **Goal:** a decision you can live with for at least the vertical slice.
- **Do this:** read the table, decide, and write the decision into `CLAUDE.md` (the "Version control" line in the Stack section). If you choose Perforce, follow the appendix at the end of this walkthrough in place of steps 5, 7, and 12.
- **Done when:** the decision is written down.
- **Common mistakes:**
  - Choosing a host with a tiny LFS quota. GitLab.com Free has 10 GiB per project, including LFS. Bitbucket Free has 1 GB.
  - Assuming "free" means unlimited. GitHub's free LFS quota will run out during the vertical slice.
- **Claude can help:** Claude can explain the trade-offs, estimate your repo size from your asset list, and set up whichever option you pick.
- **Time:** 30 minutes.

### Step 5. Install Git and put this repo on your PC

- **Goal:** Git and Git LFS are installed, and this repo is cloned to your chosen path.
- **Do this:**
  1. Install **Git for Windows** from https://git-scm.com/downloads/win. The defaults are fine. Git LFS is part of the installer and ticked by default. Git Credential Manager, also a default, handles signing in to GitHub through your browser.
  2. Open a **new** PowerShell window and run:
     ```powershell
     git --version
     git lfs version
     git lfs install
     git config --global core.longpaths true
     git config --global user.name "Your Name"
     git config --global user.email "you@example.com"
     ```
  3. Clone the repo to your chosen path, and sign in through the browser when asked:
     ```powershell
     git clone https://github.com/<you>/<repo>.git C:\Dev\Wraith
     ```
  4. On GitHub, set a monthly budget for Git LFS so you control the cost once you pass the free 10 GiB. `VERIFY:` the current menu path; look under your account's **Settings > Billing and licensing**.

     Why this matters: with no payment method or a $0 budget, GitHub **blocks LFS use** once the quota is used up. New clones then get only pointer files, and pushes fail.
- **Done when:** `git lfs version` prints a version, and `git -C C:\Dev\Wraith status` says the working tree is clean.
- **Common mistakes:**
  - Cloning into a OneDrive folder.
  - Running `git lfs install` in an old terminal before Git's PATH change took effect. Open a new terminal.
  - Pushing hundreds of GB over a slow connection in one go. Push in smaller chunks.
- **Claude can help:** Claude can run every command after the first install, once it's set up in step 6. You have to do the GitHub browser sign-in and the billing settings yourself.
- **Time:** 20–30 minutes.

### Step 6. Install Claude Code and connect it to the repo

This comes early so Claude can help with the rest of the setup.

- **Goal:** Claude Code runs in the repo root, reads `CLAUDE.md`, and can run Git.
- **Do this:**
  1. In PowerShell (not as Administrator), run:
     ```powershell
     irm https://claude.ai/install.ps1 | iex
     ```
     There are two other ways to install:
     - From CMD: `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
     - With WinGet: `winget install Anthropic.ClaudeCode`. WinGet installs don't auto-update; the native installer's do.
  2. Open a **new** terminal and run `claude --version`, then `claude doctor` for a health check. Because Git for Windows is installed, Claude Code uses Git Bash for shell commands, and it also has a PowerShell tool.
  3. Start it from the repo root:
     ```powershell
     cd C:\Dev\Wraith
     claude
     ```
     Log in through the browser when prompted.
  4. Type `/context` and check that `CLAUDE.md` appears under **Memory files**. `README.md` loads too, because `CLAUDE.md` imports it.
  5. **Permission modes.** Recent Claude Code versions start interactive sessions in **auto mode**, where a classifier approves most actions instead of asking you. **Shift+Tab** cycles modes; from auto, the first press switches to **Manual** mode, which asks before each new kind of action. Stay in Manual while you're learning how Claude works with MCP tools.
  6. Add project permission rules so risky commands always ask, even in auto mode. Ask Claude to create `.claude/settings.json` with the content below, then commit it:
     ```json
     {
       "permissions": {
         "ask": [
           "Bash(git push *)",
           "Bash(git reset *)",
           "Bash(git clean *)",
           "Bash(rm *)",
           "PowerShell(git push *)",
           "PowerShell(git reset *)",
           "PowerShell(git clean *)",
           "PowerShell(Remove-Item *)",
           "mcp__blender__execute_blender_code"
         ]
       }
     }
     ```
     The last line refers to the Blender MCP from step 13. It makes Claude ask before running arbitrary Python in Blender.
  7. **Test task.** Type:
     > Read CLAUDE.md and docs/ROADMAP.md. Tell me (1) the hardware rules you'll follow, (2) the current milestone, and (3) the top-level folders in this repo. Then run `git status` and `git lfs env` and tell me whether Git LFS is set up. Don't change any files.
- **Done when:** the answer mentions the AMD RX 9060 XT, no CUDA, and TSR or FSR instead of DLSS; names Milestone 1 (Setup); lists `docs/`; and reports Git LFS as installed.
- **Common mistakes:**
  - `claude` isn't recognized: open a new terminal. If it still fails, see the troubleshooting page in References.
  - `'irm' is not recognized`: you're in CMD, not PowerShell.
  - Using a free Claude plan, which doesn't include Claude Code.
  - Starting `claude` in a subfolder. Always start it in the repo root so it picks up `.mcp.json` and `.claude/settings.json`.
- **Claude can help:** Install and login are manual. After that, Claude can read `claude doctor` output with you and write the settings file.
- **Time:** 20–30 minutes.

### Step 7. Create the folder structure and the large-file rules

Do this **before** the Unreal project exists, so every `.uasset` is stored in LFS from the very first commit.

- **Goal:** the README's folder layout exists, and Git knows which files go to LFS and which to ignore.
- **Do this:**
  1. Ask Claude:
     > Create the README folder structure (except WraithGame/, which Unreal creates) with a .gitkeep in each empty folder. Then create the root .gitattributes and .gitignore from walkthrough 01, step 7. Show me the diff before committing.
  2. Root `.gitattributes`. Every binary type the project will produce goes to LFS:
     ```gitattributes
     # Normalize line endings for text files
     * text=auto

     # Unreal
     *.uasset filter=lfs diff=lfs merge=lfs -text
     *.umap filter=lfs diff=lfs merge=lfs -text

     # 3D, cloth, texturing, mocap
     *.blend filter=lfs diff=lfs merge=lfs -text
     *.fbx filter=lfs diff=lfs merge=lfs -text
     *.obj filter=lfs diff=lfs merge=lfs -text
     *.glb filter=lfs diff=lfs merge=lfs -text
     *.abc filter=lfs diff=lfs merge=lfs -text
     *.bvh filter=lfs diff=lfs merge=lfs -text
     *.spp filter=lfs diff=lfs merge=lfs -text
     *.sbsar filter=lfs diff=lfs merge=lfs -text
     *.zprj filter=lfs diff=lfs merge=lfs -text
     *.zpac filter=lfs diff=lfs merge=lfs -text
     *.casc filter=lfs diff=lfs merge=lfs -text

     # Images and paint files
     *.png filter=lfs diff=lfs merge=lfs -text
     *.jpg filter=lfs diff=lfs merge=lfs -text
     *.jpeg filter=lfs diff=lfs merge=lfs -text
     *.tga filter=lfs diff=lfs merge=lfs -text
     *.tif filter=lfs diff=lfs merge=lfs -text
     *.tiff filter=lfs diff=lfs merge=lfs -text
     *.exr filter=lfs diff=lfs merge=lfs -text
     *.hdr filter=lfs diff=lfs merge=lfs -text
     *.dds filter=lfs diff=lfs merge=lfs -text
     *.psd filter=lfs diff=lfs merge=lfs -text
     *.kra filter=lfs diff=lfs merge=lfs -text

     # Audio and video
     *.wav filter=lfs diff=lfs merge=lfs -text
     *.flac filter=lfs diff=lfs merge=lfs -text
     *.mp3 filter=lfs diff=lfs merge=lfs -text
     *.ogg filter=lfs diff=lfs merge=lfs -text
     *.mp4 filter=lfs diff=lfs merge=lfs -text
     *.mov filter=lfs diff=lfs merge=lfs -text
     *.mkv filter=lfs diff=lfs merge=lfs -text

     # Fonts and archives
     *.ttf filter=lfs diff=lfs merge=lfs -text
     *.otf filter=lfs diff=lfs merge=lfs -text
     *.pdf filter=lfs diff=lfs merge=lfs -text
     *.zip filter=lfs diff=lfs merge=lfs -text
     *.7z filter=lfs diff=lfs merge=lfs -text
     ```
     `VERIFY:` the file extensions your versions of Marvelous Designer (`.zprj`, `.zpac`) and Cascadeur (`.casc`) actually save, and add ArmorPaint's project extension if you pick it over Substance Painter. Check each tool's save dialog the first time you use it.
  3. Root `.gitignore`. It covers source-art and tool junk; the Unreal-specific rules go in `WraithGame/.gitignore` in step 8:
     ```gitignore
     # Blender backup files (.blend1, .blend2, ...)
     *.blend[0-9]*

     # Backup and temp files from various tools
     *~
     *.tmp

     # Reaper peak cache files
     *.reapeaks

     # Windows junk
     Thumbs.db
     desktop.ini

     # Personal Claude Code files (per the Claude Code docs)
     CLAUDE.local.md
     .claude/settings.local.json
     ```
  4. Check that the LFS rule works on a path that doesn't exist yet:
     ```powershell
     git check-attr filter -- WraithGame/Content/Test.uasset
     ```
     It should print `WraithGame/Content/Test.uasset: filter: lfs`.
  5. Commit and push.
- **Done when:** the folders exist, the `check-attr` test prints `filter: lfs`, and the commit is on GitHub.
- **Common mistakes:**
  - Adding `.gitattributes` **after** committing binaries. Those files are then stored in normal Git history forever. Fixing it takes `git lfs migrate`, which rewrites history. Do this step first.
  - Using GitHub's Unreal `.gitignore` at the **repo root**. It ignores `*.obj`, meaning compiled object files, which would also hide `.obj` meshes in `source-art/`. That's why it goes inside `WraithGame/` only.
- **Claude can help:** Fully. Claude creates the folders and files, runs the check, and commits. Review the diff before it commits.
- **Time:** 20 minutes.

### Step 8. Create the WraithGame C++ project

- **Goal:** a C++ Unreal project named `WraithGame` exists at `C:\Dev\Wraith\WraithGame\`.
- **Do this:**
  1. Launch Unreal Engine 5.8 from the Epic Games Launcher. The **Unreal Project Browser** opens.
  2. Choose **Games > Third Person**. It gives you a C++ character with a camera and Enhanced Input already wired up, which is a good base for a third-person brawler.
  3. In **Project Defaults**:
     - Project type: **C++**, not Blueprint.
     - Target platform: **Desktop**.
     - Quality preset: **Maximum**.
     - **Starter Content:** off.
     - Leave **ray tracing** off for now; walkthrough 07 decides Lumen settings.
     - **Variant:** none.

     `VERIFY:` the exact labels in 5.8's dialog.
  4. About variants: the Third Person template offers variants (Combat, Platforming, Side Scroller). The Combat variant includes combat mechanics, enemy targeting, and health management. Don't build Wraith on it, because Wraith's combat is custom C++ and GAS (walkthroughs 08–09). It's worth studying, though: create a separate throwaway project **outside the repo** with the Combat variant and read how Epic built it. `VERIFY:` a 2025 forum thread reported that variants are offered only for Blueprint projects.
  5. Set **Project Location** to the repo root (`C:\Dev\Wraith`) and **Project Name** to `WraithGame`. Unreal creates `C:\Dev\Wraith\WraithGame\WraithGame.uproject`.
  6. Click **Create**. Unreal generates and compiles the C++ code, then opens the editor. The first launch compiles thousands of shaders, which can take 10–40 minutes; watch the counter at the bottom right. Your CPU matters more than your GPU for this.
  7. Close the editor. Ask Claude to save GitHub's Unreal ignore template as `WraithGame/.gitignore` (URL in References). It ignores `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`, `*.sln`, `.vs/`, and `*_BuiltData.uasset`, among others.
- **Done when:** `WraithGame/Source/WraithGame/` contains `.h` and `.cpp` files. The template's classes are named after the project, such as `AWraithGameCharacter`. They're scaffolding; walkthrough 08 replaces them with `AWCharacter` and the other `W`-prefixed classes.
- **Common mistakes:**
  - Choosing **Blueprint**. You can add C++ later, but starting as C++ is cleaner.
  - Ending up with `WraithGame\WraithGame\WraithGame.uproject` because the location was set to a `WraithGame` folder. Set the location to the repo root.
  - A project name with spaces. It becomes the C++ module name and the `WRAITHGAME_API` macro.
  - Turning Starter Content on. It bloats the repo for no gain.
- **Claude can help:** The Project Browser is manual. Afterwards Claude can read the generated source and explain every file, and it can write `WraithGame/.gitignore`.
- **Time:** 15 minutes, plus 10–40 minutes of first compile and shaders.

### Step 9. First build, first Play, and a Live Coding test

**Live Coding** recompiles C++ while the editor is running. It's fast, but only safe for changes inside function bodies.

- **Goal:** you can build in Visual Studio, play in the editor, and hot-patch a function with Live Coding.
- **Do this:**
  1. With the editor closed, right-click `WraithGame.uproject` and choose **Generate Visual Studio project files**. On Windows 11 it's under **Show more options**. This creates `WraithGame.sln`.
  2. Open `WraithGame.sln` in Visual Studio 2026. If Solution Explorer offers **Install Missing Feature(s)**, accept it.
  3. In the toolbar, set the configuration to **Development Editor** and the platform to **Win64**. Make sure **WraithGame** is the startup project (shown in bold; right-click it and choose **Set as Startup Project** if not). Right-click WraithGame and choose **Build**.
  4. Press **F5** (Start Debugging). The editor opens with the debugger attached. Click **Play** and run around the template map. That's PIE, Play In Editor.
  5. Make a throwaway test class:
     - In the editor, choose **Tools > New C++ Class > Actor > Next**, name it `WSetupCheckActor` (Unreal adds the `A` prefix), and click **Create Class**.
     - Close the editor. Adding a class changes headers, so rebuild with the editor closed.
     - In `WSetupCheckActor.cpp`, add this line inside `BeginPlay()`, after `Super::BeginPlay();`:
       ```cpp
       UE_LOG(LogTemp, Warning, TEXT("Wraith setup check: C++ build works"));
       ```
     - Build again, then press F5.
  6. In the editor, drag `WSetupCheckActor` from the Content Browser's **C++ Classes > WraithGame** folder into the level. Press Play and open **Window > Output Log**. The yellow warning line should appear.
  7. **Live Coding test.** With the editor still open:
     - Change the text to `"Wraith setup check: Live Coding works"`, save, and press **Ctrl+Alt+F11**.
     - When the compile finishes, press Play again. You should see the new text.
  8. Remove the test actor from the level before saving. Leave the class for now; it's handy for future checks.
- **Done when:** both log lines appear, the first after a full build and the second after Live Coding.
- **Common mistakes:**
  - Building in Visual Studio while the editor is open. You'll see "Unable to build while Live Coding is active". Close the editor, or use Ctrl+Alt+F11.
  - Using Live Coding after changing a header or `UPROPERTY`/`UFUNCTION`/`UCLASS`. The safe habit is to close the editor and do a full build after any header or reflection change.
  - The wrong startup project, where F5 launches something other than WraithGame.
  - On opening the `.uproject` after pulling new code, Unreal asks "Missing modules… rebuild?". Answer yes, or build in Visual Studio.
- **Claude can help:** Claude can write the code change, explain the generated class, and, after step 10, compile from the command line and fix errors itself. Clicking in the editor is manual.
- **Time:** 45–90 minutes.

### Step 10. Build from the command line, so Claude can compile

- **Goal:** the game compiles from a terminal command, so Claude can build it and read compiler errors directly.
- **Do this:**
  1. Close the Unreal Editor.
  2. Run this, adjusting both paths to yours:
     ```powershell
     & "C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\Build.bat" WraithGameEditor Win64 Development -Project="C:\Dev\Wraith\WraithGame\WraithGame.uproject" -WaitMutex
     ```
     `WraithGameEditor` is the editor build target that Unreal created for the project. Visual Studio calls the same `Build.bat` with the same argument pattern.
  3. Ask Claude to put the exact working command into the **Commands** section of `CLAUDE.md`, along with your engine path.
- **Done when:** the output ends with `Result: Succeeded`, and `CLAUDE.md` has the command.
- **Common mistakes:**
  - Leaving the editor open. You'll get the Live Coding error.
  - A wrong engine path or a typo in `-Project=`.
  - Forgetting quotes around paths that contain spaces.
- **Claude can help:** Fully, once the command works: "Build the editor target and fix any compile errors" becomes a normal request.
- **Time:** 15 minutes.

### Step 11. Organize the Content folder and set a few editor habits

In Unreal asset paths, the project's `Content` folder is called **`/Game`**. So `/Game/Wraith/Maps` is the folder `WraithGame/Content/Wraith/Maps` on disk.

- **Goal:** your own assets have a clear home, separate from anything that comes from Fab.
- **Do this:**
  1. Plan this layout. You can create it by hand now (Content Browser: right-click > **New Folder**), or let the Unreal MCP create it as a test in step 14:
     ```text
     /Game/Wraith/
       Core/           Blueprint subclasses of C++ classes (character, game mode)
       Characters/     Wraith/, SisterVesper/, Enemies/
       Environments/   LanternMarket/, Shared/ (the modular gothic kit)
       Maps/
       Cinematics/
       UI/
       VFX/
       Audio/
       Data/           DT_ tables and data assets
       Dev/            test maps and experiments
     ```
     Fab packs install into their own folders under `/Game`. Leave them there, and use or copy what you need into `/Game/Wraith/`.
  2. **Move and rename assets only inside the Unreal Editor.** Unreal leaves small "redirector" files behind so references don't break. Now and then, right-click a folder and choose **Fix Up Redirectors**, then commit. Some 5.x versions call this **Update Redirector References**; `VERIFY:` the label in 5.8. Never move `.uasset` files in File Explorer or with `git mv`; that breaks references.
  3. **Revision control inside the editor.**
     - With **Git**, don't connect the built-in Git provider for now. It's labeled beta, and as a solo developer you can commit from the terminal or through Claude.
     - With **Perforce**, connect it (see the appendix).
  4. Keep the editor's autosave on (**Editor Preferences > General > Loading & Saving**). `VERIFY:` the location in 5.8.
- **Done when:** you know where every kind of asset goes. The folders will show up in Git once they contain assets, because Git doesn't track empty folders.
- **Common mistakes:**
  - Scattering assets at the top level of `/Game`.
  - Editing Fab packs in place and losing track of what you changed.
- **Claude can help:** Through the Unreal MCP (step 14), Claude can create the folders and later audit assets for naming-convention mistakes.
- **Time:** 15 minutes.

### Step 12. Commit, push, and run a restore test

A backup you haven't restored is only a hope.

- **Goal:** the remote contains everything needed to rebuild the project on a clean machine.
- **Do this:**
  1. Ask Claude to run `git status` and check that nothing from `Binaries/`, `Intermediate/`, `Saved/`, or `DerivedDataCache/` is staged.
  2. Run `git lfs ls-files` and check that the `.uasset` and `.umap` files are listed.
  3. Commit ("Create WraithGame C++ project on UE 5.8") and push.
  4. Clone into a new folder:
     ```powershell
     git clone https://github.com/<you>/<repo>.git C:\Dev\WraithRestoreTest
     cd C:\Dev\WraithRestoreTest
     git lfs ls-files
     ```
     In `git lfs ls-files`, an asterisk (`*`) after the ID means the full file was downloaded; a minus (`-`) means only the pointer is there.
  5. Generate Visual Studio project files for the copy, build it, open it, and press Play.
  6. Delete `C:\Dev\WraithRestoreTest` when you're done.
- **Done when:** the fresh clone opens with the same content and plays.
- **Common mistakes:**
  - Pointer files instead of content, because `git lfs install` wasn't run on that machine. Run `git lfs pull`.
  - Forgetting to commit `Config/` or `Source/`.
  - Restore tests use LFS bandwidth, which GitHub counts against the quota. That's cheap at this size, but keep it in mind once the repo is big.
- **Claude can help:** Claude can run every Git command and check the output. Opening the editor is manual.
- **Time:** 30–60 minutes.

### Step 13. Set up Blender and the Blender MCP

**MCP (Model Context Protocol)** is a standard way to give Claude tools. An MCP server exposes actions such as "list the scene objects" or "run this Python", and Claude calls them. The Blender MCP has two halves: an **add-on inside Blender** that listens on a local port, and a **server process** that Claude Code starts and that connects to it.

There are two Blender MCPs worth knowing:

| | MCP for Blender (ahujasid) | Blender Lab MCP server (official) |
|---|---|---|
| Made by | Community (about 29,500 GitHub stars) | Blender's own developers (Blender Lab); also listed as a Claude connector |
| License | MIT | GPL-3.0-or-later (from a secondary source; `VERIFY:`) |
| Blender version | 3.0+ | 5.1+ |
| Tools | Scene inspection, running Python, screenshots, export, asset integrations (Poly Haven, Sketchfab, AI 3D generators) | Running Python, file and object summaries, screenshots, renders, and search over Blender's API docs and manual |
| Telemetry | **On by default** (anonymous usage events); turned off with an environment variable | `VERIFY:` |
| Setup verified for this walkthrough | Yes, from its README | No. The setup wiki couldn't be read while writing |

**This walkthrough uses MCP for Blender** because its setup could be verified. The official Blender Lab server is a strong alternative, since it comes from Blender's own developers and its docs search helps Claude write correct code for your Blender version. See "Option B" at the end of this step.

- **Goal:** Claude Code can read and change your Blender scene.
- **Do this:**
  1. **Install Blender 5.2 LTS.** Get the newest 5.2.x Windows installer (about 350 MB) from https://www.blender.org/download/. LTS means it gets bug fixes for two years (until July 2028), so stay on it for the whole slice.
  2. **Turn on GPU rendering.** In Blender, go to **Edit > Preferences > System > Cycles Render Devices**, choose **HIP**, and tick the RX 9060 XT. Blender warns if the AMD driver is older than 24.9.1; you already have 25.6.1 or newer from step 1.
  3. **Install uv.** In PowerShell, run:
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```
     You can also use `winget install --id=astral-sh.uv -e`. Open a new terminal and run `uv --version`. The server's README warns against using `pip install uv`.
  4. **Install the add-on.** The README's one-liner:
     ```powershell
     uvx mcp-for-blender@2.1.1 install-addon
     ```
     If that doesn't work, download `addon.py` from the repo (link in References). Then in Blender go to **Edit > Preferences > Add-ons**, open the drop-down at the top right, choose **Install from Disk**, and pick the file. `VERIFY:` the menu labels in 5.2.
  5. **Enable the add-on.** In **Edit > Preferences > Add-ons**, enable **Interface: MCP for Blender**.
  6. **Connect.** In the 3D Viewport, press **N** to open the sidebar, open the **MCP for Blender** tab, and click **Connect to MCP server**. The add-on listens on port 9876. Older copies of the README call this button "Connect to Claude" or "Start MCP Server".
  7. **Register the server with Claude Code** from the repo root:
     ```powershell
     claude mcp add --env DISABLE_TELEMETRY=true --scope project --transport stdio blender -- uvx mcp-for-blender@2.1.1
     ```
     Why it's written this way:
     - `DISABLE_TELEMETRY=true` turns off the server's telemetry.
     - `--scope project` writes the entry to `.mcp.json` in the repo root, so it's saved in Git and comes back on any PC.
     - `@2.1.1` pins the version you tested. It was current on 2026-09-27. Check https://pypi.org/project/mcp-for-blender/ for newer versions and upgrade deliberately.
     - Everything after `--` is the command that starts the server.
     - Per Claude Code's docs, `--env` must not be immediately followed by the server name, which is why `--scope` sits between them.
  8. Run `claude mcp list`. Then start `claude` in the repo root, approve the project MCP server when it asks, and type `/mcp` to see its status.
  9. **Test task 1 (read).** Save a fresh Blender scene first. Then ask Claude:
     > Using the Blender MCP, list the objects in the current Blender scene.

     A new default scene has a cube, a camera, and a light.
  10. **Test task 2 (write).** Ask Claude:
      > In Blender, delete the default cube. Create a lantern post blockout named SM_LanternPost_Blockout: a square post 0.2 m wide and 3 m tall, with a 0.4 m cube on top. Join them into one mesh, put the origin at the bottom center, and stand it at the world origin. Then tell me its dimensions.

      Claude should ask permission before running Python, because of the `ask` rule from step 6. Check the result in the viewport. Keep the scene for step 15 and save it as `source-art/blender/environments/lantern-market/SM_LanternPost_Blockout.blend`.
- **Done when:** Claude lists the right objects, the post appears in Blender at the right size (3.4 m in total), and `.mcp.json` contains the `blender` entry.
- **Common mistakes:**
  - Forgetting to click **Connect** in Blender, or closing Blender. The MCP server has nothing to talk to.
  - Running two copies of the server, for example Claude Desktop and Claude Code at the same time. The README says to run only one.
  - Confusing the two projects. `uvx blender-mcp` still starts **ahujasid's** server (it was renamed), not the official Blender Lab one.
  - Leaving telemetry on by accident. Check that `.mcp.json` has the `DISABLE_TELEMETRY` entry.
- **Security:**
  - The code-execution tool runs any Python inside Blender. The README says to save your work before using it.
  - The connection between the add-on and the server has no authentication. Keep it on your own PC; never expose port 9876 to a network.
  - `BLENDER_MCP_SAFE_MODE=1` blocks file access, launching other programs, and network access. It also blocks exports, so don't use it for step 15.
  - Asset integrations: Poly Haven assets are CC0 (free, no credit needed). Many Sketchfab and Poly Pizza models are CC-BY and need credit. The optional AI 3D generators are third-party paid services with their own terms; Tencent's open-weights Hunyuan3D license excludes the EU, UK, and South Korea. Don't use any of them yet. Walkthroughs 03 and 06 cover asset licensing, and every asset's source should go in your asset list.
- **Option B: the official Blender Lab server.** `VERIFY:` all of the following against its setup wiki (link in References) before using it.
  - It needs Blender 5.1 or newer.
  - You install its add-on from the Blender Lab page, by allowing the Lab extension repository in Blender.
  - For Claude Code, the wiki gives a config that runs the server with `uv --directory <path-to-clone>/blender_mcp/mcp run blender-mcp` from a local clone of the repo.
  - Register it under a different name, such as `blender-lab`, and use only one Blender MCP at a time.
  - The test tasks are the same.
- **Claude can help:** After setup, a lot: scene inspection, blockout modeling, naming checks, and exports. Installing Blender, enabling the add-on, and clicking Connect are manual.
- **Time:** 45–75 minutes.

### Step 14. Set up the Unreal MCP (Epic's built-in plugin)

Unreal Engine 5.8 ships Epic's own **Unreal MCP** plugin, marked **Experimental**. It runs an MCP server inside the editor on your PC, and Epic's docs name Claude Code as a supported client. Experimental means rough edges. In June 2026 there were forum reports of the server not showing its tools and of dropped connections. `VERIFY:` whether those are fixed in 5.8.3. Commit before every MCP session.

- **Goal:** Claude Code can inspect and change the open level in the Unreal Editor.
- **Do this:**
  1. **Enable the plugins.** In the editor, go to **Edit > Plugins**, search for **Unreal MCP** and enable it, then search for **All Toolsets** and enable it. Restart the editor. The server exposes no tools unless All Toolsets is on.

     Claude can do the same by editing `WraithGame.uproject` with the editor closed, adding `{"Name": "ModelContextProtocol", "Enabled": true}` and `{"Name": "AllToolsets", "Enabled": true}` to the `Plugins` list. `VERIFY:` the plugin IDs against Epic's docs.
  2. **Start the server.** Turn on **Editor Preferences > General > Model Context Protocol > Auto Start Server**, or type `ModelContextProtocol.StartServer` into the console (the **Cmd** box at the bottom of the Output Log). The server listens at `http://127.0.0.1:8000/mcp`.
  3. **Register it with Claude Code** from the repo root:
     ```powershell
     claude mcp add --scope project --transport http unreal-mcp http://127.0.0.1:8000/mcp
     ```
     Epic also provides `ModelContextProtocol.GenerateClientConfig ClaudeCode`, which writes a `.mcp.json` next to `WraithGame.uproject`. Claude only reads that file if you start it inside `WraithGame/`. Using the command above keeps both MCP servers in the repo root's `.mcp.json`.
  4. Restart `claude` in the repo root, approve the new project server, and check `/mcp`. The server only shows as connected while the editor is running with the server started.
  5. **Optional:** Epic publishes a Claude Code plugin with Unreal skills (MIT license, in Anthropic's official plugin marketplace). Install it with `/plugin install unreal-engine-skills-for-claude-code@claude-plugins-official`. Its startup hook needs Git Bash, which you have. `VERIFY:` what it adds before relying on it.
  6. **Test task 1 (read).** Epic's own check. Ask Claude:
     > List all actors in the current level.

     The tool calls in Claude's output should be labeled with `unreal-mcp`.
  7. **Test task 2 (write, on a throwaway map).**
     - In the editor, use **File > New Level > Basic** and save it as `/Game/Wraith/Dev/MCP_TestMap`.
     - Ask Claude: "Spawn a cube named MCP_TestCube at (0, 0, 100) in the current level and tell me its location." Check the Outliner.
     - Then ask: "Delete MCP_TestCube."
  8. **Test task 3 (folders).** Ask Claude:
     > Create the /Game/Wraith folder layout from walkthrough 01, step 11.

     Check the Content Browser.
- **Done when:** all three tests work, and `.mcp.json` in the repo root contains both `blender` and `unreal-mcp`. Commit it.
- **Common mistakes:**
  - Enabling Unreal MCP but not **All Toolsets**, so Claude connects and finds no tools.
  - The server isn't running because the editor is closed or auto start is off.
  - Port 8000 is already used by something else. Change the port in the plugin settings, restart the editor, and update the URL in `.mcp.json`.
  - Starting Claude inside `WraithGame/` and wondering why the Blender MCP is missing.
- **Security (from Epic's docs):**
  - The server has no authentication and is meant only for use on the same PC. Epic's words: "Localhost is not a trust boundary."
  - One of its tools, `execute_tool_script`, runs arbitrary Python in the editor.
  - Epic advises against `--dangerously-skip-permissions`, and advises committing your work before long sessions.
- **If Epic's MCP doesn't work on your 5.8.x:**
  - Check the 5.8 hotfix notes first.
  - The community alternative that supports 5.8 is **ChiR24/Unreal_mcp** (MIT, actively updated; 5.8 support was a beta at the time of writing). `VERIFY:` its current status and setup before using it.
  - **VibeUE** (MIT) adds more tools on top of Epic's server if you later need more.
- **Claude can help:** Claude can edit the `.uproject` to enable the plugins (editor closed) and run the `claude mcp` commands. Restarting the editor and starting the server are manual.
- **Time:** 30–60 minutes.

### Step 15. Pipeline smoke test: Blender → Unreal

This proves the README's pipeline rule, "Blender makes the pieces, Unreal puts them together", at the correct scale. Blender works in meters and Unreal in centimeters. FBX files carry unit information, so a 3.4 m post in Blender should arrive as about 340 cm in Unreal.

- **Goal:** one real asset travels from Blender into an Unreal level at the right size.
- **Do this:**
  1. Ask Claude:
     > Using the Blender MCP, export SM_LanternPost_Blockout as FBX to source-art/blender/exports/SM_LanternPost_Blockout.fbx.
  2. Import it into `/Game/Wraith/Environments/LanternMarket/Blockout/`. Either ask Claude to do it through the Unreal MCP, or drag the FBX into the Content Browser and accept the import dialog. `VERIFY:` whether Epic's toolsets include FBX import; if not, doing it by hand is fine.
  3. Place it in `MCP_TestMap` a few meters from where the player spawns, press Play, and walk up to it. The mannequin is roughly 180 cm tall, so the post should be almost twice its height. For an exact check, switch a viewport to an orthographic view (Front or Side); holding the middle mouse button and dragging there measures distance.
  4. Commit the `.blend`, the `.fbx`, and the new `.uasset`.
- **Done when:** the post is about 340 cm tall in Unreal, stands on the ground at its base, and the commit is pushed.
- **Common mistakes:**
  - The asset arrives 100 times too big or too small. For static meshes this usually comes from Blender's unit scale settings; walkthroughs 04 and 06 cover export settings in detail.
  - The origin isn't at the base, so the post floats or sinks.
  - Exporting with Blender MCP safe mode on, which blocks file writes.
- **Claude can help:** Most of it, through both MCPs. Checking it by eye is yours.
- **Time:** 30 minutes.

### Step 16. Record your setup

- **Goal:** future sessions, and future you, know exactly what's installed.
- **Do this:** ask Claude to update:
  - `CLAUDE.md`: the engine version (exact hotfix), engine path, version control choice, MCP server names, and the build command.
  - `docs/ROADMAP.md`: tick the Milestone 1 items you've finished, and fill in the planning inputs.
  - Your hours log: how long this walkthrough took.

  Then commit and push.
- **Done when:** a new Claude session can answer "which engine version, where is it, how do I build?" from `CLAUDE.md` alone.
- **Common mistakes:** skipping this, then six months later not knowing which 5.8 hotfix the project is on.
- **Claude can help:** Fully.
- **Time:** 15 minutes.

---

## Vertical slice checklist

- [ ] `/Game/Wraith/` folders exist for the slice:
  - [ ] `Characters/Wraith`, `Characters/SisterVesper`
  - [ ] `Characters/Enemies/` with `ShieldedCultist`, `ChoirSinger`, `Snuffer`, and `Heavy`
  - [ ] `Environments/LanternMarket`, `Maps`, `Cinematics`, `UI`, `VFX`, `Audio`, `Data`, `Dev`
  - [ ] `Cinematics/ColdOpen` for the cold open
- [ ] Matching source-art folders exist:
  - [ ] `source-art/blender/characters/wraith`, `.../sister-vesper`, `.../enemies`
  - [ ] `source-art/blender/environments/lantern-market`
  - [ ] `source-art/marvelous/wraith-cloak`
  - [ ] `source-art/concept/` subfolders for Wraith, Vesper, the enemies, and Lantern Market
- [ ] Voice folders exist: `audio/voice/ja/cold-open` and `audio/voice/ja/district-01`
- [ ] `docs/story/` holds `wraith-story-bible-v2.md` and the cold open and District 1 scene scripts (walkthrough 02 organizes them)
- [ ] `.gitattributes` covers every file type the slice will produce; re-check it the first time you save from Marvelous Designer, Cascadeur, and your texturing tool
- [ ] `SM_LanternPost_Blockout` modeled through the Blender MCP, exported, and imported at the right scale: the first Lantern Market blockout piece
- [ ] `.mcp.json` in the repo root lists `blender` and `unreal-mcp`, and is committed
- [ ] `.claude/settings.json` ask-rules committed
- [ ] `CLAUDE.md` Commands section filled in; the engine hotfix version is recorded
- [ ] Restore test passed; the date is noted in the Milestone 1 checklist
- [ ] Hours for this walkthrough logged

## Going further

- **Engine debugging.** Add **Editor symbols for debugging**, and optionally Engine Source, through the engine tile's **Options** once you need to step into engine code. Check the size first.
- **Learning Unreal C++.** Before walkthrough 08, read Epic's C++ programming docs and follow one small C++ tutorial end to end. Tom Looman's site is a good source for C++ and GAS (References).
- **Git inside the editor.** If you want revision-control status icons in the Content Browser, try Project Borealis's UEGitPlugin (MIT, updated for 5.8). You compile it yourself, and it needs `bSCCAutoAddNewFiles=False` plus explicit `*.uasset` and `*.umap` attribute lines. Not needed while solo.
- **A second backup.** Git on GitHub is one off-site copy. Add a scheduled backup of the whole working folder to an external drive or a cloud backup service (the "3-2-1" rule: three copies, two kinds of storage, one off-site).
- **Claude Code habits.** Skills and custom commands for repeated tasks, such as "build and fix". Hooks that block edits to `.uasset` files. Epic's Unreal skills plugin. VibeUE for more Unreal MCP tools.
- **Claude Code on the web and big repos.** If you keep using cloud Claude Code sessions with this repo, `VERIFY:` how they handle Git LFS before the repo gets big. Pulling tens of GB of LFS files into a cloud session is slow and uses your bandwidth quota.
- **The future engine.** Epic has said 5.8 is the last planned major Unreal Engine 5 release (a 5.9 only if needed) and has targeted Unreal Engine 6 Early Access for the end of 2027. `VERIFY:` this came from a search excerpt of Epic's State of Unreal 2026 recap. Don't plan an engine move mid-production; if you ever consider one, do it at a milestone boundary after a tagged backup.

## If you choose Perforce instead (outline)

Use this in place of steps 5, 7, and 12. `VERIFY:` every step against Perforce's and Epic's current docs (links in References); the details couldn't be fully checked while this was written.

1. Download **P4 Server** (formerly Helix Core Server) and **P4V**, the free GUI client, from https://www.perforce.com/downloads.
2. Install the server on this PC (it can run as a background Windows service), on a NAS, or on a small cloud VM. If it runs on this PC, you **must** add an off-site backup of the server's data.
3. Create your user, a depot (or stream depot), and a mainline such as `//Wraith/main`.
4. **Set the typemap before adding any files**, as Epic's Perforce page instructs:
   - `binary+l` for `.uasset` and `.umap` (the `+l` means exclusive lock)
   - `binary+w` for `.exe`, `.dll`, and `.lib`
   - `text` for `.ini` and source files

   Copy Epic's full list from its page.
5. In P4V, create a workspace mapped to `C:\Dev\Wraith`.
6. Create a `.p4ignore` file with the same ignore rules as `WraithGame/.gitignore`, and point the `P4IGNORE` setting at it.
7. Add and submit the files. In the Unreal Editor, use **Revision Control > Connect to Revision Control > Perforce**.
8. Set up regular server checkpoints and copy the depot files off-site. Then do the restore test from step 12 using a fresh workspace.
9. Tell Claude in `CLAUDE.md` that the project uses Perforce and that it should use the `p4` command line.

## References

**Epic Games**
- Installing Unreal Engine: https://dev.epicgames.com/documentation/unreal-engine/install-unreal-engine
- Setting up Visual Studio for Unreal Engine: https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-visual-studio-development-environment-for-cplusplus-projects-in-unreal-engine
- Hardware and software specifications: https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-and-software-specifications-for-unreal-engine
- Unreal Engine 5.8 release notes: https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes
- Templates reference: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-templates-reference
- Template variants: https://dev.epicgames.com/documentation/en-us/unreal-engine/variants-in-game-templates
- Unreal MCP in Unreal Editor: https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor
- Epic's Claude Code plugin: https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin
- Python scripting in the editor: https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python
- Source control in Unreal Engine: https://dev.epicgames.com/documentation/en-us/unreal-engine/source-control-in-unreal-engine
- Using Perforce with Unreal Engine: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine
- Unreal Engine license and royalties: https://www.unrealengine.com/license

**Microsoft**
- Visual Studio Community: https://visualstudio.microsoft.com/vs/community/
- Visual Studio 2026 system requirements: https://learn.microsoft.com/en-us/visualstudio/releases/2026/vs-system-requirements
- Visual Studio Tools for Unreal Engine: https://learn.microsoft.com/en-us/visualstudio/gamedev/unreal/get-started/vs-tools-unreal-install
- Import a Visual Studio installer configuration (`.vsconfig`): https://learn.microsoft.com/en-us/visualstudio/install/import-export-installation-configurations
- Windows maximum path length: https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation

**Version control**
- Git for Windows: https://git-scm.com/downloads/win
- Git LFS: https://git-lfs.com
- Git LFS file locking: https://github.com/git-lfs/git-lfs/wiki/File-Locking
- GitHub Git LFS billing: https://docs.github.com/en/billing/concepts/product-billing/git-lfs
- About Git LFS on GitHub: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage
- GitHub's Unreal `.gitignore` template: https://github.com/github/gitignore/blob/main/UnrealEngine.gitignore
- Azure DevOps Git LFS: https://learn.microsoft.com/en-us/azure/devops/repos/git/manage-large-files
- Azure DevOps limits: https://learn.microsoft.com/en-us/azure/devops/repos/git/limits
- Perforce free tier: https://www.perforce.com/products/helix-core/free-version-control
- Perforce downloads: https://www.perforce.com/downloads
- Project Borealis UEGitPlugin: https://github.com/ProjectBorealis/UEGitPlugin

**Claude Code**
- Setup: https://code.claude.com/docs/en/setup
- Quickstart: https://code.claude.com/docs/en/quickstart
- Installation troubleshooting: https://code.claude.com/docs/en/troubleshoot-install
- MCP: https://code.claude.com/docs/en/mcp
- CLAUDE.md and memory: https://code.claude.com/docs/en/memory
- Permissions: https://code.claude.com/docs/en/permissions
- Permission modes: https://code.claude.com/docs/en/permission-modes
- Pricing: https://claude.com/pricing

**Blender and the Blender MCPs**
- Blender download: https://www.blender.org/download/
- Blender LTS: https://www.blender.org/download/lts/
- Blender license: https://www.blender.org/about/license/
- GPU rendering (Cycles, HIP): https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
- MCP for Blender (ahujasid): https://github.com/ahujasid/mcp-for-blender
- MCP for Blender on PyPI: https://pypi.org/project/mcp-for-blender/
- Blender Lab MCP server: https://www.blender.org/lab/mcp-server/
- Blender Lab MCP repo and setup wiki: https://projects.blender.org/lab/blender_mcp
- uv: https://github.com/astral-sh/uv

**AMD**
- Drivers: https://www.amd.com/en/support/download/drivers.html
- FSR plugin for Unreal Engine (walkthrough 07): https://gpuopen.com/learn/ue-fsr/

**Recommended learning channels**
- Unreal Engine on YouTube (official): https://www.youtube.com/@UnrealEngine
- Epic Developer Community learning library: https://dev.epicgames.com/community/unreal-engine/learning
- Tom Looman (Unreal C++ and GAS): https://www.tomlooman.com
