from __future__ import annotations

import numpy as np


def _normalize(values: np.ndarray) -> np.ndarray:
    span = float(values.max() - values.min())
    if span == 0:
        return np.zeros_like(values)
    return (values - values.min()) / span


def generate_pink_sequence(length: int, seed: int, octaves: int = 8) -> np.ndarray:
    """Generate an approximate 1/f sequence with the Voss-McCartney method."""
    rng = np.random.default_rng(seed)
    rows = rng.normal(size=(octaves, length))
    values = np.zeros(length)
    current = rng.normal(size=octaves)
    for i in range(length):
        if i == 0:
            current = rows[:, i]
        else:
            changed = 0
            n = i
            while n % 2 == 0 and changed < octaves:
                changed += 1
                n //= 2
            if changed:
                current[:changed] = rows[:changed, i]
        values[i] = current.sum()
    return _normalize(values)


def generate_brown_sequence(length: int, seed: int) -> np.ndarray:
    """Generate a bounded random-walk sequence normalized to 0..1."""
    rng = np.random.default_rng(seed)
    steps = rng.choice(
        [-4, -3, -2, -1, 0, 1, 2, 3, 4],
        size=length,
        p=[0.015, 0.035, 0.14, 0.22, 0.18, 0.22, 0.14, 0.035, 0.015],
    )
    values = np.zeros(length)
    pos = 0.5
    direction = 1.0
    for i, step in enumerate(steps):
        pos += direction * float(step) / 24.0
        if pos < 0:
            pos = abs(pos)
            direction *= -1
        elif pos > 1:
            pos = 2 - pos
            direction *= -1
        values[i] = pos
    return _normalize(values)
