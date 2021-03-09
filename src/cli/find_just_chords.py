from tabulate import tabulate
from src.edo import EDO
from src.ji import just_chords
from .utils import make_parser


MAJOR_EDOS = [12, 17, 19, 22, 24, 31]


parser = make_parser(description="List just chords in order of consonance", edo_steps=True, dissonance_function=True,
                     max_ratio=True)
parser.add_argument("-t", "--tones", nargs='?', type=int, metavar='n', default=3,
                    help="The number of tones in the chord")


class FindJustChords:
    parser = parser

    @staticmethod
    def run(tones, max_ratio, dissonance_function):
        table = [
            (
                "Ratio",
                "Dissonance",
                "Name",
                "Cents",
                *(
                    f"{s}EDO Approximation"
                    for s in MAJOR_EDOS
                )
            )
        ]

        chords = list(just_chords(tones, max_ratio))

        for chord in sorted(chords, key=lambda c: dissonance_function(c), reverse=True):
            table.append((
                ":".join(map(str, chord.ratio)),
                dissonance_function(chord),
                chord.name_with_inversion(),
                ", ".join(map(str, chord.cents())),
                *(
                    ",".join([str(ivl.steps) for ivl in chord.approximation_in(EDO(edo_steps))])
                    for edo_steps in MAJOR_EDOS
                ),
            ))

        print(tabulate(table))
