from .utils import make_parser
from src.scales import all_cycles


def element_counts(l):
    out = {}
    for e in l:
        out[e] = out.get(e, 0) + 1
    return out


class Metastats:
    parser = make_parser(
        description="Find the distribution of scale stats",
        priorities=True,
        scale_size=True,
    )

    pass_edo_steps = True

    @staticmethod
    def run(priorities, scale_size, edo_steps):
        if len(priorities) != 1:
            print("Please supply exactly one stat function")
            return
        stat = priorities[0]

        cycles = all_cycles(scale_size=scale_size, edo_steps=edo_steps)

        stat_values = [stat(cycle) for cycle in cycles]
        minv = min(stat_values)
        maxv = max(stat_values)
        ecounts = element_counts(stat_values)

        for v in range(minv, maxv + 1):
            print(v, ecounts.get(v, 0))
