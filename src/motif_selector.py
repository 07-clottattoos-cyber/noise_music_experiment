from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from music21 import clef, instrument, key, meter, metadata, note, stream, tempo


@dataclass(frozen=True)
class MotifSelection:
    score: stream.Score
    start_measure: int
    end_measure: int
    pitches: list[int]
    durations: list[float]
    reason: str


def _notes_in_measures(score: stream.Score, start: int, length: int) -> list[note.Note]:
    selected: list[note.Note] = []
    for measure_number in range(start, start + length):
        m = score.parts[0].measure(measure_number)
        if m is not None:
            selected.extend([n for n in m.notes if isinstance(n, note.Note)])
    return selected


def _make_motif_score(notes: list[note.Note], title: str) -> stream.Score:
    score = stream.Score(id=title.replace(" ", "_").lower())
    score.insert(0, metadata.Metadata(title=title, composer="Python noise music experiment"))
    part = stream.Part(id="motif")
    part.insert(0, instrument.Piano())
    part.insert(0, tempo.MetronomeMark(number=100))
    part.insert(0, key.Key("C"))
    part.insert(0, meter.TimeSignature("4/4"))
    part.insert(0, clef.TrebleClef())
    m = stream.Measure(number=1)
    current = 0.0
    number = 1
    for original in notes:
        if current + float(original.duration.quarterLength) > 4.0:
            part.append(m)
            number += 1
            m = stream.Measure(number=number)
            current = 0.0
        copied = original.__deepcopy__()
        m.append(copied)
        current += float(copied.duration.quarterLength)
    if len(m.notes) > 0:
        part.append(m)
    score.append(part)
    return score


def _trend_score(intervals: list[int]) -> float:
    if not intervals:
        return 0
    direction = sum(1 if i > 0 else -1 if i < 0 else 0 for i in intervals)
    return abs(direction) / len(intervals)


def select_motif(score: stream.Score, style: Literal["pink", "brown"]) -> MotifSelection:
    measures = len(list(score.parts[0].getElementsByClass(stream.Measure)))
    best: tuple[float, int, int, list[note.Note], str] | None = None
    for start in range(1, measures + 1):
        for length in (1, 2):
            if start + length - 1 > measures:
                continue
            notes = _notes_in_measures(score, start, length)
            if len(notes) < 3:
                continue
            pitches = [n.pitch.midi for n in notes]
            durations = [float(n.duration.quarterLength) for n in notes]
            intervals = [b - a for a, b in zip(pitches, pitches[1:])]
            rhythmic_variety = len(set(durations))
            if style == "pink":
                leaps = sum(1 for i in intervals if abs(i) >= 3)
                interval_variety = len(set(abs(i) for i in intervals))
                score_value = leaps * 3 + interval_variety * 1.5 + rhythmic_variety
                reason = f"含 {leaps} 个三度以上跳进，节奏种类 {rhythmic_variety}，音程变化较丰富。"
            else:
                step_like = sum(1 for i in intervals if abs(i) <= 2)
                smooth_ratio = step_like / max(1, len(intervals))
                score_value = smooth_ratio * 5 + _trend_score(intervals) * 2 - max(0, rhythmic_variety - 2) * 0.4
                reason = f"级进/同音比例 {smooth_ratio:.2f}，方向趋势评分 {_trend_score(intervals):.2f}，节奏较稳定。"
            if best is None or score_value > best[0]:
                best = (score_value, start, length, notes, reason)
    if best is None:
        raise ValueError(f"Cannot select {style} motif")
    _, start, length, notes, reason = best
    motif_score = _make_motif_score(notes, f"{style.title()} Selected Motif")
    pitches = [n.pitch.midi for n in notes]
    durations = [float(n.duration.quarterLength) for n in notes]
    return MotifSelection(motif_score, start, start + length - 1, pitches, durations, reason)
