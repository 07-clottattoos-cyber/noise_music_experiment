from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

import numpy as np
from music21 import clef, duration, instrument, key, meter, metadata, note, stream, tempo

from .noise_generators import generate_brown_sequence, generate_pink_sequence


DURATION_TYPES = {"half": 2.0, "quarter": 1.0, "eighth": 0.5, "16th": 0.25}
C_MAJOR_MIDI = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]


@dataclass(frozen=True)
class MelodyData:
    score: stream.Score
    note_specs: list[tuple[int, float]]


def _ql(value: float) -> Fraction:
    return Fraction(str(value))


def _duration_type(quarter_length: float) -> str:
    for name, length in DURATION_TYPES.items():
        if abs(length - quarter_length) < 1e-9:
            return name
    return "quarter"


def _make_duration(name: str) -> duration.Duration:
    d = duration.Duration(DURATION_TYPES[name])
    d.type = name
    return d


def _measure_rhythm(rng: np.random.Generator, style: str) -> list[float]:
    names = list(DURATION_TYPES.keys())
    if style == "brown":
        probs = [0.18, 0.48, 0.26, 0.08]
    else:
        probs = [0.12, 0.34, 0.32, 0.22]
    remaining = _ql(4.0)
    values: list[float] = []
    while remaining > 0:
        allowed = [n for n in names if _ql(DURATION_TYPES[n]) <= remaining]
        weights = np.array([probs[names.index(n)] for n in allowed], dtype=float)
        weights /= weights.sum()
        chosen = str(rng.choice(allowed, p=weights))
        values.append(DURATION_TYPES[chosen])
        remaining -= _ql(DURATION_TYPES[chosen])
    return values


def _generate_rhythm(measures: int, seed: int, style: str) -> list[list[float]]:
    rng = np.random.default_rng(seed)
    rhythms = [_measure_rhythm(rng, style) for _ in range(measures)]
    flat = [value for measure_values in rhythms for value in measure_values]
    missing = [value for value in DURATION_TYPES.values() if value not in flat]
    for idx, value in enumerate(missing):
        rhythms[idx % measures] = [value] + [1.0] * int(4 - value)
    return rhythms


def _quantize_to_c_major(values: Iterable[float]) -> list[int]:
    values_list = list(values)
    indices = np.rint(np.array(values_list) * (len(C_MAJOR_MIDI) - 1)).astype(int)
    return [C_MAJOR_MIDI[int(np.clip(i, 0, len(C_MAJOR_MIDI) - 1))] for i in indices]


def _force_two_octave_range(pitches: list[int]) -> list[int]:
    if pitches:
        pitches[0] = 60
    if len(pitches) > 1:
        pitches[len(pitches) // 2] = 84
    return pitches


def _build_score(title: str, rhythms: list[list[float]], pitches: list[int], bpm: int) -> MelodyData:
    score = stream.Score(id=title.replace(" ", "_").lower())
    score.insert(0, metadata.Metadata(title=title, composer="Python noise music experiment"))
    part = stream.Part(id="melody")
    part.insert(0, instrument.Piano())
    part.insert(0, tempo.MetronomeMark(number=bpm))
    part.insert(0, key.Key("C"))
    part.insert(0, meter.TimeSignature("4/4"))
    part.insert(0, clef.TrebleClef())

    specs: list[tuple[int, float]] = []
    pitch_index = 0
    for measure_number, measure_values in enumerate(rhythms, start=1):
        m = stream.Measure(number=measure_number)
        for q_len in measure_values:
            midi_pitch = pitches[pitch_index]
            n = note.Note(midi_pitch)
            n.duration = _make_duration(_duration_type(q_len))
            m.append(n)
            specs.append((midi_pitch, q_len))
            pitch_index += 1
        part.append(m)
    score.append(part)
    return MelodyData(score=score, note_specs=specs)


def build_pink_melody(config: dict) -> MelodyData:
    measures = int(config["measures"]["random_melody"])
    seed = int(config["seed"])
    rhythms = _generate_rhythm(measures, seed + 11, "pink")
    note_count = sum(len(m) for m in rhythms)
    seq = generate_pink_sequence(note_count, seed + 101)
    shaped = 0.5 + (seq - 0.5) * 0.92
    pitches = _force_two_octave_range(_quantize_to_c_major(np.clip(shaped, 0, 1)))
    return _build_score("Pink Noise Random Melody", rhythms, pitches, int(config["tempo"]["random_melody"]))


def build_brown_melody(config: dict) -> MelodyData:
    measures = int(config["measures"]["random_melody"])
    seed = int(config["seed"])
    rhythms = _generate_rhythm(measures, seed + 22, "brown")
    note_count = sum(len(m) for m in rhythms)
    seq = generate_brown_sequence(note_count, seed + 202)
    pitches = _force_two_octave_range(_quantize_to_c_major(seq))
    return _build_score("Brown Noise Random Melody", rhythms, pitches, int(config["tempo"]["random_melody"]))
