import React from "react";

import {range} from "../common/utils";
import {useFill, skipFill} from "../common/colors";
import {degreeNumber} from "../common/just_intonation";
import {EDOChordWithInversion, EDOCents} from "../common/edo";

const height = 25;

type Props = {
  chord: EDOChordWithInversion,
  diminished?: boolean,
}

export default function ScaleLine({chord, diminished}: Props) {
  const allIntervals = [0, ...chord.chord.intervals];
  const bassNote = allIntervals[chord.inversion];
  const {edoSteps} = chord.chord;
  let stepsWithDegreeNumbers: [number, number][] = allIntervals.map((steps, i) => (
    [steps - bassNote + (i < chord.inversion ? edoSteps : 0), degreeNumber(EDOCents(edoSteps, steps), diminished || false)]
  ));

  if (stepsWithDegreeNumbers[0][0] < 0) {
    const shift = -stepsWithDegreeNumbers[0][0];
    stepsWithDegreeNumbers = stepsWithDegreeNumbers.map(([steps, degreeNumber]) => [steps + shift, degreeNumber]);
  }

  const numOctaves = Math.ceil(Math.max(...stepsWithDegreeNumbers.map(p => p[0])) / edoSteps);

  return (
    <div style={{height, width: "100%", display: "flex", flexDirection: "row"}}>
      {range(edoSteps*numOctaves).map(i => {
        const stepAndDegreeNumber = stepsWithDegreeNumbers.find(p => p[0] === i);
        const used = stepAndDegreeNumber !== undefined;
        const degreeNumber = stepAndDegreeNumber === undefined ? "" : stepAndDegreeNumber[1];

        return (
          <div key={i} style={{
            flex: 1,
            backgroundColor: i === 0 || used ? useFill : skipFill,
            border: "1px solid black",
            textAlign: "center",
            color: "white",
          }}>
            {degreeNumber}
          </div>
        );
      })}
    </div>
  );
}
