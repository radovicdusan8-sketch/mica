# 02. Story and Dialogue Pipeline

> **Written for:** Unreal Engine 5.8 (5.8.3): Data Tables, editor Python, and the **Subtitles and Closed Captions** plugin (Beta in 5.8). Python 3.9+ for the repo tools. Google Sheets, LibreOffice Calc, or Excel.
> **Facts checked:** 2026-09-27. Epic's documentation was blocked from this environment, so several engine behaviors (CSV encoding, localization keys, reimport rules) were confirmed by reading Unreal's engine source code for 5.6.1 and 5.8.2 in third-party mirrors. You can confirm them in your own `UE_5.8/Engine/Source`. Unconfirmed items are marked `VERIFY:`.

## What this covers

This walkthrough takes the story from documents to spoken, subtitled lines in the game:

- how `docs/story/` is organized;
- a permanent ID for every line;
- a scene-script format a program can read;
- a dialogue spreadsheet (line ID, speaker, Japanese line, English subtitle, audio file, scene, and a few production columns), exported as UTF-8 CSV;
- a validator that catches mistakes before Unreal sees them;
- C++ row structs and Data Tables imported by hand or by script;
- voice files linked to lines by name;
- a line playing in-engine with its subtitle.

It ends with change control, so recorded audio and text never drift apart.

## Why it matters for Wraith

- **Most players will read the whole story.** The voice acting is Japanese and the subtitles are English, so for anyone who doesn't speak Japanese, subtitles are the story. Their timing, length, and readability matter as much as the writing.
- **Every line is three things that must stay in sync:** the Japanese text an actor performs, the English subtitle, and the recorded audio file. A 10+ hour story means these triples number in the thousands. A small mismatch, like a changed line that was never re-recorded, is easy to make and hard to find by hand.
- **Fights and reading don't mix.** Wraith is a fast brawler. Lines spoken during combat must be short, or players miss them. The validator flags long subtitles and fast reading speeds.
- **Localization later is cheap only if you prepare now.** Stable IDs and Unreal's text system (`FText`) make adding more subtitle languages a process, not a rewrite (walkthrough 16).
- **Solo and part-time.** Automation (one command to validate, one to import) replaces hours of careful manual checking.

## Tools

| Tool | What it's for | Cost | Commercial license OK? | AMD notes |
|---|---|---|---|---|
| Any Markdown editor (VS Code is a good free choice) | Story bible and scene scripts | Free | Yes | None |
| Google Sheets | The dialogue spreadsheet | Free with a Google account | Yes | None |
| LibreOffice Calc or Microsoft Excel (alternatives) | The dialogue spreadsheet, offline | LibreOffice free; Excel needs a Microsoft 365 subscription | Yes | None |
| Python 3.9+ | `tools/dialogue/dialogue_tool.py` (validate, export, report) | Free | Yes | None |
| Unreal Data Tables and editor Python | Holding lines in the game; scripted import | Free (engine) | Yes | None |
| Subtitles and Closed Captions plugin (ships with UE 5.8, **Beta**) | Showing subtitles, including a Sequencer subtitle track | Free (engine) | Yes | None |
| Optional: articy:draft X, Ink (Inkpot plugin), Yarn Spinner | Branching-dialogue editors with Unreal importers | articy:draft X FREE covers 700 objects per project and allows commercial use; paid plans from about €5.99/month. Inkpot is MIT. Yarn Spinner for Unreal is pre-release and not recommended for shipping. | articy FREE and Inkpot: yes | None |

**Wraith is linear, so you don't need a branching-dialogue tool.** A spreadsheet is simpler, and for a 10-hour game articy's free 700-object limit would run out.

## Before you start

- **Walkthroughs done:** 01. Command-line builds (01, step 10) are used in step 8.
- **Files already in the repo:**
  - `docs/story/README.md`: the ID rules;
  - `docs/story/scene-index.md`;
  - `docs/story/dialogue/speakers.csv`;
  - `docs/story/dialogue/dialogue_master.example.csv`;
  - `tools/dialogue/dialogue_tool.py`;
  - `tools/unreal/import_dialogue.py`.
- **Your story files:** `wraith-story-bible-v2.md` and the scene scripts.
- **A fluent Japanese reviewer.** The Japanese lines are what actors perform and what Japanese-speaking players hear. Claude can draft and check Japanese and English, but a fluent human must review both before anything is recorded. Budget for it (walkthrough 15 covers casting and recording).

## The pipeline at a glance

```text
docs/story/scenes/*.md            write and draft here (with Claude's help)
        │  a scene is ready: its lines go into the sheet
        ▼
Google Sheet "Wraith Dialogue"    the master for every line once it's Locked
        │  File > Download > CSV (UTF-8)
        ▼
docs/story/dialogue/dialogue_master.csv
        │  python tools/dialogue/dialogue_tool.py validate / export
        ▼
docs/story/dialogue/build/DT_Dialogue.json, DT_Speakers.json
        │  tools/unreal/import_dialogue.py (inside Unreal)
        ▼
/Game/Wraith/Data/Dialogue/DT_Dialogue, DT_Speakers
        │  UWDialogueSubsystem::PlayLine("D01_S020_0030")
        ▼
Sound Wave VO_D01_S020_0030 plays  +  subtitle shown (Subtitles plugin or your widget)
```

---

## Steps

### Step 1. Organize `docs/story`

- **Goal:** the story lives in the repo in a predictable layout that Claude and the tools can read.
- **Do this:**
  1. Copy `wraith-story-bible-v2.md` into `docs/story/` and the scene scripts into `docs/story/scenes/`. Commit them before changing anything, so you keep the originals.
  2. Read `docs/story/README.md`. It defines the folder layout and ID rules used everywhere below.
  3. Fill `docs/story/scene-index.md`: one row per scene in story order, with its ID, title, district, type (Cinematic, In-game, or Barks), speakers, and status. The cold open is `D00_S010`.
  4. In the story bible, add or check a **Characters** section that lists each speaking character's speaker ID from `speakers.csv`. Fill the **IsDead** column in `speakers.csv` for everyone: the dead's subtitle names can use Spirit violet and the living's Lantern gold, following the art rules. That's optional styling, but the column should be accurate.
- **Done when:** every scene in the story bible has a row in the scene index, and every speaking character has a speaker ID.
- **Common mistakes:**
  - Keeping the story bible outside the repo, so it drifts from what's in the game.
  - Inventing speaker IDs ad hoc in scripts. Add them to `speakers.csv` first.
- **Claude can help:** a lot. Claude can read the story bible and draft the scene index and speaker list for you to correct, and flag scenes that are mentioned but not written.
- **Time:** 1–2 hours.

### Step 2. Adopt the line ID scheme

An ID is a line's permanent name. It becomes the voice file's name, the Data Table row, and the subtitle's localization key.

- **Goal:** every spoken line has an ID that never changes.
- **Do this:** use the formats in `docs/story/README.md`:

  | What | Format | Example |
  |---|---|---|
  | Scene line | `D<district>_S<scene>_<line>` | `D01_S020_0030` |
  | Bark (short combat or ambient line) | `B_<SPEAKER>_<EVENT>_<nn>` | `B_VESPER_PHASE2_01` |
  | Voice file | `VO_<LineID>.wav` | `VO_D01_S020_0030.wav` |
  | Sound Wave in Unreal | `/Game/Wraith/Audio/VO/<D01 or Barks>/VO_<LineID>` | `/Game/Wraith/Audio/VO/D01/VO_D01_S020_0030` |

  Rules:
  - **Number in steps of 10**, so a new line can go between two old ones (`0015`).
  - **Never renumber and never reuse.** A cut line's ID is gone for good.
  - **Barks** are grouped by speaker and event (hit, attack, taunt, phase change). Plan several variants per event (`_01` to `_04`) so repetition isn't grating.
- **Suggested addition to the README's prefixes:** `VO_` for voice Sound Waves. The README doesn't list a prefix for sounds; add this one there if you agree.
- **Done when:** the ID rules are agreed, and any existing script has been numbered (next step).
- **Common mistakes:**
  - Renumbering "to make it tidy". That breaks audio file names and localization keys.
  - Encoding the speaker in scene-line IDs. The speaker is a column, because who says a line can change.
- **Claude can help:** Claude can number every line in existing scripts and keep the scene index in sync.
- **Time:** 15 minutes to agree; numbering is part of step 3.

### Step 3. Write scene scripts in a readable line format

- **Goal:** scene scripts that read well for you and can be parsed exactly by a program.
- **Do this:**
  1. One file per scene: `docs/story/scenes/D01_S020_<short-slug>.md`.
  2. Use this format. The README in `docs/story/` shows it too; the lines below are a **format example, not script**:
     ```markdown
     # D00_S010: Cold open

     **Where:** ...  **When:** ...  **Who:** WRAITH

     > Stage directions go in quote blocks: what we see, camera ideas, sounds.

     [D00_S010_0010] WRAITH: 灯りが消えた。
     EN: The lantern has gone out.
     DIRECTION: Quiet, flat.
     ```
     - The first line of each spoken line is `[LineID] SPEAKER: Japanese text`.
     - `EN:` is the English subtitle.
     - `DIRECTION:` is an acting note for the voice actor. Players never see it.
     - Leave a blank line between spoken lines.
  3. If you prefer screenplay formatting, **Fountain** is a plain-text screenplay format with free editors: Trelby on Windows, Afterwriting on the web, and the "Better Fountain" extension for VS Code. The line IDs still have to be there, for example as a note on each line. Mixing formats makes parsing harder, so pick one.
  4. **In-combat lines:** mark them with `TAGS: COMBAT` and keep them very short. A subtitle of four to six words is readable mid-fight; a sentence isn't.
- **Done when:** the cold open and the District 1 scenes are in this format, with an ID on every line.
- **Common mistakes:**
  - Putting the subtitle and the Japanese on the same line, so a program can't split them reliably.
  - Leaving lines without IDs "until later". Later, the audio file names depend on them.
- **Claude can help:** Claude can convert existing scripts to this format, number lines, check that every line has `EN:`, and point out lines that are too long for combat.
- **Time:** depends on the script. Conversion is quick with Claude; writing is the real work.

### Step 4. Build the dialogue spreadsheet

- **Goal:** a Google Sheet that holds every line, with guard rails that stop common mistakes.
- **Do this:**
  1. Create a Google Sheet named **Wraith Dialogue** with two tabs, **Lines** and **Speakers**.
  2. On **Lines**, put these headers in row 1, spelled exactly like this:

     | Column | Content | Rules |
     |---|---|---|
     | `LineID` | `D01_S020_0030` | Unique, permanent |
     | `SceneID` | `D01_S020` | First 8 characters of the LineID; empty for barks |
     | `Order` | 10, 20, 30… | Playback order inside the scene |
     | `Speaker` | `MAREN` | Must exist on the Speakers tab |
     | `TextJA` | The Japanese line | What the actor performs |
     | `TextEN` | The English subtitle | No line breaks; the subtitle widget wraps it |
     | `Direction` | Acting note | Not shown to players |
     | `Context` | What's happening | For translators and reviewers |
     | `Status` | Draft, Locked, Recorded, Implemented | Only moves forward |
     | `Tags` | `COMBAT`, `BARK`, `CINEMATIC`… | Separated by `;` |

     You can add more columns for your own use, such as `ReadingJA` (readings for difficult kanji and names, for the actors) or `Take` (the chosen take). The tool ignores columns it doesn't know.
  3. On **Speakers**, use the headers `SpeakerID, NameEN, NameJA, IsDead, Notes`, and paste in the rows from `docs/story/dialogue/speakers.csv`.
  4. **Guard rails:**
     - **View > Freeze > 1 row**, so the headers stay visible.
     - **Data > Data validation** on the Status column: a dropdown with the four statuses.
     - **Data > Data validation** on the Speaker column: a dropdown from the range `Speakers!A2:A`.
     - **Format > Conditional formatting** on the TextEN column: a custom formula `=LEN(F2)>84` with a red fill, so long subtitles stand out.
     - **Data > Protect sheets and ranges**: protect row 1, so headers can't be renamed by accident.
  5. **The master rule, to avoid two sources of truth:**
     - While a scene is **Draft**, its Markdown script is the master; write there.
     - When you move it to **Locked** (text final, ready to record), paste its lines into the sheet. From then on **the sheet is the master**.
     - Claude can regenerate the script file from the sheet whenever you want them to match again.
- **Done when:** the sheet exists with both tabs and all guard rails, and the cold open's lines are in it.
- **Common mistakes:**
  - Renaming a header, so the tool rejects the file.
  - Editing a Locked line in the Markdown script and forgetting the sheet.
  - Typing line breaks into subtitles.
- **Claude can help:** Claude can turn a scene file into rows you paste into the sheet, and turn sheet rows back into a scene file. It can't log in to your Google account; you do the copying and pasting (or see "Going further" for automation).
- **Time:** 1 hour to set up.

### Step 5. Export CSV correctly (UTF-8)

Unreal reads CSV files as UTF-8 (or as UTF-16 when the file starts with a byte-order mark). It has **no** support for Shift-JIS or other Windows code pages, so a CSV saved in the wrong encoding turns Japanese into garbage.

- **Goal:** `dialogue_master.csv` and `speakers.csv` on disk, in UTF-8.
- **Do this:**
  - **Google Sheets** (recommended): on the Lines tab, **File > Download > Comma-separated values (.csv)**. It downloads only the current tab, in UTF-8. Save it as `docs/story/dialogue/dialogue_master.csv`. Do the same on the Speakers tab for `speakers.csv`.
  - **Excel:** **File > Save As**, type **CSV UTF-8 (Comma delimited)**. Plain "CSV (Comma delimited)" uses the Windows code page and destroys Japanese text.
  - **LibreOffice Calc:** **File > Save As**, type **Text CSV**, tick **Edit filter settings**, and choose character set **Unicode (UTF-8)** with a comma as the field delimiter.
- **Done when:** opening the CSV in VS Code shows the Japanese correctly, and VS Code's status bar says UTF-8 (or UTF-8 with BOM, which also works).
- **Common mistakes:** Excel's default CSV type. If Japanese looks like `ç¯ã‚Š` or `???`, the encoding is wrong.
- **Claude can help:** Claude can check a CSV's encoding and fix a broken one if the original data survives.
- **Time:** 2 minutes per export.

### Step 6. Validate and export with the dialogue tool

- **Goal:** catch mistakes before they reach Unreal, and produce the files Unreal imports.
- **Do this:** from the repo root:
  ```powershell
  python tools/dialogue/dialogue_tool.py validate
  python tools/dialogue/dialogue_tool.py export
  python tools/dialogue/dialogue_tool.py report
  ```
  - **validate** checks:
    - ID formats and duplicates;
    - that SceneID matches the LineID;
    - Order numbers;
    - that every speaker exists;
    - statuses;
    - that Locked lines have both Japanese and English;
    - that subtitles have no line breaks and aren't over 84 characters (about two lines of 42);
    - that Recorded lines have their WAV file;
    - reading speed: the subtitle's characters per second of audio, warning above 20.

    Errors stop the export; warnings don't.
  - **export** writes `docs/story/dialogue/build/DT_Dialogue.json` and `DT_Speakers.json`. Japanese is stored as `\uXXXX` escapes, so the file is plain ASCII and encoding can't go wrong on import. The `Audio` field is only filled when the WAV exists.
  - **report** prints lines per status, scene, and speaker, plus Japanese character counts per speaker, which is useful for booking voice actors.
- **Subtitle guidelines** behind the checks:
  - Two lines of about 42 characters.
  - Reading speed under about 20 characters per second.

  These follow common broadcast and streaming subtitle practice. `VERIFY:` pick your final numbers with walkthrough 13's accessibility settings and adjust `MAX_SUBTITLE_CHARS` and `MAX_CHARS_PER_SECOND` at the top of the tool.
- **Done when:** `validate` reports 0 errors for the slice's lines, and the two JSON files exist.
- **Common mistakes:**
  - Ignoring reading-speed warnings. For combat lines they're real problems.
  - Hand-editing the JSON. It's regenerated every export; fix the sheet instead.
- **Claude can help:** fully. Claude runs the tool, explains each finding, and proposes fixes. It can also add new checks to the tool, such as banned words or terminology consistency with a glossary.
- **Time:** 5 minutes per run.

### Step 7. Decide how the text will be localized (a quick check, before any import)

- **Goal:** understand how subtitle text gets its localization key, so nothing you do now breaks translation later.
- **Do this:** read these points; they shape how you work from step 8 on.
  - Unreal's localizable text type is **`FText`**. When a Data Table is imported, each `FText` cell gets a **stable key** built from the row name and property name, in a namespace named after the table asset. For example, `D01_S020_0030_Subtitle` in namespace `DT_Dialogue`. (Confirmed in engine source for 5.6.1 and 5.8.2.)
  - So: **never rename a line ID, the `Subtitle` property, or the `DT_Dialogue` asset** once translation starts. Any of those changes the keys, and existing translations stop matching.
  - Data Table `FText` is collected by the Localization Dashboard's **Gather from Packages** (walkthrough 16).
  - `SpokenJA` is a plain string (`FString`) on purpose, so it isn't gathered as English source text. The Japanese lines return in walkthrough 16 as the **Japanese subtitle translation** for Japanese-speaking players, generated from the same sheet.
  - Voice audio isn't localized: every player hears Japanese. If you ever add another voice language, Unreal supports per-language assets and separate voice and text languages. That's walkthrough 16's topic.
- **Done when:** you've read this. There's nothing to click.
- **Common mistakes:**
  - Renaming `DT_Dialogue`, the `Subtitle` property, or line IDs after translation has started.
  - Storing the English subtitle as a plain string (`FString`), which the localization tools can't gather.
- **Claude can help:** Claude can explain any of this in more depth, and later generate the translation files.
- **Time:** 10 minutes.

### Step 8. Add the C++ row structs, settings, and dialogue subsystem

A **row struct** defines a Data Table's columns. A **subsystem** is an object Unreal creates automatically, one per world here, that any code can ask to do something. `PlayLine` lives there.

- **Goal:** the C++ types Data Tables need, a Project Settings page to pick the tables, and a `PlayLine(LineID)` function.
- **Do this:** ask Claude to add these files to `WraithGame/Source/WraithGame/` (this is the reference version), then build (walkthrough 01, step 10).
  1. **`WDialogueTypes.h`:**
     ```cpp
     #pragma once

     #include "CoreMinimal.h"
     #include "Engine/DataTable.h"
     #include "WDialogueTypes.generated.h"

     class USoundBase;

     /** One row of DT_Speakers. Row name = speaker ID, for example WRAITH. */
     USTRUCT(BlueprintType)
     struct WRAITHGAME_API FWSpeakerRow : public FTableRowBase
     {
         GENERATED_BODY()

         UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Speaker")
         FText DisplayName;

         /** The dead can be shown in Spirit violet, the living in Lantern gold. */
         UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Speaker")
         bool bIsDead = false;
     };

     /** One row of DT_Dialogue. Row name = line ID, for example D01_S020_0030. */
     USTRUCT(BlueprintType)
     struct WRAITHGAME_API FWDialogueLineRow : public FTableRowBase
     {
         GENERATED_BODY()

         UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Dialogue")
         FName SceneId;

         UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Dialogue")
         int32 Order = 0;

         /** Row name in DT_Speakers. */
         UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Dialogue")
         FName Speaker;

         /** The Japanese line as recorded. Kept for tools and lip sync; players see Subtitle. */
         UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Dialogue")
         FString SpokenJA;

         /** English subtitle; localized through Unreal's localization tools (walkthrough 16). */
         UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Dialogue")
         FText Subtitle;

         UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Dialogue")
         TSoftObjectPtr<USoundBase> Audio;
     };
     ```
     `TSoftObjectPtr` is a reference that doesn't load the sound until you ask for it, so a table of thousands of lines doesn't load thousands of sounds.
  2. **`WDialogueSettings.h`** adds a **Project Settings > Game > Wraith Dialogue** page:
     ```cpp
     #pragma once

     #include "CoreMinimal.h"
     #include "Engine/DeveloperSettings.h"
     #include "WDialogueSettings.generated.h"

     class UDataTable;

     UCLASS(Config = Game, DefaultConfig, meta = (DisplayName = "Wraith Dialogue"))
     class WRAITHGAME_API UWDialogueSettings : public UDeveloperSettings
     {
         GENERATED_BODY()

     public:
         UPROPERTY(Config, EditAnywhere, Category = "Tables")
         TSoftObjectPtr<UDataTable> DialogueTable;

         UPROPERTY(Config, EditAnywhere, Category = "Tables")
         TSoftObjectPtr<UDataTable> SpeakerTable;
     };
     ```
  3. **`WDialogueSubsystem.h`:**
     ```cpp
     #pragma once

     #include "CoreMinimal.h"
     #include "Subsystems/WorldSubsystem.h"
     #include "WDialogueSubsystem.generated.h"

     DECLARE_DYNAMIC_MULTICAST_DELEGATE_FourParams(FWOnLineStarted,
         FName, LineId, FText, SpeakerName, FText, Subtitle, float, Duration);

     /** Plays dialogue lines by ID and tells the subtitle display what to show. */
     UCLASS()
     class WRAITHGAME_API UWDialogueSubsystem : public UWorldSubsystem
     {
         GENERATED_BODY()

     public:
         /** Plays the line's voice (attached to SpeakerActor if given, otherwise 2D) and broadcasts OnLineStarted. */
         UFUNCTION(BlueprintCallable, Category = "Wraith|Dialogue")
         void PlayLine(FName LineId, AActor* SpeakerActor = nullptr);

         /** The subtitle display binds to this (step 11). */
         UPROPERTY(BlueprintAssignable, Category = "Wraith|Dialogue")
         FWOnLineStarted OnLineStarted;

     private:
         /** How long to show a subtitle for a line that has no audio yet. */
         static float EstimateDuration(const FText& Subtitle);
     };
     ```
  4. **`WDialogueSubsystem.cpp`:**
     ```cpp
     #include "WDialogueSubsystem.h"

     #include "WDialogueSettings.h"
     #include "WDialogueTypes.h"
     #include "Engine/DataTable.h"
     #include "Kismet/GameplayStatics.h"
     #include "Sound/SoundBase.h"

     void UWDialogueSubsystem::PlayLine(FName LineId, AActor* SpeakerActor)
     {
         const UWDialogueSettings* Settings = GetDefault<UWDialogueSettings>();
         const UDataTable* Lines = Settings->DialogueTable.LoadSynchronous();
         if (!Lines)
         {
             UE_LOG(LogTemp, Warning, TEXT("PlayLine: set the Dialogue Table in Project Settings > Wraith Dialogue"));
             return;
         }

         const FWDialogueLineRow* Line = Lines->FindRow<FWDialogueLineRow>(LineId, TEXT("PlayLine"));
         if (!Line)
         {
             return; // FindRow has already logged the missing row
         }

         FText SpeakerName = FText::FromName(Line->Speaker);
         if (const UDataTable* Speakers = Settings->SpeakerTable.LoadSynchronous())
         {
             if (const FWSpeakerRow* Speaker = Speakers->FindRow<FWSpeakerRow>(Line->Speaker, TEXT("PlayLine")))
             {
                 SpeakerName = Speaker->DisplayName;
             }
         }

         float Duration = EstimateDuration(Line->Subtitle);
         // Synchronous loading keeps this simple; walkthrough 17 moves it to async loading if it ever hitches.
         if (USoundBase* Sound = Line->Audio.LoadSynchronous())
         {
             Duration = Sound->GetDuration();
             if (SpeakerActor && SpeakerActor->GetRootComponent())
             {
                 UGameplayStatics::SpawnSoundAttached(Sound, SpeakerActor->GetRootComponent());
             }
             else
             {
                 UGameplayStatics::SpawnSound2D(this, Sound);
             }
         }

         OnLineStarted.Broadcast(LineId, SpeakerName, Line->Subtitle, Duration);
     }

     float UWDialogueSubsystem::EstimateDuration(const FText& Subtitle)
     {
         // About 15 characters per second, and never shorter than 1.5 seconds.
         return FMath::Max(1.5f, Subtitle.ToString().Len() / 15.0f);
     }
     ```
  5. In `WraithGame.Build.cs`, add `"DeveloperSettings"` to `PublicDependencyModuleNames`. `UDeveloperSettings` lives in that module.
  6. Close the editor and build.
- **Done when:** the build succeeds, and the editor shows **Project Settings > Game > Wraith Dialogue** with two table slots.
- **Common mistakes:**
  - Forgetting the `DeveloperSettings` module, which gives link errors mentioning `UDeveloperSettings`.
  - Using Live Coding for these changes. New structs and classes need a full build with the editor closed.
- **Claude can help:** fully. Claude writes the files, edits `Build.cs`, builds from the command line, and fixes compile errors.
- **Time:** 30–60 minutes.

### Step 9. Import the tables into Unreal

- **Goal:** `DT_Dialogue` and `DT_Speakers` exist in `/Game/Wraith/Data/Dialogue/`, filled from the JSON, with stable text keys.
- **Do this:**
  1. **By hand, the first time**, so you see what happens:
     - Drag `docs/story/dialogue/build/DT_Speakers.json` into the Content Browser folder `/Game/Wraith/Data/Dialogue/`.
     - When asked for the **Data Table Row Type**, pick `WSpeakerRow`. Unreal names reflected structs without the `F`.
     - The asset is named after the file, `DT_Speakers`.
     - Repeat with `DT_Dialogue.json` and `WDialogueLineRow`.
  2. **Set the tables** in **Project Settings > Game > Wraith Dialogue**.
  3. **Check a row** by opening `DT_Dialogue`:
     - The Japanese should display correctly.
     - `Subtitle` should be the English text.
     - Hovering or opening the text field's localization options should show the key `<LineID>_Subtitle` in namespace `DT_Dialogue`. `VERIFY:` where 5.8's editor shows an `FText`'s key and namespace.
  4. **Updates:**
     - Run `dialogue_tool.py export` again.
     - Then either right-click each table and choose **Reimport**, or run the script inside Unreal:
       ```python
       exec(open(r"C:/Dev/Wraith/tools/unreal/import_dialogue.py", encoding="utf-8").read())
       ```
       Type it in the Output Log with the command box set to **Python**.
     - The script also imports new voice files (step 10). It creates the tables if they don't exist, refills them, and prints the row count; check that the count is right.
  5. **Know the reimport rule:** a JSON reimport **empties the table and refills it**. Rows deleted from the sheet disappear from the table. That's what you want, because the sheet is the master.
- **Done when:** both tables exist, show the right row counts and correct Japanese, and a reimport after changing one subtitle updates it.
- **Common mistakes:**
  - Picking the wrong row struct at import.
  - Editing rows inside the Unreal table editor. The next reimport erases those edits; change the sheet instead.
  - Renaming the Data Table assets later, which changes every localization key (step 7).
- **Claude can help:** fully, through the Unreal MCP. Claude can run `import_dialogue.py`, read the row counts, and spot-check rows. `VERIFY:` the script is written against the 5.8 Python API (functions confirmed in Epic's API docs and engine source) but hasn't been run in your editor. Try it on a copy of the project, or on a fresh commit you can revert.
- **Time:** 30 minutes the first time, then under a minute.

### Step 10. Import the voice audio

- **Goal:** every recorded line's WAV becomes a Sound Wave whose name matches its line ID, so `DT_Dialogue` finds it automatically.
- **Do this:**
  1. **File spec.** Walkthrough 15 sets the final recording spec; until then use mono WAV at 48 kHz, 16- or 24-bit.
  2. **Place each file** at `audio/voice/ja/<D01 or Barks>/VO_<LineID>.wav` in the repo. The folder must match the ID's district, or `Barks`.
  3. **Import:** run `tools/unreal/import_dialogue.py` inside Unreal (step 9). It imports any `VO_*.wav` that doesn't have a Sound Wave yet into `/Game/Wraith/Audio/VO/<folder>/`. Set `REIMPORT_EXISTING = True` at the top of the script when you replace takes.
  4. **Set each line's Status to Recorded** in the sheet, then export and reimport the tables. The export fills in the `Audio` path for lines whose WAV exists.
  5. **Sound settings:** walkthrough 15 adds a Sound Class for dialogue (for the volume slider) and compression settings. Nothing is needed yet.
- **Done when:** a recorded line's row in `DT_Dialogue` points at its Sound Wave, and double-clicking the Sound Wave plays the right line.
- **Common mistakes:**
  - A file name that doesn't match the ID exactly, such as `VO_D01_S20_0030.wav`. The validator warns when Recorded lines have no file.
  - Stereo voice files. Voice is mono; stereo doubles memory and complicates 3D positioning.
- **Claude can help:** Claude can rename batches of recorded files to the ID scheme (from a list or from take sheets), check the files (sample rate, channels, length), and run the import.
- **Time:** 10 minutes per batch.

### Step 11. Play a line and show its subtitle

- **Goal:** calling `PlayLine("D00_S010_0010")` plays the audio (or waits the estimated time) and shows the subtitle with the speaker's name.
- **Do this, using the Subtitles plugin (recommended):**
  1. **Edit > Plugins** and enable **Subtitles and Closed Captions**. It's **Beta** in 5.8 and needs the **ViewportWidgetOverlay** plugin, which the editor offers to enable. Restart.

     This plugin is Epic's replacement for the old subtitle system. It shows subtitles through a UMG widget and has a Sequencer subtitle track (used in walkthrough 12). It also supports closed captions (sound descriptions such as "[a lantern gutters out]") and audio descriptions.
  2. Create a widget Blueprint `WBP_Subtitles` that subclasses the plugin's **Subtitle Widget** class. Walkthrough 13 styles it; for now keep the default look. Select it under **Project Settings > Subtitles And Closed Captions**. `VERIFY:` the exact setting name.
  3. **Glue it together in Blueprint** (Blueprints for thin glue, per the README). In your game mode or HUD Blueprint, on Begin Play:
     - get the **WDialogueSubsystem**;
     - bind **OnLineStarted**;
     - in the bound event, call the plugin's **Queue Single Subtitle** node with the text `{SpeakerName}: {Subtitle}` (a **Format Text** node) and the given duration.

     `VERIFY:` the node's exact name and pins in 5.8. The plugin's Blueprint library also has Queue Subtitles From Asset, Stop Subtitles In Asset, and Replace Subtitle Widget.
  4. **Test:** in a test map's Level Blueprint, on a key press, call **Play Line** with `D00_S010_0010`. You should see the subtitle for the audio's length. When there's no audio yet, it shows for an estimated time: about one second per 15 characters, and at least 1.5 seconds.
- **Fallback, if the Beta plugin gives you trouble:** make your own UMG widget, bind it to **OnLineStarted**, and show the text for `Duration` seconds. Walkthrough 13 builds this properly either way. Keeping the plugin out of the C++ means switching approaches only changes Blueprint glue.
- **Done when:** pressing the test key plays the line with a visible subtitle and speaker name, and it disappears when the audio ends.
- **Common mistakes:**
  - Binding the delegate after the line already played, so nothing shows the first time.
  - Enabling the plugin without its dependency.
  - Building subtitle logic into C++ gameplay code. Keep the display swappable.
- **Claude can help:** Claude can write the C++ side and describe the Blueprint graph step by step. Placing Blueprint nodes is manual, unless Epic's MCP toolsets can create Blueprint graphs for you (they include Blueprint creation and editing; `VERIFY:` how far that goes).
- **Time:** 1 hour.

### Step 12. Scratch voice for timing (optional, recommended)

**Scratch voice** is a temporary recording used to time scenes and gameplay before the real actors record.

- **Goal:** realistic line lengths in the gray box and in first cutscene drafts, long before casting.
- **Do this:**
  1. Record rough reads yourself (any language you can speak at the right pace), or use a text-to-speech voice. Name the files exactly like the final VO (`VO_<LineID>.wav`), so final takes replace them one for one.
  2. Keep scratch files out of `audio/voice/ja/`. Use `audio/voice/scratch/` and point a copy of the import script at it. That way no scratch file can ship by accident.
  3. If you use a text-to-speech tool, check its license, and **never ship it**. AI-generated voice in the shipped game has to be disclosed on Steam (walkthrough 20) and isn't the plan.
- **Done when:** the cold open and in-game D01 lines have scratch audio with realistic lengths.
- **Common mistakes:** scratch files slowly becoming "final" because they're already in.
- **Claude can help:** Claude can generate a recording checklist per scene (IDs, text, direction) and batch-rename your recordings.
- **Time:** 1–2 hours for the slice.

### Step 13. Change control: keep text, audio, and game in sync

- **Goal:** after recording starts, no line changes without the audio being redone.
- **Do this:**
  1. **Status only moves forward:** Draft → Locked → Recorded → Implemented. If a Locked or Recorded line's text must change:
     - move it back to **Locked**;
     - write the reason in `Context`;
     - it goes on the next recording list;
     - the validator's "audio exists but status is Locked" warning keeps it visible until you re-record.
  2. **Before a recording session:** filter the sheet to `Status = Locked` for the actor's speaker IDs, and export that view as the actor's script: ID, Japanese, reading notes, direction, context. `dialogue_tool.py report` gives you the line and character counts for booking.
  3. **After a session:** rename the takes to `VO_<LineID>.wav`, validate, set them to Recorded, export, and import (steps 6, 9, 10).
  4. **Commit** the sheet export, the JSON, and the imported assets together, with a message like `Dialogue: D01 recorded (42 lines)`.
- **Done when:** this is how you work every time. The validator is clean after each recording batch.
- **Common mistakes:**
  - Quietly fixing a typo in TextJA after recording. The actor said the old line.
  - Editing subtitles without re-running the validator's reading-speed check.
- **Claude can help:** Claude can produce the actor scripts, check a recording batch against the sheet, and write the commit.
- **Time:** part of every recording session.

---

## Vertical slice checklist

- [ ] Story bible v2 and all District 1 and cold open scene scripts in `docs/story/`, committed as originals first
- [ ] `docs/story/scene-index.md` lists every slice scene (cold open `D00_S010`, D01 scenes, Vesper fight barks)
- [ ] `speakers.csv` complete for the slice's speakers, IsDead set for each
- [ ] Every slice line has a permanent ID in the scene scripts
- [ ] Google Sheet "Wraith Dialogue" with guard rails; slice scenes Locked and in the sheet
- [ ] Vesper's barks planned by phase (for example `B_VESPER_PHASE1_01`–`04`) and enemy combat barks for the four archetypes
- [ ] `dialogue_tool.py validate` at 0 errors; no reading-speed warnings on combat lines
- [ ] C++ row structs, `UWDialogueSettings`, and `UWDialogueSubsystem` built; tables set in Project Settings
- [ ] `DT_Dialogue` and `DT_Speakers` imported, keys checked, and reimport tested
- [ ] Subtitles and Closed Captions plugin enabled with `WBP_Subtitles` (or the fallback widget)
- [ ] A test key plays `D00_S010_0010` with subtitle and speaker name
- [ ] Scratch VO for the slice, kept in `audio/voice/scratch/`
- [ ] Recording-ready scripts exported for each slice actor (walkthrough 15 takes over from here)

## Going further

- **Automatic Google Sheets sync.** The Google Sheets API can download tabs without clicking, which is useful once the sheet has thousands of lines. The simple `.../export?format=csv` URL generally needs the sheet shared publicly, which you don't want for a story. Use the official API with your own credentials instead. Claude can write this; you set up the Google credentials.
- **Terminology glossary.** A `docs/story/glossary.md` of names and terms in Japanese and English, checked by the validator. It keeps translations consistent over 10 hours of story.
- **Bark system.** A small C++ system that picks a bark variant by event, with cooldowns and "don't repeat the last one" logic. It belongs in walkthrough 11 for enemies and 08 for Wraith.
- **Lip sync and facial animation** from the voice audio for unmasked characters (walkthrough 12, MetaHuman).
- **Closed captions.** Use the plugin's closed-caption type for important non-speech sounds, such as a lantern snuffing out behind the player. It's an accessibility win that walkthroughs 13 and 15 build on.

## References

**Epic Games** (documentation links; some pages were only reachable as search excerpts while writing)
- Data-driven gameplay elements (Data Tables): https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine
- `UDataTable` API: https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/UDataTable
- `DataTableFunctionLibrary` (Python): https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/DataTableFunctionLibrary
- `DataTableFactory` (Python): https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/DataTableFactory
- Text localization: https://dev.epicgames.com/documentation/en-us/unreal-engine/text-localization-in-unreal-engine
- String tables: https://dev.epicgames.com/documentation/en-us/unreal-engine/using-string-tables-for-text-in-unreal-engine
- Asset localization: https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-localization-in-unreal-engine
- Subtitles and Closed Captions plugin: https://dev.epicgames.com/documentation/unreal-engine/subtitles-and-closed-captions-plugin-in-unreal-engine
- Scripting the editor with Python: https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python

**Spreadsheets and formats**
- Google Sheets, publish and download: https://support.google.com/docs/answer/183965
- Excel, saving as CSV: https://support.microsoft.com/en-us/excel/save-a-workbook-to-text-format-txt-or-csv
- LibreOffice Calc, CSV files: https://help.libreoffice.org/latest/en-US/text/scalc/guide/csv_files.html
- Fountain syntax: https://fountain.io/syntax/

**Optional narrative tools**
- articy:draft X FREE: https://www.articy.com/en/articydraft/free/
- articy:draft X importer for Unreal: https://github.com/ArticySoftware/ArticyXImporterForUnreal
- Inkpot (Ink for Unreal): https://github.com/The-Chinese-Room/Inkpot
- Yarn Spinner for Unreal: https://github.com/YarnSpinnerTool/YarnSpinner-UnrealEngine

**Recommended learning channels**
- Unreal Engine on YouTube (official; search for localization and Data Tables): https://www.youtube.com/@UnrealEngine
- Epic Developer Community learning library: https://dev.epicgames.com/community/unreal-engine/learning
