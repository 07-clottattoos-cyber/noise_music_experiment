from __future__ import annotations

import platform
import shutil
import subprocess
from pathlib import Path

from music21 import stream


OUTPUT_SUBDIRS = ["scores", "audio", "midi", "musicxml", "stats", "charts", "report"]


def ensure_output_dirs(base_dir: Path) -> None:
    for subdir in OUTPUT_SUBDIRS:
        (base_dir / subdir).mkdir(parents=True, exist_ok=True)


def find_musescore() -> str | None:
    candidates = ["mscore", "musescore", "musescore4", "MuseScore4.exe", "MuseScore.exe"]
    for candidate in candidates:
        found = shutil.which(candidate)
        if found:
            return found
    if platform.system() == "Darwin":
        app_candidates = [
            "/Applications/MuseScore 4.app/Contents/MacOS/mscore",
            "/Applications/MuseScore 4.app/Contents/MacOS/MuseScore",
            "/Applications/MuseScore.app/Contents/MacOS/mscore",
        ]
        for candidate in app_candidates:
            if Path(candidate).exists():
                return candidate
    return None


def export_musicxml_and_midi(score: stream.Score, name: str, output_dir: Path) -> dict[str, Path]:
    musicxml_path = output_dir / "musicxml" / f"{name}.musicxml"
    midi_path = output_dir / "midi" / f"{name}.mid"
    score.write("musicxml", fp=str(musicxml_path))
    score.write("midi", fp=str(midi_path))
    return {"musicxml": musicxml_path, "midi": midi_path}


def export_with_musescore(musicxml_path: Path, name: str, output_dir: Path, musescore: str | None = None) -> dict[str, Path]:
    command = musescore or find_musescore()
    if not command:
        return {}

    exported: dict[str, Path] = {}
    targets = {
        "pdf": output_dir / "scores" / f"{name}.pdf",
        "wav": output_dir / "audio" / f"{name}.wav",
    }
    for kind, target in targets.items():
        try:
            subprocess.run(
                [command, "-o", str(target), str(musicxml_path)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=90,
            )
            exported[kind] = target
        except (subprocess.SubprocessError, OSError) as exc:
            print(f"MuseScore 导出 {target.name} 失败：{exc}")
    return exported


def export_score(score: stream.Score, name: str, output_dir: Path, musescore: str | None = None) -> dict[str, Path]:
    paths = export_musicxml_and_midi(score, name, output_dir)
    paths.update(export_with_musescore(paths["musicxml"], name, output_dir, musescore))
    return paths
