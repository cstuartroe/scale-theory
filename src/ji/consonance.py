import math
from functools import cache


@cache
def lcm(*ints):
    out = ints[0]
    for n in ints[1:]:
        out = int(out * n / math.gcd(out, n))
    return out


@cache
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


@cache
def reduce_ratio(*ints):
    g = math.gcd(*ints)
    return tuple(n // g for n in ints)


@cache
def euler_dissonance(ji):
    return sum((n-1) for n in prime_factors(lcm(*ji.ratio))) + 1


@cache
def vogel_dissonance(ji):
    return sum((n-1) for n in prime_factors(lcm(*ji.ratio)) if n != 2) + 1


@cache
def gill_purves_pair(n1, n2):
    n1, n2 = reduce_ratio(n1, n2)
    return (n1 + n2 - 1) / (n1 * n2)


@cache
def gill_purves(ratio):
    pair_dissonances = []
    for i in range(len(ratio) - 1):
        for j in range(i + 1, len(ratio)):
            pair_dissonances.append(gill_purves_pair(ratio[i], ratio[j]))
    return -round(100*sum(pair_dissonances)/len(pair_dissonances), 1)


def gill_purves_dissonance(ji):
    return gill_purves(ji.ratio)


def gill_purves_scale(ji):
    return gill_purves(ji.ratio + (2*ji.ratio[0],))


DISSONANCE_FUNCTIONS = {
    "euler": euler_dissonance,
    "vogel": vogel_dissonance,
    "gp": gill_purves_dissonance,
    "gps": gill_purves_scale,
    "compromise": lambda chord: euler_dissonance(chord) + gill_purves_dissonance(*chord)/10
}
