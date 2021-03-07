from .scales import Cycle


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
def find_cycles_naive(scale_size, edo_steps):
    assert scale_size <= edo_steps
    out = set()
    for mode_tuple in find_mode_tuples(scale_size, edo_steps):
        out.add(Cycle(mode_tuple))
    return out


MODE_TUPLE_CACHE = {}


def find_mode_tuples_cached(scale_size, edo_steps):
    if (scale_size, edo_steps) in MODE_TUPLE_CACHE:
        return MODE_TUPLE_CACHE[(scale_size, edo_steps)]

    out = []

    if scale_size == 1:
        out = [(edo_steps,)]

    for jump in range(1, edo_steps - scale_size + 2):
        for mode_tuple in find_mode_tuples(scale_size - 1, edo_steps - jump):
            out.append((jump, *mode_tuple))

    MODE_TUPLE_CACHE[(scale_size, edo_steps)] = out
    return out


def find_cycles_cached(scale_size, edo_steps):
    assert scale_size <= edo_steps
    out = set()
    for mode_tuple in find_mode_tuples_cached(scale_size, edo_steps):
        out.add(Cycle(mode_tuple))
    return out
