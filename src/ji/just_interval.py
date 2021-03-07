import math
import jxon
from .consonance import euler_dissonance, vogel_dissonance, gill_purves_dissonance


with open("static/ji/intervals.jxon", "r") as fh:
    NAMED_INTERVALS = jxon.load(fh)


class Interval:
    def octaves(self) -> float:
        raise NotImplementedError

    def cents(self):
        return round(self.octaves() * 1200, 1)


class JI(Interval):
    def __init__(self, num, denom):
        assert num > denom
        self.num = num
        self.denom = denom

    def octaves(self):
        return math.log2(self.num / self.denom)

    def __repr__(self):
        return f"JI({self.num}, {self.denom})"

    def name(self):
        for ivl in NAMED_INTERVALS:
            if (ivl["num"], ivl["denom"]) == (self.num, self.denom):
                return ivl["name"]

    def euler_dissonance(self):
        return euler_dissonance(self.denom, self.num)

    def vogel_dissonance(self):
        return vogel_dissonance(self.denom, self.num)

    def gill_purves_dissonance(self):
        return gill_purves_dissonance(self.denom, self.num)

    def compromise_dissonance(self):
        return self.euler_dissonance() + self.gill_purves_dissonance() / 10

    @classmethod
    def by_name(cls, name: str):
        for ivl in NAMED_INTERVALS:
            if ivl["name"] == name:
                return cls(ivl["num"], ivl["denom"])


JI.NAMED_INTERVALS = [JI(ivl["num"], ivl["denom"]) for ivl in NAMED_INTERVALS]
