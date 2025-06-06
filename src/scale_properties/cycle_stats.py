from typing import List
from src.ji import JI
from src.edo import EDOInterval
from src.scales import Cycle


def intervals_in_edo(edo, interval_names):
    return set(edo.approximate(JI.by_name(ivl_name)) for ivl_name in interval_names)


def count_by_name(cycle: Cycle, name: str):
    return cycle.interval_counts()[cycle.edo().approximate(JI.by_name(name))]


def count_p5s(cycle: Cycle):
    return count_by_name(cycle, "p5")


def interval_diversity(cycle: Cycle, important_intervals: List[str] = None):
    intervals = cycle.interval_set()
    if important_intervals:
        intervals = intervals & intervals_in_edo(cycle.edo(), important_intervals)

    return len(intervals)


def count_chords(cycle: Cycle, third_names: List[str]):
    fifth = cycle.edo().approximate(JI.by_name("p5"))
    chords = dict([(name, 0) for name in third_names])
    for mode in cycle.modes:
        if fifth in mode.interval_set():
            for name, third in zip(third_names, intervals_in_edo(cycle.edo(), third_names)):
                if third in mode.interval_set():
                    chords[name] += 1
    return chords


def count_chord_richness(cycle: Cycle, third_names: List[str]):
    return min(count_chords(cycle, third_names).values())


def count_total_chords(cycle: Cycle, third_names: List[str]):
    return sum(count_chords(cycle, third_names).values())


def count_distinct_chord_roots(cycle: Cycle, third_names: List[str]):
    fifth = cycle.edo().approximate(JI.by_name("p5"))
    total = 0
    for mode in cycle.modes:
        if fifth in mode.interval_set():
            for third in intervals_in_edo(cycle.edo(), third_names):
                if third in mode.interval_set():
                    total += 1
                    break
    return total


def count_extensions(cycle: Cycle, ivl_names: List[str]):
    total = 0
    for mode in cycle.modes:
        if all(ivl in mode.interval_set() for ivl in intervals_in_edo(cycle.edo(), ivl_names)):
            total += 1
    return total


# These methods are intended to avoid the assumption that a non-consonance is a dissonance
# In 31EDO in particular there are a number of intervals I consider to be intermediate
# Consonances and especially dissonances can be quite EDO-specific, so passing them in by name won't do

def count_present_consonances(cycle: Cycle):
    return len(set(cycle.edo().consonances) & cycle.interval_set())


def count_dissonances(cycle: Cycle):
    return -sum([cycle.interval_counts().get(d, 0) for d in cycle.edo().dissonances])


def count_intervals(cycle: Cycle, intervals: list[int]):
    ivs = [EDOInterval(i, cycle.edo_steps()) for i in intervals]
    return -sum([cycle.interval_counts().get(i, 0) for i in ivs])


def largest_jump(cycle: Cycle):
    return max(cycle.jumps)


def wonkiness(cycle: Cycle):
    average_jump = cycle.edo_steps()/len(cycle.jumps)
    out = 0
    for jump in cycle.jumps:
        out += (jump - average_jump)**2
    return round(out, 2)


HATED_INTERVALS: dict[int, list[int]] = {
    16: [6],
    22: [1, 8],
    31: [1, 9, 11, 12],
}


def intervals_i_hate(cycle: Cycle):
    return count_intervals(cycle, HATED_INTERVALS.get(cycle.edo_steps(), []))


class Proper:
    IMPROPER = "improper"
    PROPER = "proper"
    STRICTLY_PROPER = "strictly_proper"


def proper(cycle: Cycle):
    degrees = [set() for _ in range(cycle.size() - 1)]
    for mode in cycle.modes:
        for i, ivl in enumerate(mode.intervals()):
            degrees[i].add(ivl)

    not_strict = False
    for deg1, deg2 in zip(degrees[:-1], degrees[1:]):
        x, y = max(deg1), min(deg2)
        if x > y:
            return Proper.IMPROPER
        elif x == y:
            not_strict = True

    return Proper.PROPER if not_strict else Proper.STRICTLY_PROPER


_methods = [
    count_p5s,
    interval_diversity,
    count_chord_richness,
    count_total_chords,
    count_distinct_chord_roots,
    count_extensions,
    count_present_consonances,
    count_dissonances,
    proper,
]

CYCLE_STATS = dict([
    (f.__name__, f)
    for f in _methods
])
