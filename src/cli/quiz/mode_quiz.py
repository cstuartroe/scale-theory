from random import randrange, choice
from src.edo import EDOInterval
from src.scales import Cycle
from .common import quiz_parser, quiz_loop, get_bass_note

parser = quiz_parser("distinguish modes")
parser.add_argument("-C", "--cycle_name", metavar="cycle", type=str, default="diatonic",
                    help="The cycle to take intervals from - may be a "
                         "name or a comma-separated list of jumps")
parser.add_argument("-g", "--groups", default=4, type=int,
                    help="How many note groupings to play")


class ModeQuiz:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, groups, cycle: Cycle, **midi_params):
        def genf():
            mode_num = randrange(cycle.size())
            mode = cycle.modes[mode_num]
            ivls = []
            available_ivls = set(mode.intervals())

            for i in range(groups):
                ivls.append(EDOInterval(0, edo_steps))
                while len(ivls) < (i+1) * 4:
                    if len(available_ivls) == 0:
                        available_ivls = set(mode.intervals())

                    ivl = choice(list(available_ivls))
                    if ivl != ivls[-1]:
                        ivls.append(ivl)
                        available_ivls.remove(ivl)

            bass_note = get_bass_note(edo_steps)
            notes = [(bass_note + ivl.steps,) for ivl in ivls]

            answer = str(mode_num + 1)

            return answer, notes, midi_params

        quiz_loop(genf)
