from random import choice
from src.scales import EDOChord
from src.midi_utils import BASE_MIDI_NOTE
from .common import quiz_parser, quiz_loop, get_bass_note

QUIZZABLE_CHORD_SHAPES = [
    "major",
    "minor",
    "sus4",
    "m7",
    "dom7",
    "maj7",
    "h7",
    "septimal minor",
    "septimal m7",
    "diminished",
    "augmented",
]


parser = quiz_parser("distinguish modes")
parser.add_argument("-S", "--shapes", metavar="shape", type=str, default=",".join(QUIZZABLE_CHORD_SHAPES),
                    help="The set of chord shapes to quiz on")
parser.add_argument("-I", "--with_inversions", action="store_true",
                    help="Whether to quiz on inversions")
parser.add_argument("-F", "--fixed_root", action="store_true",
                    help="Whether to keep a fixed root note")


class ChordShapeQuiz:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, shapes, with_inversions, fixed_root, **midi_params):
        shapes = [shape.strip() for shape in shapes.split(",")]
        for shape in shapes:
            if shape not in QUIZZABLE_CHORD_SHAPES:
                print("Invalid chord shape:", shape)
                print("Accepted chord shapes:", ", ".join(QUIZZABLE_CHORD_SHAPES))
                return

        print("Quizzable shapes:", ", ".join(EDOChord.used_shape_names(shapes, edo_steps)))

        def genf():
            shape = choice(shapes)
            ec = EDOChord.by_name(shape, edo_steps)
            if with_inversions or not fixed_root:
                ec = choice(ec.inversions())

            bass_note = BASE_MIDI_NOTE if fixed_root else get_bass_note(edo_steps)
            notes = [bass_note] + [bass_note + ivl.steps for ivl in ec.intervals()]

            name, inv = ec.name_and_inversion()
            if with_inversions:
                answer = f"{name} {inv}"
            else:
                answer = name

            return answer, [notes], midi_params

        quiz_loop(genf)
