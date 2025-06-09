import React from "react";

import {range} from "../common/utils";
import {skipFill, useFill} from "../common/colors";
import {EDOChord} from "../common/edo";
import {AudioParams, getAudio} from "../common/audioCache";


const imageSize = 120;
const center = imageSize / 2;
const radius = 55;
const innerRadius = 40;

function ScaleLoopSVG({chord}: { chord: EDOChord }) {
  const sliceRadians = 2 * Math.PI / chord.edoSteps;

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
                     fill={[0, ...chord.intervals].includes(i) ? useFill : skipFill}/>
      })}
    </svg>
  );
}

type Props = {
  chord: EDOChord,
  playable: "no_play" | "arpeg_only" | "play_both",
  tonicMidiNumber: number,
}

const timbre = "piano";

export default function ScaleLoop({chord, playable, tonicMidiNumber}: Props) {
  const chordMidiNumbers = [0, ...chord.intervals].map(n => n + tonicMidiNumber);
  const edoSteps = chord.edoSteps;

  const chordAudioParams: AudioParams = {timbre, edoSteps, duration: 2000, notes: [chordMidiNumbers]};
  const arpeggioAudioParams: AudioParams = {timbre, edoSteps, duration: 750, notes: chordMidiNumbers.map(n => [n])};

  const buttonStyle = {width: "50px", margin: "auto"} as const;

  return (
    <div style={{width: "100%", display: "flex", position: "relative"}}>
      <ScaleLoopSVG chord={chord}/>
      {playable !== "no_play" && (
        <div style={{
          position: "absolute",
          width: "100%",
          paddingTop: `${playable === "play_both" ? 35 : 45}px`,
          display: "flex",
          flexDirection: "column"
        }}>
          {playable == "play_both" && <>
            <div className="xenbutton" style={buttonStyle} onClick={() => {
              getAudio(chordAudioParams).play()
            }}>
              play
            </div>
          </>}
          <div className="xenbutton" style={buttonStyle} onClick={() => {
            getAudio(arpeggioAudioParams).play()
          }}>
            arpeg
          </div>
        </div>
      )}
    </div>
  );
}
