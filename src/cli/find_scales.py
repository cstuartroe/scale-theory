from typing import List
from src.scales import Cycle, all_cycles
from .utils import make_parser


def list_best_cycles_from(cycles: List[Cycle], priorities):
    cycle_stats = []
    for cycle in cycles:
        cycle_stats.append((cycle, tuple(p(cycle) for p in priorities)))

    print(len(cycles), "cycles found.")

    cycle_stats.sort(key=lambda x: x[1])
    for cycle, stats in cycle_stats[-100:]:
        named_parents = [p for p in cycle.parents() if p.name() is not None]
        print(cycle, *stats, cycle.name() or "", *named_parents)


def list_best_cycles(scale_size, edo_steps, priorities):
    list_best_cycles_from(all_cycles(scale_size, edo_steps), priorities)


class ListCycles:
    parser = make_parser(
        description="List the best cycles according to a set of criteria",
        length=True,
        priorities=True,
    )

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, length, priorities):
        list_best_cycles(length, edo_steps, priorities)
