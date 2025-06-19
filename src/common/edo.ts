import {allJustChords, JustChord, JustInterval} from "./just_intonation";

export type EDOChord = {
  edoSteps: number,
  intervals: number[],
}

export type NamedEDOChord = EDOChord & {
  name: string,
}

export type EDOChordWithInversion = {
  chord: EDOChord,
  inversion: number,
}

export function approximateInterval(ivl: JustInterval, edoSteps: number): number {
  return Math.round(edoSteps * Math.log2(ivl.numerator/ivl.denominator));
}

export function approximateJustChord(jChord: JustChord, edoSteps: number): NamedEDOChord {
  return {
    edoSteps,
    intervals: jChord.harmonics.slice(1).map(numerator => approximateInterval({numerator, denominator: jChord.harmonics[0]}, edoSteps)),
    name: jChord.name,
  };
}

// allUniqueEDOChords finds all distinct approximations of just chords in a particular EDO.
// When two just chords have the same approximation, it is assigned the name of the just chord that appears first in allJustChords
export function allUniqueEDOChords(edoSteps: number): NamedEDOChord[]  {
  const out: NamedEDOChord[] = [];

  allJustChords.forEach(jc => {
    const chord = approximateJustChord(jc, edoSteps);
    for (const c of out) {
      if (JSON.stringify(c.intervals) === JSON.stringify(chord.intervals)) {
        return;
      }
    }
    out.push(chord);
  });

  return out;
}

export function EDOCents(edoSteps: number, interval: number): number {
  return 1200*interval/edoSteps;
}

const supportedEDOs = [5, 7, 9, 12, 15, 16, 17, 19, 22, 24, 31] as const;

export type SupportedEdo = (typeof supportedEDOs)[number];

const abbreviated31EDODegrees = ["P1", "^1", "s2", "m2", "N2", "M2", "S2", "s3", "m3", "N3", "M3", "S3", "v4", "P4", "^4", "A4", "d5", "v5", "P5", "^5", "s6", "m6", "N6", "M6", "S6", "s7", "m7", "N7", "M7", "S7", "v8", "P8"];

export function abbreviate(edoSteps: number, interval: number): string {
  if (interval > edoSteps) {
    let out = abbreviate(edoSteps, interval % edoSteps);
    out = out.replace("1", "8").replace("2", "9").replace("3", "10").replace("4", "11").replace("5", "12").replace("6", "13").replace("7", "14");
    return out;
  }

  if (interval === edoSteps/2) {
    return "TT";
  }

  return abbreviated31EDODegrees[Math.round(31*interval/edoSteps)];
}

export function intervalByAbbreviation(edoSteps: number, abbreviation: string): number {
  return Math.round(edoSteps*abbreviated31EDODegrees.indexOf(abbreviation)/31);
}

export {supportedEDOs};
