
def degree_approximations(edo_steps):
    step_cents = [round(1200 * i / edo_steps) for i in range(edo_steps)]

    RMAX = 32
    cents_ratios = []

    for denom in range(1, RMAX + 1):
        for num in range(denom, RMAX + 1):
            if math.gcd(num, denom) == 1 and (num / denom <= 2):
                cents_ratios.append(((num, denom), cents(num / denom)))

    cents_ratios.sort(key=lambda x: x[1])

    APPROX_THRESHOLD = 1200/(edo_steps*2)
    approximations = {}

    for deg, cents_deg in enumerate(step_cents):
        approximations[deg] = []
        for (num, denom), cents_ratio in cents_ratios:
            if math.fabs(cents_deg - cents_ratio) <= APPROX_THRESHOLD:
                approximations[deg].append((
                    (num, denom),
                    round(cents_deg - cents_ratio, 1),
                ))

    return approximations


if __name__ == "__main__":
    for deg, approximations in degree_approximations(31).items():
        print(deg)
        for (num, denom), diff in approximations:
            if compromise_dissonance(denom, num) < 40:
                print(f"{num}:{denom}    {euler_dissonance(denom, num)} {gill_purves_dissonance(denom, num)} ({'+' if diff > 0 else ''}{diff})")
        print()