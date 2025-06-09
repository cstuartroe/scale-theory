import React, {useContext, useState} from "react";

import {EDOStepsContext} from "../common/contexts";
import {allJustChords, harmonicsInOrder} from "../common/just_intonation";
import EDOIntervalsSVG from "../components/EDOIntervalsSVG";
import MaxHarmonicSlider from "../components/MaxHarmonicSlider";
import {approximateJustChord, EDOChord} from "../common/edo";
import ScaleLoop from "../components/ScaleLoop";
import {midi440} from "../common/midi";

const EDOHome = (_: {}) => {
  const edoSteps = useContext(EDOStepsContext);
  const [maxHarmonicIndex, setMaxHarmonicIndex] = useState(5);

  const chordNames: [EDOChord, string[]][] = [];
  allJustChords.forEach((jChord) => {
    const chord = approximateJustChord(jChord, edoSteps);
    let dupe = false;
    chordNames.forEach(([c, names]) => {
      if (JSON.stringify(c.intervals) === JSON.stringify(chord.intervals)) {
        dupe = true;
        names.push(jChord.name);
      }
    });
    if (!dupe) {
      chordNames.push([chord, [jChord.name]]);
    }
  });

  return (
    <div className="row">
      <div className="col-12 col-md-8 offset-md-2">
        <h1>{edoSteps}EDO</h1>

        <h2>Intervals</h2>

        <div className="row">
          <div className="col-12 col-md-6 col-lg-4 offset-md-3 offset-lg-4">
            <MaxHarmonicSlider maxHarmonicIndex={maxHarmonicIndex} setMaxHarmonicIndex={setMaxHarmonicIndex}/>
          </div>
        </div>

        <div style={{display: "flex"}} className="col-12">
          <EDOIntervalsSVG edoSteps={edoSteps} maxHarmonic={harmonicsInOrder[maxHarmonicIndex]}/>
        </div>

        <h2>Chords</h2>

        <div className="row">
          {chordNames.map(([chord, names]) => {
            return (
              <div key={names[0]} className="col-6 col-md-3" style={{paddingBottom: "10px"}}>
                <ScaleLoop chord={chord} playable="play_both" tonicMidiNumber={midi440}/>
                <p style={{textAlign: "center"}}>{names.join(", ")}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default EDOHome;
