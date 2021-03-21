import argparse
from src.ji.consonance import DISSONANCE_FUNCTIONS


def make_parser(description, edo_steps=True, cycle=False, priorities=False, scale_size=False, max_ratio=False,
                dissonance_function=False, duration=False, velocity=False, channel=False, num_results=False):
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
        parser.add_argument('-l', '--scale_size', metavar='n', type=int, default=7,  help='number of notes in the scale')

    if edo_steps:
        parser.add_argument("-s", "--edo_steps", metavar="n", type=int, default=31)

    if max_ratio:
        parser.add_argument("-m", "--max_ratio", type=int, metavar='n', default=60,
                            help="The largest integer to use in a frequency ratio")

    if dissonance_function:
        parser.add_argument("-f", "--dissonance_function_name", choices=DISSONANCE_FUNCTIONS.keys(), default="euler",
                            help="Choice of dissonance function to use for ranking")

    if duration:
        parser.add_argument("-D", "--note_duration", default=500, type=int, metavar="n",
                            help="The duration in ms of each note in the scale")

    if velocity:
        parser.add_argument("-v", "--velocity", default=64, type=int, metavar='n',
                            help="The midi velocity of each note (0-255)")

    if channel:
        parser.add_argument('-c', '--channel', default=0, type=int, metavar='n',
                            help="The midi channel to send scale to")

    if num_results:
        parser.add_argument('-N', '--num_results', default=50, type=int, metavar='n',
                            help="The number of top results to list")

    return parser
