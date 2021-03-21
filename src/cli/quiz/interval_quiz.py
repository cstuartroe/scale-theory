from random import randrange
from src.edo import EDO, EDOInterval
from .common import quiz_parser, quiz_loop, get_bass_note

parser = quiz_parser("distinguish intervals")
parser.add_argument("-d", "--direction", default="asc", type=str, choices=["asc", "desc", "unison"],
                    help="Which direction to play notes in")


class IntervalQuiz:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, direction, **midi_params):
        print("Interval names:", ", ".join(EDO(edo_steps).names()))

        def genf():
            interval = EDOInterval(randrange(1, edo_steps), edo_steps)
            bass_note = get_bass_note(edo_steps)

            answer = interval.name()

            if direction == "asc":
                notes = [(bass_note,), (bass_note + interval.steps,)]

            elif direction == "desc":
                notes = [(bass_note + interval.steps,), (bass_note,)]

            elif direction == "unison":
                notes = [(bass_note,), (bass_note + interval.steps,)]

            else:
                raise ValueError

            return answer, notes, midi_params

        quiz_loop(genf)
