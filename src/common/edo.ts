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

export type EDOScale = EDOChord;

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

const supportedEDOs = [5, 7, 9, 12, 15, 16, 17, 19, 22, 24, 31];

export {supportedEDOs};
