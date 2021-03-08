from .scales import Cycle
from functools import cache


@cache
def find_mode_tuples(scale_size, edo_steps):
    if scale_size == 1:
        return [(edo_steps,)]

    out = []
    for jump in range(1, edo_steps - scale_size + 2):
        for mode_tuple in find_mode_tuples(scale_size - 1, edo_steps - jump):
            out.append((jump, *mode_tuple))

    return out


# This method is naive in that it uses find_mode_tuples, which will output all possible modes
# This is less efficient than algorithms that avoid generating multiple modes of the same cycle
@cache
def find_cycles_naive(scale_size, edo_steps):
    print(f"Computing all cycles of size {scale_size} in {edo_steps}EDO...")
    assert scale_size <= edo_steps
    out = set()
    for mode_tuple in find_mode_tuples(scale_size, edo_steps):
        out.add(Cycle(mode_tuple))
    return out


# this is just set to whatever should be the default method
all_cycles = find_cycles_naive
