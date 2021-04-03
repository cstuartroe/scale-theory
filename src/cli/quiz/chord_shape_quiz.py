from random import choice, randrange
from src.scales import EDOChord
from .common import quiz_parser, quiz_loop, get_bass_note
from ...edo import EDOInterval

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


parser = quiz_parser("distinguish modes", length=1)
parser.add_argument("-S", "--shapes", metavar="shape", type=str, default=",".join(QUIZZABLE_CHORD_SHAPES),
                    help="The set of chord shapes to quiz on")
parser.add_argument("-I", "--with_inversions", action="store_true",
                    help="Whether to quiz on inversions")


class ChordsQuiz:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, shapes, with_inversions, fixed_root, length, **midi_params):
        shapes = [shape.strip() for shape in shapes.split(",")]
        for shape in shapes:
            if shape not in QUIZZABLE_CHORD_SHAPES:
                print("Invalid chord shape:", shape)
                print("Accepted chord shapes:", ", ".join(QUIZZABLE_CHORD_SHAPES))
                return

        print("Quizzable shapes:", ", ".join(EDOChord.used_shape_names(shapes, edo_steps)))

        def genf():
            chords = []
            for _ in range(length):
                shape = choice(shapes)
                ec = EDOChord.by_name(shape, edo_steps)
                if with_inversions or not fixed_root:
                    ec = choice(ec.inversions())
                chords.append(ec)

            bass_note = get_bass_note(fixed_root, edo_steps)
            tonic_jumps = [0] + [randrange(1, edo_steps) for _ in range(length - 1)]

            notes = [
                chord.get_note_numbers(tonic_midi_number=bass_note + tonic_jump)
                for chord, tonic_jump in zip(chords, tonic_jumps)
            ]

            def short_name(chord):
                name, inv = chord.name_and_inversion()
                if with_inversions:
                    return f"{name} {inv}"
                else:
                    return name

            answer = short_name(chords[0])
            for chord, tonic_jump in zip(chords[1:], tonic_jumps[1:]):
                answer += f", {EDOInterval(tonic_jump, edo_steps).name()} {short_name(chord)}"

            return answer, notes, midi_params

        quiz_loop(genf)
