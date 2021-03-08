import regex
from src.scales import Cycle
from src.scale_properties import CYCLE_STATS, PRIORITY_SEQUENCES


def resolve_cycle_name(edo_steps, cycle_name):
    cycle = Cycle.by_name(edo_steps, cycle_name)
    if cycle:
        return cycle
    else:
        try:
            jumps = [int(j) for j in cycle_name.split(",")]
            if sum(jumps) != edo_steps:
                raise ValueError(f"Jumps should add to {edo_steps}, but actually add to {sum(jumps)}")
            return Cycle(jumps)
        except ValueError:
            raise ValueError("Not a known scale name or valid comma-separated list of integers")


def resolve_priorities(priorities_string):
    if priorities_string in PRIORITY_SEQUENCES:
        return PRIORITY_SEQUENCES[priorities_string]

    priorities_strings = regex.fullmatch(r"(([\w\d]+\([\w\d ,]*\)),?)+", priorities_string).captures(2)
    priorities = []

    for priorities_string in priorities_strings:
        m = regex.fullmatch(r"([\w\d]+)\((([\w\d ]+),?)*\)", priorities_string)
        method_name = m.groups()[0]
        args = m.captures(3)
        method = CYCLE_STATS[method_name]
        priorities.append(lambda cycle: method(cycle, *([args] if len(args) > 0 else ())))

    return priorities


def resolve(parsed_args):
    out = {}
    for k, v in vars(parsed_args).items():
        if k == "cycle_name":
            out["cycle"] = resolve_cycle_name(parsed_args.edo_steps, v)

        elif k == "priorities":
            out["priorities"] = resolve_priorities(v)

        else:
            out[k] = v

    return out
