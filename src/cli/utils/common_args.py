import argparse


def make_parser(description, edo_steps=True, cycle=False, priorities=False, scale_size=False):
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
        parser.add_argument('scale_size', type=int, nargs='?', default=7,  help='number of notes in the scale')

    if edo_steps:
        parser.add_argument("-s", "--edo_steps", metavar="edo_steps", nargs='?', type=int, default=31)

    return parser
