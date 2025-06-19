import React from "react";

import {range} from "../common/utils";
import {skipFill, useFill} from "../common/colors";
import {EDOChord} from "../common/edo";
import {AudioParams, getAudio} from "../common/audioCache";
import {PlayType, scaleAudioParams} from "../common/play";


const imageSize = 120;
const center = imageSize / 2;
const radius = 55;
const innerRadius = 40;

function ScaleLoopSVG({chord}: { chord: EDOChord }) {
  const sliceRadians = 2 * Math.PI / chord.edoSteps;

  const moddedIntervals = chord.intervals.map(ivl => ivl % chord.edoSteps);

  return (
    <svg width={imageSize} height={imageSize} style={{margin: "auto"}}>
      {range(chord.edoSteps).map(i => {
        const arcCenterRadians = sliceRadians * i - Math.PI / 2;
        const arcStartRadians = arcCenterRadians - sliceRadians / 2;
        const arcEndRadians = arcCenterRadians + sliceRadians / 2;

        const d = `
        M ${center + radius * Math.cos(arcStartRadians)} ${center + radius * Math.sin(arcStartRadians)}
        A ${radius} ${radius} 0 0 1 ${center + radius * Math.cos(arcEndRadians)} ${center + radius * Math.sin(arcEndRadians)}
        L ${center + innerRadius * Math.cos(arcEndRadians)} ${center + innerRadius * Math.sin(arcEndRadians)}
        A ${innerRadius} ${innerRadius} 0 0 0 ${center + innerRadius * Math.cos(arcStartRadians)} ${center + innerRadius * Math.sin(arcStartRadians)}
        Z
        `

        return <path key={i} d={d} stroke="black" strokeWidth="1"
                     fill={[0, ...moddedIntervals].includes(i) ? useFill : skipFill}/>
      })}
    </svg>
  );
}

type Props = {
  chord: EDOChord,
  playTypes: PlayType[],
  tonicMidiNumber: number,
}

const timbre = "piano";

const playButtonText: {[key in PlayType]: string} = {
  chord: "play",
  arpeggio: "arpeg",
  scale: "play",
  "double scale": "2x",
}

export default function ScaleLoop({chord, playTypes, tonicMidiNumber}: Props) {
  const chordMidiNumbers = [0, ...chord.intervals].map(n => n + tonicMidiNumber);
  const edoSteps = chord.edoSteps;

  const buttonStyle = {width: "50px", margin: "auto"} as const;

  return (
    <div style={{width: "100%", display: "flex", position: "relative"}}>
      <ScaleLoopSVG chord={chord}/>
      <div style={{
        position: "absolute",
        width: "100%",
        paddingTop: `${55 - 10*playTypes.length}px`,
        display: "flex",
        flexDirection: "column"
      }}>
        {playTypes.map(pt => (
          <div key={pt} className="xenbutton" style={buttonStyle} onClick={() => {
            getAudio({timbre, ...scaleAudioParams(chord, pt, tonicMidiNumber)}).play()
          }}>
            {playButtonText[pt]}
          </div>
        ))}
      </div>
    </div>
  );
}
