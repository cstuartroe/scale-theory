from tabulate import tabulate
from src.ji import just_chords
from src.edo import EDO
from src.scales import Mode
from .utils import make_parser
from timer import Timer


MAJOR_EDOS = [12, 17, 19, 22, 24, 31]


parser = make_parser(description="List just chords in order of consonance", edo_steps=False, dissonance_function=True,
                     max_ratio=True, num_results=True)
parser.add_argument("-t", "--tones", type=int, metavar='n', default=3,
                    help="The number of tones in the chord")


class FindJustChords:
    parser = parser

    @staticmethod
    def run(tones, max_ratio, dissonance_function, num_results):
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
        chords_with_dissonance = [(c, dissonance_function(c)) for c in chords]
        sorted_chords = sorted(chords_with_dissonance, key=lambda x: x[1], reverse=True)

        for chord, _ in sorted_chords[-num_results:]:
            table.append((
                ":".join(map(str, chord.ratio)),
                dissonance_function(chord),
                chord.name_with_inversion(),
                ", ".join(map(str, chord.cents())),
                *(
                    ",".join([str(jump) for jump in Mode.from_just_chord(chord, edo_steps).jumps])
                    for edo_steps in MAJOR_EDOS
                ),
            ))

        print(tabulate(table))

        print(len(chords), "chords found.")
