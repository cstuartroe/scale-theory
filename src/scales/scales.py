import os
import re
from typing import List
import jxon
from functools import cache
from src.edo import EDO, EDOInterval


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
        return f"Cycle({self.jumps})"

    @cache
    def name(self):
        for cycle in NAMED_CYCLES.get(self.edo().steps, []):
            if Cycle(cycle["jumps"]) == self:
                return cycle["name"]

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


class Mode(Scale):
    @cache
    def weight(self):
        total = 0
        for j in range(len(self.jumps)):
            total += j * self.jumps[j]
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
        return f"Mode({self.jumps})"

    def __hash__(self):
        return hash(self.jumps)

