from .cycle_stats import *


PRIORITY_SEQUENCES = {
    "h7n7_priorities": (
        lambda cycle: interval_diversity(cycle, ["n2", "septimal m3", "m3", "n3", "maj3", "h7"]),
        count_p5s,
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "n3", "maj3"]),
        lambda cycle: count_total_chords(cycle, ["m3", "maj3"])
    ),

    "diatonic_priorities": (proper, count_p5s),

    "dioudeteric_priorities": (
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "n3", "maj3", "septimal maj3"]),
        lambda cycle: count_total_chords(cycle, ["septimal m3", "m3", "n3", "maj3", "septimal maj3"])
    ),

    "greek_letter_priorities": (
        lambda cycle: interval_diversity(cycle, ["septimal m3", "h7"]),
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "maj3"]),
        lambda cycle: count_total_chords(cycle, ["m3", "maj3"]),
        count_p5s
    ),

    "theta_subcycle_priorities": (
        lambda cycle: interval_diversity(cycle, ["septimal maj2", "septimal m3", "h7"]),
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "maj3"]),
        lambda cycle: count_total_chords(cycle, ["m3", "maj3"]),
        count_p5s
    ),

    "god_B_priorities": (
        lambda cycle: interval_diversity(cycle, ["n2", "septimal m3", "m3", "n3", "maj3", "h7"]),
        lambda cycle: count_chord_richness(cycle, ["septimal m3", "m3", "n3", "maj3", "septimal maj3"]),
        lambda cycle: count_total_chords(cycle, ["m3", "maj3"]),
        count_p5s
    ),

    "variety_priorities": (
        count_p5s,
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
        count_p5s,
    ),

    "consonance_priorities": (
        count_p5s,
        lambda cycle: count_total_chords(cycle, ["septimal m3", "m3", "maj3"]),
        lambda cycle: count_present_consonances(cycle),
        interval_diversity,
        lambda cycle: count_dissonances(cycle),
    ),

    "minor_chord_priorities": (
        lambda cycle: count_total_chords(cycle, ["septimal m3"]),
        count_p5s,
    ),

    "total_chord_priorities": (
        proper,
        lambda cycle: count_distinct_chord_roots(cycle, ["septimal m3", "m3", "maj3"]),
        lambda cycle: count_total_chords(cycle, ["septimal m3", "m3", "maj3"]),
        count_p5s,
    ),

    "n2_not_n3": (
        lambda cycle: -count_by_name(cycle, "n3"),
        count_p5s,
        lambda cycle: count_by_name(cycle, "n2"),
        proper,
        lambda cycle: count_total_chords(cycle, ["septimal m3", "m3", "maj3"]),
    ),

    "hatred_avoidance": (
        lambda cycle: intervals_i_hate(cycle),
        lambda cycle: -wonkiness(cycle),
        proper,
        interval_diversity,
        count_p5s,
        lambda cycle: count_total_chords(cycle, ["maj3"]),
        lambda cycle: count_total_chords(cycle, ["m3"]),
    ),
}