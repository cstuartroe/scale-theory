import jxon
from .consonance import euler_dissonance, vogel_dissonance

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
        self.ratio = tuple(ratio)

    def __repr__(self):
        return f"JustChord({self.ratio})"

    def invert(self, inversion):
        ratio = self.ratio[inversion % len(self.ratio):] + tuple(map(lambda n: n * 2, self.ratio[:inversion % len(self.ratio)]))
        if all(n % 2 == 0 for n in ratio):
            return JustChord(n // 2 for n in ratio)
        else:
            return JustChord(ratio)

    def name_and_inversion(self):
        for chord_obj in NAMED_CHORDS:
            chord = JustChord(chord_obj["ratio"])

            for inv in range(self.size()):
                if self.invert(inv) == chord:
                    return chord_obj["name"], inv

    def name(self):
        return self.name_and_inversion()[0]

    def size(self):
        return len(self.ratio)

    def __eq__(self, other):
        return self.ratio == other.ratio

    def __hash__(self):
        return hash(self.ratio)

    def euler_dissonance(self):
        return euler_dissonance(*self.ratio)

    def vogel_dissonance(self):
        return vogel_dissonance(*self.ratio)

    @classmethod
    def by_name(cls, name: str, inversion=0):
        for chord in NAMED_CHORDS:
            if chord["name"] == name:
                return cls(chord["ratio"]).invert(inversion)


JustChord.NAMED_CHORDS = [JustChord(chord["ratio"]) for chord in NAMED_CHORDS]
