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
def euler_dissonance(ji):
    return sum((n-1) for n in prime_factors(lcm(*ji.ratio))) + 1


@cache
def vogel_dissonance(ji):
    return sum((n-1) for n in prime_factors(lcm(*ji.ratio)) if n != 2) + 1


@cache
def gill_purves_dissonance(ji):
    n1, n2 = ji.ratio
    return round(100*(1-((n1+n2-1)/(n1*n2))))


DISSONANCE_FUNCTIONS = {
    "euler": euler_dissonance,
    "vogel": vogel_dissonance,
    "gp": gill_purves_dissonance,
    "compromise": lambda chord: euler_dissonance(chord) + gill_purves_dissonance(*chord)/10
}
