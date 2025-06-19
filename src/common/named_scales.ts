import {citationForm, EDOScale} from "./edo_scales";
import {supportedEDOs} from "./edo";

// "Phonology":
// Consonants: 1:p 2:t 3:m 4:k 5:n 6:l 7:s
// Vowels: sub/dim:u min/down:o neut/perf:a maj/up:e sup/aug:i
const named31EDOdegrees = ["pa", "pe", "tu", "to", "ta", "te", "ti", "mu", "mo", "ma", "me", "mi", "ko", "ka", "ke", "ki", "nu", "no", "na", "ne", "lu", "lo", "la", "le", "li", "su", "so", "sa", "se", "si", "po"]

function approximateAs31Steps(edoSteps: number, steps: number) {
  return Math.round(31*steps/edoSteps);
}

export function automaticScaleName(scale: EDOScale): string {
  const degreeNames = scale.intervals.map(ivl => named31EDOdegrees[approximateAs31Steps(scale.edoSteps, ivl)]);
  let out = "";
  for (let i = 0; i < degreeNames.length; i++) {
    out += degreeNames[i];
    if (degreeNames.length > 4 && i % 3 == 2) {
      out += " ";
    }
  }
  return out;
}

export type NamedScale = {
  scale: EDOScale, // must be citation form
  name: string,
  modeNames?: string[],
}

const namedScales: NamedScale[] = [
  {
    scale: {
      edoSteps: 12,
      intervals: [2,4,7,9],
    },
    name: "pentatonic",
    modeNames: ["major", "suspended", "blues minor", "blues major", "minor"],
  },
  {
    scale: {
      edoSteps: 12,
      intervals: [2,4,5,7,9,11],
    },
    name: "diatonic",
    modeNames: ["ionian", "dorian", "phrygian", "lydian", "mixolydian", "aeolian", "locrian"],
  },
  {
    scale: {
      edoSteps: 12,
      intervals: [2,3,5,7,8,11],
    },
    name: "harmonic minor",
    modeNames: ["harmonic minor", "locrian M6", "augmented major", "dorian #4", "phrygian dominant", "lydian #9", "super locrian"]
  },
  {
    scale: {
      edoSteps: 12,
      intervals: [2,3,5,7,9,11],
    },
    name: "melodic minor",
  },
  {
    scale: {
      edoSteps: 12,
      intervals: [1,4,5,7,8,11],
    },
    name: "double harmonic",
  },
];

const scalesByEdoAndName = new Map<number, Map<string, NamedScale>>(
  supportedEDOs.map(edoSteps => [edoSteps, new Map<string, NamedScale>(
    namedScales.filter(scale => scale.scale.edoSteps === edoSteps).map(scale => [scale.name, scale])
  )])
);

export {namedScales, scalesByEdoAndName};
