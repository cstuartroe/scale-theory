const harmonicsInOrder = [2, 3, 5, 7, 9, 11];

export type JustInterval = {
  numerator: number,
  denominator: number,
  name?: string,
}

const allJustIntervals = [
  {
    numerator: 1,
    denominator: 1,
    name: "unison",
  },
  {
    numerator: 12,
    denominator: 11,
    name: "lesser neutral second",
  },
  {
    numerator: 11,
    denominator: 10,
    name: "greater neutral second",
  },
  {
    numerator: 10,
    denominator: 9,
    name: "lesser major second",
  },
  {
    numerator: 9,
    denominator: 8,
    name: "greater major second",
  },
  {
    numerator: 8,
    denominator: 7,
    name: "septimal major second"
  },
  {
    numerator: 7,
    denominator: 6,
    name: "septimal minor third"
  },
  {
    numerator: 6,
    denominator: 5,
    name: "minor third",
  },
  {
    numerator: 11,
    denominator: 9,
    name: "neutral third",
  },
  {
    numerator: 5,
    denominator: 4,
    name: "major third",
  },
  {
    numerator: 14,
    denominator: 11,
    name: "undecimal major third",
  },
  {
    numerator: 9,
    denominator: 7,
    name: "septimal major third"
  },
  {
    numerator: 4,
    denominator: 3,
    name: "perfect fourth",
  },
  {
    numerator: 11,
    denominator: 8,
    name: "lesser undecimal tritone",
  },
  {
    numerator: 7,
    denominator: 5,
    name: "lesser septimal tritone"
  },
  {
    numerator: 10,
    denominator: 7,
    name: "greater septimal tritone"
  },
  {
    numerator: 16,
    denominator: 11,
    name: "greater undecimal tritone",
  },
  {
    numerator: 3,
    denominator: 2,
    name: "perfect fifth",
  },
  {
    numerator: 14,
    denominator: 9,
    name: "septimal minor sixth",
  },
  {
    numerator: 11,
    denominator: 7,
    name: "undecimal minor sixth",
  },
  {
    numerator: 8,
    denominator: 5,
    name: "minor sixth",
  },
  {
    numerator: 18,
    denominator: 11,
    name: "neutral sixth",
  },
  {
    numerator: 5,
    denominator: 3,
    name: "major sixth",
  },
  {
    numerator: 12,
    denominator: 7,
    name: "septimal major sixth",
  },
  {
    numerator: 7,
    denominator: 4,
    name: "septimal minor seventh",
  },
  {
    numerator: 16,
    denominator: 9,
    name: "lesser minor seventh"
  },
  {
    numerator: 9,
    denominator: 5,
    name: "greater minor seventh"
  },
  {
    numerator: 20,
    denominator: 11,
    name: "lesser neutral seventh",
  },
  {
    numerator: 11,
    denominator: 6,
    name: "greater neutral seventh",
  },
  {
    numerator: 2,
    denominator: 1,
    name: "octave",
  },
] as const;

export function jiCents(ivl: JustInterval): number {
  return Math.log2(ivl.numerator/ivl.denominator)*1200;
}

function reduceBy2(n: number): number {
  while (n % 2 === 0) {
    n /= 2;
  }
  return n;
}

export function greatestHarmonic(ivl: JustInterval): number {
  return Math.max(reduceBy2(ivl.numerator), reduceBy2(ivl.denominator));
}

export type JustChord = {
  name: string,
  harmonics: number[],
}

export type JustChordWithInversion = {
  chord: JustChord,
  inversion: number,
}

const allJustChords: JustChord[] = [
  {
    name: "major",
    harmonics: [4, 5, 6],
  },
  {
    name: "minor",
    harmonics: [10, 12, 15],
  },
  {
    name: "major seven",
    harmonics: [8, 10, 12, 15],
  },
  {
    name: "minor seven",
    harmonics: [10, 12, 15, 18],
  },
  {
    name: "dominant seven",
    harmonics: [4, 5, 6, 7],
  },
  {
    name: "sus4",
    harmonics: [6, 8, 9],
  },
  {
    name: "diminished",
    harmonics: [45, 54, 64],
  },
  {
    name: "augmented",
    harmonics: [16, 20, 25],
  },
  {
    name: "neutral",
    harmonics: [18, 22, 27],
  },
  {
    name: "add9",
    harmonics: [4, 5, 6, 9],
  },
];

export function degreeNumber(cents: number, diminished: boolean): number {
  if (cents === 0) {
    return 1;
  } else if (cents <= 250) {
    return 2;
  } else if (cents <= 450) {
    return 3;
  } else if (cents < 600) {
    return 4;
  } else if (cents === 600) {
    return diminished ? 5 : 4;
  } else if (cents < 750) {
    return 5;
  } else if (cents < 950) {
    return 6;
  } else if (cents < 1200) {
    return 7;
  } else if (cents === 1200) {
    return 8;
  } else if (cents <= 1450) {
    return 9;
  } else if (cents <= 1650) {
    return 10;
  } else if (cents <= 1800) {
    return 11;
  } else if (cents < 1950) {
    return 12;
  } else if (cents < 2150) {
    return 13;
  } else {
    return -1;
  }
}

export {harmonicsInOrder, allJustIntervals, allJustChords};
