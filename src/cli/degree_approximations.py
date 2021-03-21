from src.edo import EDO
from src.ji import just_chords
from .utils import make_parser


parser = make_parser(description="Identify which just intervals each step of a given EDO system approximates",
                     edo_steps=True, max_ratio=True, dissonance_function=True)
parser.add_argument("-t", "--threshold", default=15, type=int, metavar='n',
                    help="The highest dissonance allowed for an interval to be shown")


class DegreeApproximations:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, max_ratio, dissonance_function, threshold):
        edo = EDO(edo_steps)
        approximations = dict([(deg, set()) for deg in edo.degrees()])

        for c in just_chords(2, max_ratio):
            ivl = c.intervals()[0]  # TODO: change strategies?
            if dissonance_function(ivl) < threshold:
                deg = edo.approximate(ivl)
                approximations[deg].add(ivl)

        for deg in edo.degrees():
            print(deg.name())
            for ivl in approximations[deg]:
                diff = round(deg.cents() - ivl.cents(), 1)
                print(f"{ivl.num}:{ivl.denom}    {dissonance_function(ivl)} ({'+' if diff > 0 else ''}{diff})")
            print()
