from src.scales import Cycle
from .utils import make_parser
from .find_scales import list_best_cycles_from


def list_best_subcycles(cycle: Cycle, priorities, length):
    list_best_cycles_from(cycle.children(length), priorities)


class ListSubcycles:
    parser = make_parser(
        description="Find the best subcycles of a given cycle according to a given priorities list",
        cycle=True,
        priorities=True,
        length=True,
    )

    @staticmethod
    def run(cycle, priorities, length):
        list_best_subcycles(cycle, priorities, length)
