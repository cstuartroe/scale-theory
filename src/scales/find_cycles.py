from .scales import Cycle
from functools import cache
import math


# This method is naive in that it uses find_mode_tuples, which will output all possible modes
# This is less efficient than algorithms that avoid generating multiple modes of the same cycle
@cache
def find_mode_tuples_naive(scale_size, edo_steps):
    if scale_size == 1:
        return [(edo_steps,)]

    out = []
    for jump in range(1, edo_steps - scale_size + 2):
        for mode_tuple in find_mode_tuples_naive(scale_size - 1, edo_steps - jump):
            out.append((jump, *mode_tuple))

    return out


@cache
def find_mode_tuples_with_largest_step(scale_size, edo_steps, largest_step):
    if scale_size == 1:
        return [(edo_steps,)]

    out = []
    for first_step in range(1, min(largest_step, edo_steps - scale_size + 1) + 1):
        for mode_tuple in find_mode_tuples_with_largest_step(scale_size - 1, edo_steps - first_step, largest_step):
            out.append((first_step, *mode_tuple))
    return out


@cache
def find_mode_tuples_largest_step_first(scale_size, edo_steps):
    out = []
    for largest_step in range(math.ceil(edo_steps/scale_size), edo_steps - scale_size + 2):
        for mode_tuple in find_mode_tuples_with_largest_step(scale_size - 1, edo_steps - largest_step, largest_step):
            out.append((largest_step, *mode_tuple))
    return out


@cache
def all_cycles(scale_size: int, edo_steps: int, modes_method=find_mode_tuples_largest_step_first):
    assert scale_size <= edo_steps
    print(f"Computing all cycles of size {scale_size} in {edo_steps}EDO...")
    out = set()
    for mode_tuple in modes_method(scale_size, edo_steps):
        out.add(Cycle(mode_tuple))
    return out
