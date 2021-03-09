import math
import jxon
from .just_interval import JI

ORDINALS = [
    "0th",
    "1st",
    "2nd",
    "3rd",
]

with open("static/ji/chords.jxon", "r") as fh:
    NAMED_CHORDS = jxon.load(fh)


class JustChord:
    def __init__(self, ratio: [int]):
        assert all(ratio[i] < ratio[i+1] for i in range(len(ratio) - 1))
        self.ratio = tuple([n//math.gcd(*ratio) for n in ratio])

    def __repr__(self):
        return f"JustChord({self.ratio})"

    def invert(self, inversion):
        ratio = self.ratio[inversion % len(self.ratio):] + tuple(map(lambda n: n * 2, self.ratio[:inversion % len(self.ratio)]))
        if all(n % 2 == 0 for n in ratio):
            return JustChord([n // 2 for n in ratio])
        else:
            return JustChord(ratio)

    def name_and_inversion(self):
        for chord_obj in NAMED_CHORDS:
            chord = JustChord(chord_obj["ratio"])

            for inv in range(self.size()):
                if self.invert(inv) == chord:
                    return chord_obj["name"], inv

        return None, None

    def name(self):
        return self.name_and_inversion()[0]

    def name_with_inversion(self):
        name, inv = self.name_and_inversion()
        if name is None:
            return None
        elif inv == 0:
            return name
        else:
            return f"{name} ({ORDINALS[inv]} inversion)"

    def size(self):
        return len(self.ratio)

    def __eq__(self, other):
        return self.ratio == other.ratio

    def __hash__(self):
        return hash(self.ratio)

    def intervals(self):
        return [JI(self.ratio[0], overtone) for overtone in self.ratio[1:]]

    def cents(self):
        return [ivl.cents() for ivl in self.intervals()]

    def approximation_in(self, edo):
        return [edo.approximate(ivl) for ivl in self.intervals()]

    @classmethod
    def by_name(cls, name: str, inversion=0):
        for chord in NAMED_CHORDS:
            if chord["name"] == name:
                return cls(chord["ratio"]).invert(inversion)


JustChord.NAMED_CHORDS = [JustChord(chord["ratio"]) for chord in NAMED_CHORDS]


def chords_helper(tones, start, max_ratio):
    if tones == 0:
        return [()]
    else:
        out = []
        for tonic in range(start, max_ratio + 1):
            for tail in chords_helper(tones - 1, tonic + 1, max_ratio):
                out.append((tonic, *tail))
        return out


def just_chords(tones, max_ratio):
    return set([JustChord(chord) for chord in chords_helper(tones, 2, max_ratio) if (chord[-1] / chord[0] < 2)])
