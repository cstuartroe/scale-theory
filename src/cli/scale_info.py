from src.scales import Cycle
from src.scale_properties.cycle_stats import (
    count_present_consonances,
    count_dissonances,
    interval_diversity,
    count_chords,
    count_extensions,
    proper,
)
# from src.midi_utils import midi_to_12edo_name, get_midi_numbers
from .utils import make_parser

TETRACHORDS = {
    "maj7": ["maj3", "p5", "maj7"],
    "m7": ["m3", "p5", "m7"],
    "dom7": ["maj3", "p5", "m7"],
    "h7": ["maj3", "p5", "h7"],
    "subminadd4": ["septimal m3", "p4", "p5"],
    "submimaj7": ["septimal m3", "p5", "maj7"],
    "minmaj7": ["m7", "p5", "maj7"],
}


def scale_info(cycle: Cycle):
    print(cycle.name())

    for mode in cycle.modes:
        print("unison    ", end="")
        for jump, ivl in zip(mode.jumps, mode.intervals()):
            print(f"-{jump}->  ", ivl.name().ljust(10), end="")

        print(f"-{mode.jumps[-1]}->  ", "p8")

    for ivl in cycle.canon_mode.intervals():
        print(ivl.cents(), end=", ")
    print()

    print(f"Consonant interval diversity: {count_present_consonances(cycle)}/{len(cycle.edo().consonances)}")
    print("Total dissonances:", count_dissonances(cycle))
    print(cycle.interval_vector())
    print("Total chords:", *[count_chords(cycle, [third])[third] for third in ["septimal m3", "m3", "n3", "maj3", "septimal maj3"]])
    print("Total tetrachords:")
    for name, degrees in TETRACHORDS.items():
        if count_extensions(cycle, degrees) > 0:
            print(f"  {name}: {count_extensions(cycle, degrees)}")
    print("Proper:", proper(cycle))
    # TODO
    # print("MIDI notes:", ", ".join(map(midi_to_12edo_name, get_midi_numbers(cycle))))
    print()


class ScaleInfo:
    parser = make_parser(
        description="Print info about a single cycle",
        cycle=True,
    )

    @staticmethod
    def run(cycle):
        scale_info(cycle)
