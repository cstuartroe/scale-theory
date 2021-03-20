from random import randrange
from src.midi_utils import emit_midi_sequence, emit_midi_chord
from src.edo import EDO
from src.cli.utils import make_parser, ScaleTheoryError

parser = make_parser(
    description="Quiz your ability to distinguish intervals and chords",
    duration=True,
    velocity=True,
    channel=True,
)
parser.add_argument("-d", "--direction", nargs='?', default="asc", type=str, choices=["asc", "desc", "unison"],
                    help="Which direction to play notes in")


class Round:
    def __init__(self, edo, intervals, bass_note, direction, **midi_params):
        self.edo = edo
        self.intervals = intervals
        self.bass_note = bass_note
        self.direction = direction
        self.midi_params = midi_params

    def get_guess(self):
        while True:
            guess_str = input("Guess: ")
            if guess_str == "again":
                self.play()
            elif guess_str == "quit":
                raise KeyboardInterrupt
            elif guess_str in self.edo.names():
                return self.edo.names().index(guess_str)
            else:
                try:
                    return int(guess_str)
                except ValueError:
                    print("Must be an integer or a scale degree:", self.edo.names())

    def play(self):
        if self.direction == "asc":
            emit_midi_sequence(
                jumps=self.intervals,
                starting_note=self.bass_note,
                **self.midi_params,
            )

        elif self.direction == "desc":
            emit_midi_sequence(
                jumps=[-n for n in self.intervals[::-1]],
                starting_note=self.bass_note + sum(self.intervals),
                **self.midi_params,
            )
        elif self.direction == "unison":
            emit_midi_chord(
                self.intervals,
                starting_note=self.bass_note,
                **self.midi_params,
            )
        else:
            raise ValueError


class IntervalQuiz:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, direction, **kwargs):
        edo = EDO(edo_steps)

        while True:
            interval = randrange(1, edo_steps)
            bass_note = randrange(40, 90)

            r = Round(
                edo=edo,
                intervals=[interval],
                bass_note=bass_note,
                direction=direction,
                **kwargs
            )

            r.play()

            guess = r.get_guess()

            if guess == interval:
                print("Hooray!")
            else:
                print(f"Darn! It was a {edo.names()[interval]}")
                while input("Play again? ") in ['y', 'yes']:
                    r.play()
