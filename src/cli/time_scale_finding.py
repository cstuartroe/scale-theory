from timer import Timer
from src.scales.find_cycles import find_cycles_naive
from .utils import make_parser

METHODS = [find_cycles_naive]


class TimeScaleFinding:
    parser = make_parser(
        description='Measure the runtime of various methods for finding scales.',
        scale_size=True,
    )

    @staticmethod
    def run(scale_size, edo_steps):
        t = Timer()

        computed_cycles = []
        for method in METHODS:
            method.cache_clear()
            t.task(method.__name__)
            computed_cycles.append(method(scale_size, edo_steps))
            t.clear()

        for c in computed_cycles[1:]:
            # we want to make sure the algorithms produce the same end result
            assert c == computed_cycles[0]

        print(len(computed_cycles[0]), "scales found.")

        t.log()
