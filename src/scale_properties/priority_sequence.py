from .cycle_stats import *


PRIORITY_SEQUENCES = {
    "h7n7_priorities": (
        lambda cycle: interval_diversity(cycle, ["n2", "septimal m3", "m3", "n3", "maj3", "h7"]),
        count18s,
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "n3", "maj3"]),
        lambda cycle: count_total_chords(cycle, ["m3", "maj3"])
    ),

    "diatonic_priorities": (count18s,),

    "dioudeteric_priorities": (
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "n3", "maj3", "septimal maj3"]),
        lambda cycle: count_total_chords(cycle, ["septimal m3", "m3", "n3", "maj3", "septimal maj3"])
    ),

    "greek_letter_priorities": (
        lambda cycle: interval_diversity(cycle, ["septimal m3", "h7"]),
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "maj3"]),
        lambda cycle: count_total_chords(cycle, ["m3", "maj3"]),
        count18s
    ),

    "theta_subcycle_priorities": (
        lambda cycle: interval_diversity(cycle, ["septimal maj2", "septimal m3", "h7"]),
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "maj3"]),
        lambda cycle: count_total_chords(cycle, ["m3", "maj3"]),
        count18s
    ),

    "god_B_priorities": (
        lambda cycle: interval_diversity(cycle, ["n2", "septimal m3", "m3", "n3", "maj3", "h7"]),
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "n3", "maj3", "septimal maj3"]),
        lambda cycle: count_total_chords(cycle, ["m3", "maj3"]),
        count18s
    ),

    "variety_priorities": (
        count18s,
        interval_diversity,
    ),

    "melodic_priorities": (
        lambda cycle: cycle.edo().pentatonic() in cycle.children(5),
        proper,
        interval_diversity,
    ),

    "harmonic_priorities": (
        lambda cycle: cycle.edo().pentatonic() in cycle.children(5),
        lambda cycle: interval_diversity(cycle, ["n2", "septimal maj2", "septimal m3", "n3", "small septimal tritone"]),
        lambda cycle: count_distinct_chord_roots(cycle, ["septimal m3", "m3", "maj3"]),
        lambda cycle: count_total_chords(cycle, ["septimal m3", "m3", "maj3"]),
        count18s,
    ),

    "consonance_priorities": (
        count18s,
        lambda cycle: count_total_chords(cycle, ["septimal m3", "m3", "maj3"]),
        lambda cycle: count_present_consonances(cycle),
        interval_diversity,
        lambda cycle: count_dissonances(cycle),
    ),

    "minor_chord_priorities": (
        lambda cycle: count_total_chords(cycle, ["septimal m3"]),
        count18s,
    )
}