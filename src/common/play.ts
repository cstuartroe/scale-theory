import {EDOChord} from "./edo";
import {EDOScale} from "./edo_scales";


export type PlayType = "chord" | "arpeggio" | "scale" | "double scale";

export function midiNotes(scale: EDOChord | EDOScale, playType: PlayType, tonicMidiNumber: number): number[][] {
  switch (playType) {
    case "chord": return [[0, ...scale.intervals].map(n => n + tonicMidiNumber)];
    case "arpeggio": return [0, ...scale.intervals].map(n => [n + tonicMidiNumber]);
    case "scale": return [0, ...scale.intervals, scale.edoSteps].map(n => [n + tonicMidiNumber]);
    case "double scale": return [0, ...scale.intervals].map(n => [n + tonicMidiNumber - scale.edoSteps]).concat([0, ...scale.intervals, scale.edoSteps].map(n => [n + tonicMidiNumber]));
  }
}

export function scaleAudioParams(scale: EDOChord | EDOScale, playType: PlayType, tonicMidiNumber: number): {edoSteps: number, duration: number, notes: number[][]} {
  const {edoSteps} = scale;
  const duration = playType === "chord" ? 2000 : 750;
  const notes = midiNotes(scale, playType, tonicMidiNumber);

  return {edoSteps, duration, notes};
}