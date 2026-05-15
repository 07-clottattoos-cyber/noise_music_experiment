from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from music21 import note, stream

from src.development import MotifMaterial, build_brown_development, build_pink_development
from src.main import load_config
from src.melody_builder import build_brown_melody, build_pink_melody


ROOT = Path(__file__).resolve().parents[1]


def _notes(score: stream.Score) -> list[note.Note]:
    return [n for n in score.recurse().notes if isinstance(n, note.Note)]


def _measure_count(score: stream.Score) -> int:
    return len(list(score.parts[0].getElementsByClass(stream.Measure)))


def _assert_common_constraints(score: stream.Score) -> None:
    assert _measure_count(score) >= 16
    for measure in score.parts[0].getElementsByClass(stream.Measure):
        assert float(measure.duration.quarterLength) == 4.0
    duration_types = {n.duration.type for n in _notes(score)}
    assert {"half", "quarter", "eighth", "16th"}.issubset(duration_types)
    midi_values = [n.pitch.midi for n in _notes(score)]
    assert max(midi_values) - min(midi_values) >= 24


def test_random_melody_constraints() -> None:
    config = load_config()
    _assert_common_constraints(build_pink_melody(config).score)
    _assert_common_constraints(build_brown_melody(config).score)


def test_development_lengths() -> None:
    material = MotifMaterial([60, 62, 64, 67], [1.0, 1.0, 1.0, 1.0])
    assert _measure_count(build_pink_development(material)) == 24
    assert _measure_count(build_brown_development(material)) == 28


def test_main_exports_exist() -> None:
    subprocess.run([sys.executable, "-m", "src.main"], cwd=ROOT, check=True)
    required = [
        "output/musicxml/pink_music.musicxml",
        "output/musicxml/brown_music.musicxml",
        "output/musicxml/pink_motif.musicxml",
        "output/musicxml/brown_motif.musicxml",
        "output/musicxml/pink_theme_development.musicxml",
        "output/musicxml/brown_theme_development.musicxml",
        "output/midi/pink_music.mid",
        "output/midi/brown_music.mid",
        "output/stats/pink_pitch_stats.csv",
        "output/stats/brown_pitch_stats.csv",
        "output/stats/summary_stats.xlsx",
        "output/report/experiment_report.md",
    ]
    for relative_path in required:
        path = ROOT / relative_path
        assert path.exists()
        assert path.stat().st_size > 0
