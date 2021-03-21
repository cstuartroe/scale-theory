from random import randrange
from src.midi_utils import emit_midi_sequence, emit_midi_chord
from src.edo import EDO
from .common import quiz_parser, quiz_loop

parser = quiz_parser("distinguish intervals")
parser.add_argument("-d", "--direction", nargs='?', default="asc", type=str, choices=["asc", "desc", "unison"],
                    help="Which direction to play notes in")


class IntervalRound:
    def __init__(self, edo, interval, bass_note, direction, **midi_params):
        self.edo = edo
        self.interval = interval
        self.bass_note = bass_note
        self.direction = direction
        self.midi_params = midi_params

    def play(self):
        if self.direction == "asc":
            emit_midi_sequence(
                jumps=[self.interval],
                starting_note=self.bass_note,
                **self.midi_params,
            )

        elif self.direction == "desc":
            emit_midi_sequence(
                jumps=[-self.interval],
                starting_note=self.bass_note + self.interval,
                **self.midi_params,
            )

        elif self.direction == "unison":
            emit_midi_chord(
                [self.interval],
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
        print("Interval names:", ", ".join(edo.names()))

        def genf():
            interval = randrange(1, edo_steps)
            bass_note = randrange(40, 40 + int(edo_steps * 1.5))

            return edo.names()[interval], {
                "edo": edo,
                "interval": interval,
                "bass_note": bass_note,
                "direction": direction,
                **kwargs,
            }

        quiz_loop(genf, IntervalRound)
