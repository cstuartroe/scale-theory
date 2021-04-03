import os
import re
from typing import List
import jxon
from functools import cache
from src.ji import JustChord
from src.edo import EDO, EDOInterval
from src.midi_utils import emit_midi_sequence, sequence_from_jumps


class Scale:
    def __init__(self, jumps: [int]):
        self.jumps = tuple(jumps)

    @cache
    def edo_steps(self):
        return sum(self.jumps)

    def edo(self):
        return EDO(self.edo_steps())

    def size(self):
        return len(self.jumps)


SCALES_DIR = "static/scales"
NAMED_CYCLES = {}
for filename in os.listdir(SCALES_DIR):
    if filename == "scales.jxsd":
        continue

    assert (re.fullmatch(r"[0-9]+edo\.jxon", filename))
    with open(os.path.join(SCALES_DIR, filename), "r") as fh:
        cycles = jxon.load(fh)
        # uniqueness constraint - will hopefully enforce in jxon at some point
        assert len(set(map(lambda c: c["name"], cycles))) == len(cycles)
        NAMED_CYCLES[int(filename[:-8])] = cycles


class CycleMetaclass(type):
    __instances = {}

    def __call__(cls, jumps):
        modes = [
            Mode(jumps[i:] + jumps[:i])
            for i in range(len(jumps))
        ]

        canon_mode = min(modes, key=lambda mode: mode.weight())

        if canon_mode.jumps not in CycleMetaclass.__instances:
            obj = cls.__new__(cls, canon_mode)
            obj.__init__(canon_mode.jumps)
            obj.modes = modes
            obj.canon_mode = canon_mode
            CycleMetaclass.__instances[canon_mode.jumps] = obj

        return CycleMetaclass.__instances[canon_mode.jumps]


class Cycle(Scale, metaclass=CycleMetaclass):
    def __init__(self, jumps):
        super().__init__(jumps)

        # these ae immediately overwritten in CycleMetaclass.__call__, they're just written here for the benefit
        # of the type checker
        self.modes: List[Mode] = []
        self.canon_mode: Mode = None

    def __eq__(self, other):
        return self.jumps == other.jumps

    def __repr__(self):
        return f"Cycle({self.jumps})".replace(" ", "")

    @cache
    def name(self):
        for cycle in NAMED_CYCLES.get(self.edo().steps, []):
            if Cycle(cycle["jumps"]) == self:
                return cycle["name"]

        if self.size() <= 5:
            for just_chord in JustChord.NAMED_CHORDS:
                if Cycle.from_just_chord(just_chord, self.edo_steps()) == self:
                    return just_chord.name()

    @cache
    def children(self, length=None):
        out = set()
        for i in range(1, self.size()):
            child = Cycle((
                *self.jumps[:i - 1],
                self.jumps[i - 1] + self.jumps[i],
                *self.jumps[i + 1:]
            ))
            if length is None or length == child.size():
                out.add(child)
            if length != child.size():
                out = out | child.children(length)
        return out

    @cache
    def interval_counts(self):
        out = dict([(EDOInterval(steps, self.edo_steps()), 0) for steps in range(1, self.edo_steps())])
        for mode in self.modes:
            for interval in mode.intervals():
                out[interval] += 1

        return out

    @cache
    def interval_set(self):
        return set([ivl for ivl, count in self.interval_counts().items() if count > 0])

    def __hash__(self):
        return hash(self.jumps)

    @cache
    def parents(self):
        return []  # TODO

    @staticmethod
    def by_name(edo_steps: int, name: str):
        for cycle in NAMED_CYCLES.get(edo_steps, []):
            if cycle["name"] == name:
                return Cycle(cycle["jumps"])

    @staticmethod
    def named_cycles(edo_steps: int):
        return [Cycle(cycle["jumps"]) for cycle in NAMED_CYCLES.get(edo_steps, [])]

    def play_midi(self, note_duration, velocity, channel):
        emit_midi_sequence(
            sequence_from_jumps(self.jumps + self.jumps),
            note_duration=note_duration,
            velocity=velocity,
            channel=channel,
        )

    @classmethod
    def from_just_chord(cls, just_chord: JustChord, edo_steps: int):
        return EDOChord.from_just_chord(just_chord, edo_steps).cycle()


PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]


class Mode(Scale):
    @cache
    def weight(self):
        total = 1
        for i, jump in enumerate(self.jumps):
            total *= PRIMES[i] ** jump
        return total

    @cache
    def intervals(self):
        out = [self.jumps[0]]
        for jump in self.jumps[1:-1]:
            out.append(out[-1] + jump)
        return [EDOInterval(steps, self.edo_steps()) for steps in out]

    @cache
    def interval_set(self):
        return set(self.intervals())

    def cycle(self):
        return Cycle(self.jumps)

    def __eq__(self, other):
        return self.jumps == other.jumps

    def __repr__(self):
        return f"Mode({self.jumps})".replace(" ", "")

    def __hash__(self):
        return hash(self.jumps)

    def play_midi(self, note_duration, velocity, channel):
        emit_midi_sequence(
            sequence_from_jumps(self.jumps),
            note_duration=note_duration,
            velocity=velocity,
            channel=channel,
        )


class EDOChord(Mode):
    @classmethod
    def from_just_chord(cls, just_chord: JustChord, edo_steps: int):
        edo = EDO(edo_steps)
        edo_intervals = [edo.approximate(ivl) for ivl in just_chord.intervals()]
        jumps = []
        for i in range(len(edo_intervals)):
            jumps.append(edo_intervals[i].steps - (0 if i == 0 else edo_intervals[i-1].steps))
        jumps.append(edo_steps - edo_intervals[-1].steps)
        return cls(jumps)

    @classmethod
    def by_name(cls, name, edo_steps, inversion=0):
        return cls.from_just_chord(JustChord.by_name(name, inversion), edo_steps)

    @cache
    def just_chord(self):
        for just_chord in JustChord.NAMED_CHORDS:
            if just_chord.size() == self.size():
                for inv in just_chord.inversions():
                    if EDOChord.from_just_chord(inv, self.edo_steps()) == self:
                        return inv

    def name_with_inversion(self):
        return self.just_chord().name_with_inversion()

    def name_and_inversion(self):
        return self.just_chord().name_and_inversion()

    def name(self):
        return self.just_chord().name()

    def inversion(self):
        return self.just_chord().inversion()

    @cache
    def invert(self, inversion):
        return EDOChord(self.jumps[inversion:] + self.jumps[:inversion])

    @cache
    def inversions(self):
        return [self.invert(i) for i in range(self.size())]

    def invert_absolute(self, inversion):
        return self.invert(
            inversion - self.inversion()
        )

    def __repr__(self):
        return f"EDOChord({self.jumps})".replace(" ", "")

    def get_note_numbers(self, *, bass_midi_number=None, tonic_midi_number=None):
        if bass_midi_number is not None and tonic_midi_number is None:
            return (
                bass_midi_number,
                *[
                    bass_midi_number + ivl.steps
                    for ivl in self.intervals()
                ]
            )

        if bass_midi_number is None and tonic_midi_number is not None:
            tonic = self.intervals()[-self.inversion()] if self.inversion() != 0 else EDOInterval(0, self.edo_steps())
            return self.get_note_numbers(bass_midi_number=tonic_midi_number - tonic.steps)

        raise ValueError("Exactly one of bass_midi_number and tonic_midi_number must be None")

    # some, e.g. h7, may be excluded in smaller EDOs
    @classmethod
    def used_shape_names(cls, shape_names, edo_steps):
        out = []
        for shape_name in shape_names:
            ec = EDOChord.by_name(shape_name, edo_steps)
            if ec.name() not in out:
                out.append(ec.name())
        return out
