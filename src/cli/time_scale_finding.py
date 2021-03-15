from timer import Timer
from src.scales.find_cycles import find_mode_tuples_naive, find_mode_tuples_largest_step_first
from .utils import make_parser
from src.scales import Cycle

METHODS = [find_mode_tuples_naive, find_mode_tuples_largest_step_first]


class TimeScaleFinding:
    parser = make_parser(
        description='Measure the runtime of various methods for finding scales.',
        scale_size=True,
    )

    pass_edo_steps = True

    @staticmethod
    def run(scale_size, edo_steps):
        t = Timer()

        computed_cycles = []
        num_computed_modes = {}
        for method in METHODS:
            method.cache_clear()
            t.task(method.__name__)
            modes = list(method(scale_size, edo_steps))
            t.clear()
            computed_cycles.append(set([Cycle(mode) for mode in modes]))
            num_computed_modes[method.__name__] = len(modes)
            t.clear()

        for c in computed_cycles[1:]:
            # we want to make sure the algorithms produce the same end result
            assert c == computed_cycles[0]

        print(len(computed_cycles[0]), "cycles found.")
        print("Number of modes computed:")
        for method_name, num_modes in num_computed_modes.items():
            print(method_name, num_modes)

        t.log()
