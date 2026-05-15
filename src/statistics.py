from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from music21 import note, stream


def extract_notes(score: stream.Score) -> list[note.Note]:
    return [n for n in score.recurse().notes if isinstance(n, note.Note)]


def _measure_count(score: stream.Score) -> int:
    return len(list(score.parts[0].getElementsByClass(stream.Measure)))


def _zone(midi_pitch: int) -> str:
    if 60 <= midi_pitch <= 67:
        return "low"
    if 69 <= midi_pitch <= 79:
        return "middle"
    if 81 <= midi_pitch <= 84:
        return "high"
    return "outside"


def analyze_score(score: stream.Score, label: str) -> dict[str, Any]:
    notes = extract_notes(score)
    midi_values = [n.pitch.midi for n in notes]
    intervals = [b - a for a, b in zip(midi_values, midi_values[1:])]
    duration_types = [n.duration.type for n in notes]
    quarter_lengths = [float(n.duration.quarterLength) for n in notes]
    span = max(midi_values) - min(midi_values) if midi_values else 0
    total_measures = _measure_count(score)
    required_durations = {"half", "quarter", "eighth", "16th"}

    return {
        "label": label,
        "pitch_counts": Counter(n.pitch.nameWithOctave for n in notes),
        "midi_counts": Counter(midi_values),
        "duration_type_counts": Counter(duration_types),
        "quarter_length_counts": Counter(quarter_lengths),
        "interval_counts": Counter(intervals),
        "zone_counts": Counter(_zone(m) for m in midi_values),
        "lowest_pitch": min(notes, key=lambda n: n.pitch.midi).pitch.nameWithOctave,
        "highest_pitch": max(notes, key=lambda n: n.pitch.midi).pitch.nameWithOctave,
        "lowest_midi": min(midi_values),
        "highest_midi": max(midi_values),
        "pitch_range_semitones": span,
        "total_notes": len(notes),
        "total_measures": total_measures,
        "constraints_met": total_measures >= 16 and span >= 24 and required_durations.issubset(set(duration_types)),
    }


def _counter_to_df(counter: Counter, key_name: str) -> pd.DataFrame:
    return pd.DataFrame(sorted(counter.items()), columns=[key_name, "count"])


def _save_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str, path: Path) -> None:
    plt.figure(figsize=(9, 4.8))
    plt.bar(df[x_col].astype(str), df[y_col])
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def write_statistics(analyses: dict[str, dict[str, Any]], output_dir: Path) -> dict[str, Path]:
    stats_dir = output_dir / "stats"
    charts_dir = output_dir / "charts"
    written: dict[str, Path] = {}
    summary_rows: list[dict[str, Any]] = []

    with pd.ExcelWriter(stats_dir / "summary_stats.xlsx") as writer:
        for label, analysis in analyses.items():
            pitch_df = _counter_to_df(analysis["pitch_counts"], "pitch")
            duration_df = _counter_to_df(analysis["duration_type_counts"], "duration_type")
            interval_df = _counter_to_df(analysis["interval_counts"], "interval_semitones")
            zone_df = _counter_to_df(analysis["zone_counts"], "zone")

            for suffix, df in [
                ("pitch_stats", pitch_df),
                ("duration_stats", duration_df),
                ("interval_stats", interval_df),
                ("zone_stats", zone_df),
            ]:
                path = stats_dir / f"{label}_{suffix}.csv"
                df.to_csv(path, index=False)
                written[f"{label}_{suffix}"] = path
                df.to_excel(writer, sheet_name=f"{label}_{suffix}"[:31], index=False)

            summary_rows.append(
                {
                    "label": label,
                    "lowest_pitch": analysis["lowest_pitch"],
                    "highest_pitch": analysis["highest_pitch"],
                    "pitch_range_semitones": analysis["pitch_range_semitones"],
                    "total_notes": analysis["total_notes"],
                    "total_measures": analysis["total_measures"],
                    "constraints_met": analysis["constraints_met"],
                }
            )

            _save_bar(pitch_df, "pitch", "count", f"{label} pitch distribution", charts_dir / f"{label}_pitch_distribution.png")
            _save_bar(duration_df, "duration_type", "count", f"{label} duration distribution", charts_dir / f"{label}_duration_distribution.png")
            _save_bar(interval_df, "interval_semitones", "count", f"{label} interval distribution", charts_dir / f"{label}_interval_distribution.png")

        summary_df = pd.DataFrame(summary_rows)
        summary_df.to_excel(writer, sheet_name="summary", index=False)
        summary_csv = stats_dir / "summary_stats.csv"
        summary_df.to_csv(summary_csv, index=False)
        written["summary_csv"] = summary_csv

    written["summary_xlsx"] = stats_dir / "summary_stats.xlsx"
    return written
