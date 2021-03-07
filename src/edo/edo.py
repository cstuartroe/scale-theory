from src.ji import Interval, JI


MAJOR_MINOR_INTERVALS = ["2", "3", "6", "7"]
PERFECT_INTERVALS = ["4", "5"]


class EDOInterval(Interval):
    def __init__(self, steps: int, edo_steps: int):
        self.steps = steps
        self.edo_steps = edo_steps

    def octaves(self):
        return self.steps/self.edo_steps

    def name(self):
        return EDO.get(self.edo_steps).names[self.steps]

    def __repr__(self):
        return f"EDOInterval({self.steps}, {self.edo_steps})"


class EDO:
    EDOS = {}

    def __init__(self, steps: int):
        self.steps = steps
        self.names = self.gen_names()

    def __repr__(self):
        return f"EDO({self.steps})"

    def approximate(self, ivl: Interval):
        return EDOInterval(round(ivl.octaves() * self.steps), self.steps)

    def augment_ratio(self):
        for i in range(self.steps // 7 + 1):
            if (self.steps - i*7) % 5 == 0:
                m2 = i
                aug = (self.steps - i*7)//5
                return m2/aug

    def gen_names(self) -> [str]:
        out = [[] for _ in range(self.steps + 1)]
        out[0].append("unison")
        out[-1].append("p8")

        named_intervals = {}

        for ivl in MAJOR_MINOR_INTERVALS:
            for mm in ["m", "maj"]:
                named_intervals[mm + ivl] = self.approximate(JI.by_name(mm + ivl)).steps

        for ivl in PERFECT_INTERVALS:
            named_intervals["p" + ivl] = self.approximate(JI.by_name("p" + ivl)).steps

        aug = named_intervals["maj3"] - named_intervals["m3"]
        m2 = named_intervals["m2"]

        try:
            assert named_intervals["maj2"] - m2 == aug
            assert named_intervals["maj7"] - named_intervals["m7"] == aug
            assert named_intervals["p4"] - named_intervals["maj3"] == m2
        except AssertionError:
            print(named_intervals)
            raise ValueError

        for name, steps in named_intervals.items():
            out[steps].append(name)

        def any_core_names(names):
            for name in names:
                if name.startswith("p") or name.startswith("m") or name == "unison":
                    return True

            return False

        for ivl in MAJOR_MINOR_INTERVALS:
            m_steps = named_intervals["m" + ivl]
            maj_steps = named_intervals["maj" + ivl]
            if not any_core_names(out[m_steps - 1]):
                out[m_steps - 1].append("sub" + ivl)
            if not any_core_names(out[maj_steps + 1]):
                out[maj_steps + 1].append("sup" + ivl)
            if aug == 2:
                out[m_steps + 1].append("n" + ivl)

        for ivl in PERFECT_INTERVALS:
            p_steps = named_intervals["p" + ivl]
            if not any_core_names(out[p_steps - aug]):
                out[p_steps - aug].append("dim" + ivl)
            if not any_core_names(out[p_steps + aug]):
                out[p_steps + aug].append("aug" + ivl)
            if aug == 2:
                out[p_steps - 1].append("down" + ivl)
                out[p_steps + 1].append("up" + ivl)

        if len(out[1]) == 0:
            out[1].append("step")
        if len(out[-2]) == 0:
            out[-2].append("down8")

        if any(len(names) == 0 for names in out):
            print(out)
            raise ValueError("Some step(s) lack names")

        return ["/".join(names) for names in out]

    @staticmethod
    def get(edo_steps):
        if edo_steps not in EDO.EDOS:
            EDO.EDOS[edo_steps] = EDO(edo_steps)

        return EDO.EDOS[edo_steps]
