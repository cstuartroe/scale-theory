import {range, round} from "../common/utils";
import React from "react";
import {allJustIntervals, greatestHarmonic, jiCents, JustInterval} from "../common/just_intonation";
import {abbreviate} from "../common/edo";

const width = 550;
const lineStart = 95;
const lineEnd = 250;
const lineWidth = (lineEnd - lineStart) / 2 + 10;
const height = 1200;
const padding = 30;
const textOffsetX = 5;
const degreeWidth = 30;
const textOffsetY = 5;
const chartFont = "regular 10px sans-serif";

const jiColors: { [key: number]: string } = {
  1: "#3333ff",
  3: "#ff3333",
  5: "#33ff33",
  7: "#ddbb33",
  9: "#ff33ff",
  11: "#777777",
};

function JIColor(ivl: JustInterval): string {
  return jiColors[greatestHarmonic(ivl)];
}

type Props = {
  edoSteps: number,
  maxHarmonic: number,
};

export default function EDOIntervalsSVG({edoSteps, maxHarmonic}: Props) {
  return (
    <svg width={width} height={height + 2 * padding} style={{margin: "auto"}}>
      <rect width={width} height={height + 2 * padding} fill="none" stroke={jiColors[11]}/>

      {range(edoSteps + 1).map((_, i) => {
        const y = i * height / edoSteps + padding;
        return <React.Fragment key={i}>
          <line x1={lineStart} x2={lineStart + lineWidth} y1={y} y2={y} stroke="black" strokeWidth="2"/>
          <text x={textOffsetX} y={y + textOffsetY} style={{fill: "black", font: chartFont}}>
            {abbreviate(edoSteps, i)}
          </text>
          <text x={textOffsetX + degreeWidth} y={y + textOffsetY} style={{fill: "black", font: chartFont}}>
            {round(i / edoSteps * 1200, 1)}¢
          </text>
        </React.Fragment>
      })}

      {allJustIntervals.map((ivl, _) => {
        if (greatestHarmonic(ivl) > maxHarmonic) {
          return null;
        }

        const y = Math.log2(ivl.numerator / ivl.denominator) * height + padding;
        return <React.Fragment key={ivl.name}>
          <line x1={lineEnd - lineWidth} x2={lineEnd} y1={y} y2={y} stroke={JIColor(ivl)} strokeWidth="2"/>
          <text x={lineEnd + textOffsetX} y={y + textOffsetY} style={{fill: JIColor(ivl), font: chartFont}}>
            {round(jiCents(ivl), 1)}¢
          </text>
          <text x={lineEnd + textOffsetX + 65} y={y + textOffsetY} style={{fill: JIColor(ivl), font: chartFont}}>
            {ivl.name} {ivl.numerator}/{ivl.denominator}
          </text>
        </React.Fragment>;
      })}
    </svg>
  );
}