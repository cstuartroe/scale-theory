from random import choice
from src.edo import EDO, EDOInterval
from .common import quiz_parser, quiz_loop, get_bass_note

parser = quiz_parser("distinguish intervals")
parser.add_argument("-d", "--direction", default="asc", type=str, choices=["asc", "desc", "unison"],
                    help="Which direction to play notes in")
parser.add_argument("-i", "--intervals", default=None, type=str,
                    help="Which scale degrees to quiz on")


class IntervalQuiz:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, direction, intervals, fixed_root, **midi_params):
        if intervals is None:
            interval_names = EDO(edo_steps).names()
        else:
            interval_names = [i.strip() for i in intervals.split(",")]

        print("Intervals being quizzed:", ", ".join(interval_names))

        def genf():
            interval = EDOInterval.by_name(choice(interval_names), edo_steps)
            bass_note = get_bass_note(fixed_root, edo_steps)

            answer = interval.name()

            if direction == "asc":
                notes = [(bass_note,), (bass_note + interval.steps,)]

            elif direction == "desc":
                notes = [(bass_note + interval.steps,), (bass_note,)]

            elif direction == "unison":
                notes = [(bass_note, bass_note + interval.steps,)]

            else:
                raise ValueError

            return answer, notes, midi_params

        quiz_loop(genf)
