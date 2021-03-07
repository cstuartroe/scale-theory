import math


def lcm(*ints):
    out = ints[0]
    for n in ints[1:]:
        out = int(out * n / math.gcd(out, n))
    return out


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


def euler_dissonance(*ints):
    return sum((n-1) for n in prime_factors(lcm(*ints))) + 1


def vogel_dissonance(*ints):
    return sum((n-1) for n in prime_factors(lcm(*ints)) if n != 2) + 1


def gill_purves_dissonance(n1, n2):
    return round(100*(1-((n1+n2-1)/(n1*n2))))
