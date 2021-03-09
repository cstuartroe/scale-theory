import argparse
from src.ji.consonance import DISSONANCE_FUNCTIONS


def make_parser(description, edo_steps=True, cycle=False, priorities=False, scale_size=False, max_ratio=False,
                dissonance_function=False):
    parser = argparse.ArgumentParser(description=description)

    if cycle:
        parser.add_argument("cycle_name", metavar="cycle", type=str,
                            help="The cycle to print information about - may be a "
                                 "name or a comma-separated list of jumps")

    if priorities:
        parser.add_argument("priorities", type=str,
                            help="Either the name of an existing priorities list, "
                                 "or a comma-separated list of priorities")

    if scale_size:
        parser.add_argument('-l', '--scale_size', metavar='n', type=int, nargs='?', default=7,  help='number of notes in the scale')

    if edo_steps:
        parser.add_argument("-s", "--edo_steps", metavar="n", nargs='?', type=int, default=31)

    if max_ratio:
        parser.add_argument("-m", "--max_ratio", nargs='?', type=int, metavar='n', default=50,
                            help="The largest integer to use in a frequency ratio")

    if dissonance_function:
        parser.add_argument("-f", "--dissonance_function_name", choices=DISSONANCE_FUNCTIONS.keys(), default="euler",
                            help="Choice of dissonance function to use for ranking")

    return parser
