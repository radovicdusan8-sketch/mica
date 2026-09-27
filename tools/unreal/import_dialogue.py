"""Import Wraith's voice lines and dialogue tables into Unreal (walkthrough 02).

Run inside the Unreal Editor, never from a normal terminal:
  - Output Log: switch the command box from "Cmd" to "Python" and enter
        exec(open(r"C:/Dev/Wraith/tools/unreal/import_dialogue.py", encoding="utf-8").read())
  - or ask Claude to run this file through the Unreal MCP.

What it does:
  1. Imports new voice WAVs from audio/voice/ja/<folder>/VO_*.wav into
     /Game/Wraith/Audio/VO/<folder>/ (set REIMPORT_EXISTING to refresh all).
  2. Creates DT_Dialogue and DT_Speakers the first time, then refills them
     from docs/story/dialogue/build/*.json (made by dialogue_tool.py export).

Written against the UE 5.8 editor Python API. It can't be run outside
Unreal, so test it on a copy of the project first (walkthrough 02, step 9).
"""

import glob
import os

import unreal

REIMPORT_EXISTING = False  # True re-imports every WAV, not just new ones

PROJECT_DIR = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
REPO_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))
VOICE_DIR = os.path.join(REPO_ROOT, "audio", "voice", "ja")
BUILD_DIR = os.path.join(REPO_ROOT, "docs", "story", "dialogue", "build")
VO_PACKAGE = "/Game/Wraith/Audio/VO"
TABLE_PACKAGE = "/Game/Wraith/Data/Dialogue"

TABLES = [
    # (asset name, row struct, exported JSON)
    ("DT_Speakers", "/Script/WraithGame.WSpeakerRow", "DT_Speakers.json"),
    ("DT_Dialogue", "/Script/WraithGame.WDialogueLineRow", "DT_Dialogue.json"),
]


def import_voice():
    if not os.path.isdir(VOICE_DIR):
        unreal.log_warning(f"No voice folder at {VOICE_DIR}; skipping audio import.")
        return
    tasks = []
    for folder in sorted(os.listdir(VOICE_DIR)):
        for wav in sorted(glob.glob(os.path.join(VOICE_DIR, folder, "VO_*.wav"))):
            name = os.path.splitext(os.path.basename(wav))[0]
            destination = f"{VO_PACKAGE}/{folder}"
            if not REIMPORT_EXISTING and unreal.EditorAssetLibrary.does_asset_exist(f"{destination}/{name}"):
                continue
            task = unreal.AssetImportTask()
            task.set_editor_property("filename", wav)
            task.set_editor_property("destination_path", destination)
            task.set_editor_property("automated", True)
            task.set_editor_property("replace_existing", True)
            task.set_editor_property("save", True)
            tasks.append(task)
    if tasks:
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    unreal.log(f"Voice import: {len(tasks)} file(s) imported.")


def get_or_create_table(name, struct_path):
    row_struct = unreal.load_object(None, struct_path)
    if row_struct is None:
        raise RuntimeError(f"Row struct {struct_path} not found. Build the C++ code first.")
    asset_path = f"{TABLE_PACKAGE}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
        return unreal.EditorAssetLibrary.load_asset(asset_path), row_struct
    factory = unreal.DataTableFactory()
    factory.set_editor_property("struct", row_struct)
    table = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        name, TABLE_PACKAGE, unreal.DataTable, factory)
    return table, row_struct


def import_tables():
    for name, struct_path, json_name in TABLES:
        json_path = os.path.join(BUILD_DIR, json_name)
        if not os.path.exists(json_path):
            unreal.log_error(f"{json_path} is missing. Run: python tools/dialogue/dialogue_tool.py export")
            continue
        table, row_struct = get_or_create_table(name, struct_path)
        reported_ok = unreal.DataTableFunctionLibrary.fill_data_table_from_json_file(
            table, json_path, row_struct)
        rows = unreal.DataTableFunctionLibrary.get_data_table_row_names(table)
        # The return value isn't always reliable, so the row count is the real check.
        unreal.log(f"{name}: {len(rows)} rows after import (import reported {'ok' if reported_ok else 'failure'})")
        unreal.EditorAssetLibrary.save_loaded_asset(table)


import_voice()
import_tables()
