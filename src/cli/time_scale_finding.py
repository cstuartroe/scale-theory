import argparse
from timer import Timer
from src.scales import find_cycles_naive, find_cycles_cached

parser = argparse.ArgumentParser(description='Measure the runtime of various methods for finding scales.')
parser.add_argument('scale_size', type=int, nargs='?', default=7,
                    help='number of notes in the scale')
parser.add_argument('edo_steps', type=int, nargs='?', default=12,
                    help='number of divisions of octave')


class TimeScaleFinding:
    parser = parser

    @staticmethod
    def run(scale_size, edo_steps):
        t = Timer()
        t.task("find_scales_naive")
        naive_scales = find_cycles_naive(scale_size, edo_steps)
        t.task("find_cycles_cached")
        cached_scales = find_cycles_cached(scale_size, edo_steps)
        t.clear()
        assert cached_scales == naive_scales
        print(len(naive_scales), "scales found.")
        t.log()
