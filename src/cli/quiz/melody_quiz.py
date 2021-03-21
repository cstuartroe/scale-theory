from random import randrange, choice
from src.edo import EDOInterval, EDO
from src.scales import Cycle
from .common import quiz_parser, quiz_loop, get_bass_note

parser = quiz_parser("transcribe melodies")
parser.add_argument("-C", "--cycle_name", metavar="cycle", type=str, default="diatonic",
                    help="The cycle to take intervals from - may be a "
                         "name or a comma-separated list of jumps")
parser.add_argument("-l", "--length", default=4, type=int,
                    help="How many melody notes to include")
parser.add_argument("-M", "--max_leap", default=705, type=int,
                    help="Maximum distance in cents between adjacent notes")


class MelodyQuiz:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, length, max_leap, cycle: Cycle, **midi_params):
        print("Interval names:", ", ".join(EDO(edo_steps).names()))

        def genf():
            mode = cycle.modes[randrange(cycle.size())]
            ivls = [EDOInterval(0, edo_steps)]
            while len(ivls) < length:
                ivl = choice(mode.intervals())
                if ivl != ivls[-1] and abs(ivls[-1].cents() - ivl.cents()) <= max_leap:
                    ivls.append(ivl)

            bass_note = get_bass_note(edo_steps)
            notes = [(bass_note + ivl.steps,) for ivl in ivls]

            answer = ",".join(ivl.name() for ivl in ivls[1:])

            return answer, notes, midi_params

        quiz_loop(genf)
