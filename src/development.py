from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from music21 import clef, duration, instrument, key, meter, metadata, note, stream, tempo


@dataclass(frozen=True)
class MotifMaterial:
    pitches: list[int]
    durations: list[float]


def _clip_c4_c6(midi_pitch: int) -> int:
    return max(60, min(84, midi_pitch))


def _invert(pitches: Iterable[int], axis: int = 72) -> list[int]:
    return [_clip_c4_c6(axis - (p - axis)) for p in pitches]


def _fit_measure(pitches: list[int], durations: list[float]) -> list[tuple[int, float]]:
    result: list[tuple[int, float]] = []
    total = 0.0
    i = 0
    while total < 4.0:
        p = pitches[i % len(pitches)]
        d = durations[i % len(durations)]
        if total + d > 4.0:
            d = 4.0 - total
        result.append((_clip_c4_c6(p), d))
        total += d
        i += 1
    return result


def _duration(q_len: float) -> duration.Duration:
    d = duration.Duration(q_len)
    if q_len == 2.0:
        d.type = "half"
    elif q_len == 1.0:
        d.type = "quarter"
    elif q_len == 0.5:
        d.type = "eighth"
    elif q_len == 0.25:
        d.type = "16th"
    return d


def _new_score(title: str, bpm: int) -> tuple[stream.Score, stream.Part]:
    score = stream.Score(id=title.replace(" ", "_").lower())
    score.insert(0, metadata.Metadata(title=title, composer="Python noise music experiment"))
    part = stream.Part(id="melody")
    part.insert(0, instrument.Piano())
    part.insert(0, tempo.MetronomeMark(number=bpm))
    part.insert(0, key.Key("C"))
    part.insert(0, meter.TimeSignature("4/4"))
    part.insert(0, clef.TrebleClef())
    score.append(part)
    return score, part


def _append_measure(part: stream.Part, number: int, material: list[tuple[int, float]]) -> None:
    m = stream.Measure(number=number)
    for midi_pitch, q_len in material:
        n = note.Note(_clip_c4_c6(midi_pitch))
        n.duration = _duration(q_len)
        m.append(n)
    part.append(m)


def build_pink_development(material: MotifMaterial, measures: int = 24, bpm: int = 116) -> stream.Score:
    score, part = _new_score("Pink Theme Development", bpm)
    base_pitches = material.pitches
    base_durations = material.durations
    for number in range(1, measures + 1):
        if number <= 8:
            shift = 0 if number % 2 else 5
            pitches = [p + shift for p in base_pitches]
            durations = base_durations
        elif number <= 16:
            shift = 7 if number % 3 else -5
            pitches = _invert([p + shift for p in base_pitches], axis=72)
            durations = [max(0.25, d / 2) for d in base_durations]
        else:
            shift = [0, 2, 4, 7, 5, 2, 0, 0][number - 17]
            pitches = [p + shift for p in base_pitches]
            durations = [min(2.0, d * 1.5) if number >= 21 else d for d in base_durations]
        if number == measures:
            pitches = [72, 76, 79, 84]
            durations = [1.0, 1.0, 1.0, 1.0]
        _append_measure(part, number, _fit_measure(pitches, durations))
    return score


def build_brown_development(material: MotifMaterial, measures: int = 28, bpm: int = 92) -> stream.Score:
    score, part = _new_score("Brown Theme Development", bpm)
    base_pitches = material.pitches
    base_durations = material.durations
    for number in range(1, measures + 1):
        if number <= 8:
            shift = 0
            durations = base_durations
        elif number <= 16:
            shift = (number - 9) % 4
            durations = base_durations
        elif number <= 24:
            shift = ((number - 17) // 2) * 3 - 3
            durations = [max(0.5, d) for d in base_durations]
        else:
            shift = 0
            durations = [2.0, 1.0, 1.0]
        pitches = [p + shift for p in base_pitches]
        if number > 24:
            pitches = [67, 65, 62, 60]
        if number == measures:
            pitches = [64, 62, 60]
            durations = [1.0, 1.0, 2.0]
        _append_measure(part, number, _fit_measure(pitches, durations))
    return score
