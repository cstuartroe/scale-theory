import os
import re
import jxon
from src.edo import EDO, EDOInterval


class Scale:
    def __init__(self, jumps: [int]):
        self.jumps = tuple(jumps)

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
        NAMED_CYCLES[int(filename[:-8])] = jxon.load(fh)


class Cycle(Scale):
    def modes(self):
        return [
            Mode(self.jumps[i:] + self.jumps[:i])
            for i in range(len(self.jumps))
        ]

    def canon_mode(self):
        return min(self.modes(), key=lambda mode: mode.weight())

    def __eq__(self, other):
        return self.canon_mode() == other.canon_mode()

    def __repr__(self):
        return f"Cycle({self.canon_mode().jumps})"

    def name(self):
        for cycle in NAMED_CYCLES[self.edo()]:
            if Cycle(cycle["jumps"]) == self:
                return cycle["name"]

    def children(self):
        out = set()
        for i in range(1, self.size()):
            child = Cycle((
                *self.jumps[:i - 1],
                self.jumps[i - 1] + self.jumps[i],
                *self.jumps[i + 1:]
            ))
            out.add(child)
            out = out | child.children()
        return out

    def __hash__(self):
        return hash(self.canon_mode())

    @staticmethod
    def by_name(edo_steps: int, name: str):
        for cycle in NAMED_CYCLES.get(edo_steps, []):
            if cycle["name"] == name:
                return Cycle(cycle["jumps"])

    @staticmethod
    def named_cycles(edo_steps: int):
        return [Cycle(cycle["jumps"]) for cycle in NAMED_CYCLES.get(edo_steps, [])]


class Mode(Scale):
    def weight(self):
        total = 0
        for j in range(len(self.jumps)):
            total += j * self.jumps[j]
        return total

    def interval(self, degree):
        return EDOInterval(sum(self.jumps[:degree]), self.edo_steps())

    def intervals(self):
        return [self.interval(degree) for degree in range(len(self.jumps))]

    def cycle(self):
        return Cycle(self.jumps)

    def __eq__(self, other):
        return self.jumps == other.jumps

    def __repr__(self):
        return f"Mode({self.jumps})"

    def __hash__(self):
        return hash(self.jumps)

