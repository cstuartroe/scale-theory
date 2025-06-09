import {EDOChordWithInversion} from "./edo";

const midi440 = 69; // Nice

export function midiNumbersForChord(chord: EDOChordWithInversion, tonicMidi: number): number[] {
  const out = [0, ...chord.chord.intervals].map((steps, i) => tonicMidi + steps + ((chord.inversion > 0 && chord.inversion > i) ? chord.chord.edoSteps : 0));
  out.sort();
  return out;
}

export {midi440};
