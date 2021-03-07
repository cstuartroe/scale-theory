import math
from tabulate import tabulate

CHORD_MAX = 100


def chords_helper(tones, start=2):
    if tones == 0:
        return [()]
    else:
        out = []
        for tonic in range(start, CHORD_MAX + 1):
            for tail in chords_helper(tones - 1, tonic + 1):
                out.append((tonic, *tail))
        return out


def chords(tones=3):
    return [chord for chord in chords_helper(tones) if math.gcd(*chord) == 1 and (chord[-1] / chord[0] < 2)]


def chords_with_dissonance(tones=3, dissonance_function=euler_dissonance):
    out = []

    for chord in chords(tones):
        out.append((chord, dissonance_function(*chord)))

    out.sort(key=lambda x: x[1])
    return out


def closest_approximation(r, edo_steps):
    r_cents = cents(r)
    step_size = 1200 / edo_steps
    steps = round(r_cents / step_size)
    return round((steps * step_size) - r_cents, 1)


MAJOR_EDOS = [12, 17, 19, 22, 24, 31, 41]


if __name__ == "__main__":
    table = [
        (
            "Ratio",
            "Dissonance",
            "Name",
            "Cents",
            *(
                f"{s}EDO Approximation"
                for s in MAJOR_EDOS
            )
        )
    ]

    for chord, dissonance in chords_with_dissonance(2, dissonance_function=euler_dissonance):
        table.append((
            ':'.join(map(str, chord)),
            dissonance,
            NAMED_CHORDS.get(chord, ''),
            cents(chord[1]/chord[0]),
            *(
                closest_approximation(chord[1]/chord[0], edo_steps)
                for edo_steps in MAJOR_EDOS
            ),
        ))

    print(tabulate(table))
