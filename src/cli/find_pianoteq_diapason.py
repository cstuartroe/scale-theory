from src.player_utils import (
    midi_number_frequency,
    midi_number_standard_frequency,
    midi_name_to_number,
    BASE_MIDI_NOTE,
)
from .utils import make_parser

parser = make_parser("Determine the frequency to use as the diapason in Pianoteq in "
                     "order to match MIDI number 52 to a particular note in standard tuning")
parser.add_argument("note", type=str)


class FindPianoteqDiapason:
    parser = parser

    pass_edo_steps = True

    @staticmethod
    def run(edo_steps, note):
        desired_frequency = midi_number_standard_frequency(midi_name_to_number(note))

        print(midi_number_frequency(
            69,
            edo_steps,
            BASE_MIDI_NOTE,
            desired_frequency,
        ))
