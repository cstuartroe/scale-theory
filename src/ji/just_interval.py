import math
import jxon


with open("static/ji/intervals.jxon", "r") as fh:
    NAMED_INTERVALS = jxon.load(fh)


class Interval:
    def octaves(self) -> float:
        raise NotImplementedError

    def cents(self):
        return round(self.octaves() * 1200, 1)

    def __gt__(self, other):
        return self.cents() > other.cents()
        
    def __lt__(self, other):
        return self.cents() < other.cents()


class JI(Interval):
    def __init__(self, denom, num):
        assert num >= denom
        self.num = num
        self.denom = denom
        self.ratio = (denom, num)

    def octaves(self):
        return math.log2(self.num / self.denom)

    def __repr__(self):
        return f"JI({self.num}, {self.denom})"

    def name(self):
        for ivl in NAMED_INTERVALS:
            if (ivl["num"], ivl["denom"]) == (self.num, self.denom):
                return ivl["name"]

    @classmethod
    def by_name(cls, name: str):
        for ivl in NAMED_INTERVALS:
            if ivl["name"] == name:
                return cls(num=ivl["num"], denom=ivl["denom"])


JI.NAMED_INTERVALS = [JI(num=ivl["num"], denom=ivl["denom"]) for ivl in NAMED_INTERVALS]
