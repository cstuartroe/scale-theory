from random import choice, shuffle, randrange
from src.edo import EDOInterval
from src.scales import Cycle, EDOChord
from .common import quiz_parser, quiz_loop, get_bass_note

QUIZZABLE_CHORD_SHAPES = [
    "major",
    "minor",
    "sus4",
    "m7",
    "dom7",
    "maj7",
    "diminished",
    "augmented",
]

parser = quiz_parser("distinguish modes", length=2, cycle="diatonic")
parser.add_argument("-S", "--shapes", metavar="shape", type=str, default=",".join(QUIZZABLE_CHORD_SHAPES),
                    help="The set of chord shapes to quiz on")
parser.add_argument('-m', '--mode', default=None, type=str, metavar='n',
                    help="The mode of the cycle to use")

class ProgressionQuiz:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, shapes, fixed_root, length, cycle: Cycle, mode: str, **midi_params):
        shapes = [shape.strip() for shape in shapes.split(",")]
        for shape in shapes:
            if shape not in QUIZZABLE_CHORD_SHAPES:
                print("Invalid chord shape:", shape)
                print("Accepted chord shapes:", ", ".join(QUIZZABLE_CHORD_SHAPES))
                return

        print("Quizzable shapes:", ", ".join(EDOChord.used_shape_names(shapes, edo_steps)))

        def genf():
            if mode:
                tonic_mode = cycle.modes[int(mode)]
            else:
                tonic_mode = choice(cycle.modes)

            notes = []
            first_tonic_midi_number = get_bass_note(fixed_root, edo_steps)
            chord_names = []
            cutoff = randrange(-edo_steps//4, edo_steps//2 + 1)

            def add_chord(ivl: EDOInterval):
                shuffled_shapes = [*shapes]
                shuffle(shuffled_shapes)
                for shape_name in shuffled_shapes:
                    chord = EDOChord.by_name(shape_name, edo_steps)

                    fits = True
                    for ci in chord.intervals():
                        steps = (ivl.steps + ci.steps) % edo_steps
                        if steps != 0 and EDOInterval(steps, edo_steps) not in tonic_mode.intervals():
                            fits = False
                            break

                    if fits:
                        tonic_midi_number = first_tonic_midi_number + ivl.steps

                        inversion = 0
                        if edo_steps - ivl.steps <= cutoff:
                            tonic_midi_number -= edo_steps
                        else:
                            for ci in chord.intervals():
                                if ivl.steps + ci.steps >= edo_steps - cutoff:
                                    inversion -= 1
                            inversion %= len(chord.intervals()) + 1

                        notes.append(chord.invert(inversion).get_note_numbers(tonic_midi_number=tonic_midi_number))
                        chord_names.append(ivl.name() + ":" + shape_name)

                        break

            add_chord(EDOInterval(0, edo_steps))
            while len(notes) < length:
                add_chord(choice(tonic_mode.intervals()))

            return ",".join(chord_names), notes, {"edo": edo_steps, **midi_params}

        quiz_loop(genf)
