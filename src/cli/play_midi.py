import time
from src.scales import Cycle
from .utils import make_parser, ScaleTheoryError

parser = make_parser(
    description="Play a scale or mode(s) of a scale",
    cycle=True,
)

parser.add_argument("-d", "--duration", nargs='?', default=500, type=int, metavar="n",
                    help="The duration in ms of each note in the scale")
parser.add_argument("-v", "--velocity", nargs='?', default=64, type=int, metavar='n',
                    help="The midi velocity of each note (0-255)")
parser.add_argument('-m', '--mode', nargs='?', default=None, type=str, metavar='n',
                    help="The mode(s) of a cycle to play. Leave blank to play 2 octaves, specify a mode with a number, "
                         "or specify 'all' to play all modes in order")
parser.add_argument('-c', '--channel', nargs='?', default=0, type=int, metavar='n',
                    help="The midi channel to send scale to")


class PlayMidi:
    parser = parser

    @staticmethod
    def run(cycle: Cycle, duration, velocity, mode, channel):
        if mode is None:
            cycle.play_midi(note_duration=duration, velocity=velocity, channel=channel)
        elif mode == 'all':
            for i, m in enumerate(cycle.modes):
                if i != 0:
                    time.sleep(1)
                m.play_midi(note_duration=duration, velocity=velocity, channel=channel)
        else:
            try:
                mode_number = int(mode)
            except ValueError:
                raise ScaleTheoryError("Mode should be left blank, or be 'all' or an integer")

            try:
                m = cycle.modes[mode_number - 1]
            except ValueError:
                raise ScaleTheoryError(f"Mode number too high (max {len(cycle.modes)})")

            m.play_midi(note_duration=duration, velocity=velocity, channel=channel)
