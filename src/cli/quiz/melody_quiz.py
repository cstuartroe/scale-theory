from random import randrange, choice
from src.edo import EDOInterval, EDO
from src.scales import Cycle, EDOChord
from .common import quiz_parser, quiz_loop, get_bass_note

parser = quiz_parser("transcribe melodies", cycle=True, length=3)
parser.add_argument("-M", "--max_leap", default=705, type=int,
                    help="Maximum distance in cents between adjacent notes")
parser.add_argument("-P", "--progression", action="store_true",
                    help="Introduce melody with a chord IV-V-I chord progression "
                         "rather than a single note")


class MelodyQuiz:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, length, max_leap, fixed_root, progression, cycle: Cycle, **midi_params):
        print("Interval names:", ", ".join(EDO(edo_steps).names()))

        def genf():
            mode = cycle.modes[randrange(cycle.size())]
            ivls = []
            while len(ivls) < length:
                ivl = choice(mode.intervals())

                if len(ivls) > 0:
                    prev = ivls[-1]
                elif not progression:
                    prev = EDOInterval(0, edo_steps)
                else:
                    prev = None

                if prev is None or (ivl != prev and abs(prev.cents() - ivl.cents()) <= max_leap):
                    ivls.append(ivl)

            bass_note = get_bass_note(fixed_root, edo_steps)
            if progression:
                p4 = bass_note + EDOInterval.by_name("p4", edo_steps).steps
                p5 = bass_note + EDOInterval.by_name("p5", edo_steps).steps
                notes = [
                    EDOChord.by_name("major", edo_steps).get_note_numbers(p4),
                    EDOChord.by_name("major", edo_steps).get_note_numbers(p5),
                    EDOChord.by_name("major", edo_steps).get_note_numbers(bass_note),
                    (),
                ]
            else:
                notes = [(bass_note,)]

            notes += [(bass_note + ivl.steps,) for ivl in ivls]

            answer = ",".join(ivl.name() for ivl in ivls)

            return answer, notes, midi_params

        quiz_loop(genf)
