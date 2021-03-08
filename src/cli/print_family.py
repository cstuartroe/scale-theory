from src.scales import Cycle
from .scale_info import scale_info
from .utils import make_parser


def print_family(parent: Cycle, lengths):
    subscales = parent.children()
    named_subscales = [c for c in subscales if c.name() is not None and c.size() in lengths]
    named_subscales.sort(key=lambda cycle: cycle.size())

    for scale in named_subscales:
        scale_info(scale)

    scale_info(parent)


class PrintFamily:
    parser = make_parser(
        description="Print information about a cycle and its children",
        cycle=True,
    )

    @staticmethod
    def run(edo_steps, cycle):
        print_family(cycle, lengths=[6, 7, 8, 9])
