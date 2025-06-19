import React, {useMemo, useState} from "react";

import {
  edoStepsParam,
  maxJumpParam,
  minJumpParam,
  scalePropertiesParam,
  setSimultaneously,
  sizeParam
} from "../common/query_params";
import ScaleLoop from "../components/ScaleLoop";
import {EDOChord} from "../common/edo";
import {citationForm, getAllScales, modes} from "../common/edo_scales";
import {getAllScalesInWorker} from "../workers/getAllScales/wrapper";
import {choose} from "../common/utils";
import ScaleLine from "../components/ScaleLine";
import {midi440} from "../common/midi";
import {automaticScaleName, namedScales} from "../common/named_scales";
import {getAudio} from "../common/audioCache";
import {scaleAudioParams} from "../common/play";
import {parseScaleProperties, sortByScaleProperties} from "../common/scale_properties";

const pageSize = 20;

function getPropertyRanges(propertyValues: [string, number | string][][]): Map<string, (number | string)[]> {
  const seenValues = new Map<string, Set<number | string>>();

  propertyValues.forEach(properties => {
    properties.forEach(([propertyName, value]) => {
      const set = seenValues.get(propertyName);
      if (set === undefined) {
        seenValues.set(propertyName, new Set([value]));
      } else {
        set.add(value);
      }
    });
  })

  return new Map<string, (number | string)[]>(seenValues.entries().map(([propertyName, seenValues]): [string, (number | string)[]] => {
    const l: (number | string)[] = Array.from(seenValues.keys());
    l.sort();
    return [propertyName, l];
  }));
}

function spectrumColor(valuesRange: (number | string)[], value: (number | string)) {
  const i = valuesRange.indexOf(value);
  if (i === -1) {
    throw new Error(`Value not found: ${value}`);
  }

  const relativeValue = i/(valuesRange.length-1);

  const r = 256 - Math.round(128*relativeValue);
  const g = 128 + Math.round(128*relativeValue);
  const b = 128;
  return `rgb(${r}, ${g}, ${b})`;
}

function ScaleDisplay({scales}: {scales: [[string, number | string][], EDOChord][] | null}) {
  const [pagesShown, setPagesShown] = useState(1);

  if (scales === null) {
    return (
      <div style={{display: "flex", flexDirection: "row"}}>
        <img src="/static/img/loading.gif" alt="Loading..." style={{margin: "auto"}}/>
      </div>
    );
  } else {
    const propertyRanges = getPropertyRanges(scales.map(p => p[0]));

    return (
      <>
        <p>{scales.length} distinct scales</p>

        {scales.slice(0, pageSize*pagesShown).map(([scores, scale]) => {
          const namedScale = namedScales.find(s => citationForm(s.scale).intervals + "" === scale.intervals + "");
          if (namedScale !== undefined) {
            scale = namedScale.scale;
          }

          return (
            <div className="row" key={scale.intervals + ""} style={{border: "1px solid black", margin: "1vh 0"}}>
              <div className="col-12">
                <h2>{namedScale ? namedScale.name : automaticScaleName(scale)}</h2>
              </div>
              <div className="col-4">
                <ScaleLoop chord={scale} playTypes={["scale", "double scale"]} tonicMidiNumber={midi440}/>
              </div>
              <div className="col-8">
                {modes(scale).map((mode, i) => (
                  <div key={mode.intervals + ""} className="row" style={{margin: "0 0 .5vh"}}>
                    <div className="col-6 col-lg-3">
                      <p style={{fontWeight: "bold", textAlign: "center", margin: "0"}}>
                        {namedScale?.modeNames ? namedScale?.modeNames[i] : automaticScaleName(mode)}
                      </p>
                    </div>
                    <div className="col-6 col-lg-2">
                      <div
                        className="xenbutton"
                        style={{padding: "0 1vw"}}
                        onClick={() => getAudio({timbre: "piano", ...scaleAudioParams(mode, "scale", midi440)}).play()}
                      >
                        play
                      </div>
                    </div>
                    <div className="col-12 col-lg-7">
                      <ScaleLine chord={{chord: mode, inversion: 0}}/>
                    </div>
                  </div>
                ))}
              </div>
              <div className="col-12">
                <div className="row">
                  {scores.map(([propertyName, value]) => {

                    return (
                      <div className="col-3 col-md-2" style={{backgroundColor: spectrumColor(propertyRanges.get(propertyName)!, value)}}>
                        {propertyName}: {value}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          );
        })}

        {(pagesShown < Math.ceil(scales.length/pageSize)) && <div className="xenbutton" onClick={() => setPagesShown(pagesShown + 1)}>
          Show more
        </div>}
      </>
    );
  }
}

export default function ScaleExplorer() {
  const edoSteps = edoStepsParam.get();
  const qSize = sizeParam.get();
  const qMinJump = minJumpParam.get();
  const qMaxJump = maxJumpParam.get() || edoSteps - qSize + 1;
  const qScaleProperties = scalePropertiesParam.get();

  const [size, setSize] = useState<number>(qSize);
  const [minJump, setMinJump] = useState<number>(qMinJump);
  const [maxJump, setMaxJump] = useState<number>(qMaxJump);

  const [scales, setScales] = useState<[[string, number | string][], EDOChord][] | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const parsedScaleProperties = parseScaleProperties(edoSteps, qScaleProperties);

  const loadScales = () => {
    setErrorMessage(null);

    // Beyond a certain size, want to do this async
    if (choose(edoSteps, size) < 100000) {
      setScales(sortByScaleProperties(getAllScales(edoSteps, qSize, qMinJump, qMaxJump), parsedScaleProperties));
    } else {
      setScales(null);
      getAllScalesInWorker(edoSteps, qSize, qMinJump, qMaxJump)
        .then(scales => {
          setScales(sortByScaleProperties(scales, parsedScaleProperties));
        })
        .catch(_ => {
          setErrorMessage("Computation was not able to complete.");
          setScales([]);
        });
    }
  }

  useMemo(loadScales, [edoSteps, qSize, qMinJump, qMaxJump, qScaleProperties]);

  const updateScales = () => {
    setSimultaneously(sizeParam.setter(size), minJumpParam.setter(minJump), maxJumpParam.setter(maxJump));
  }

  return (
    <div className="row">
      <div className="col-12 col-md-6 offset-md-3 col-lg-4 offset-lg-4" style={{display: "flex", flexDirection: "column"}}>
        <p style={{color: "red"}}>{errorMessage}</p>
        <div>Size: {size}</div>
        <input
          type="range"
          min="3"
          max={edoSteps}
          value={size}
          onChange={e => {
            const newSize = Number.parseInt(e.target.value);
            setSize(newSize);
            setMinJump(Math.min(minJump, Math.floor(edoSteps/newSize)));
            setMaxJump(Math.min(Math.max(maxJump, Math.ceil(edoSteps/newSize)), edoSteps - newSize + 1));
          }}
        />
        <div>Minimum jump: {minJump}</div>
        <input
          type="range"
          min="1"
          max={Math.floor(edoSteps/size)}
          value={minJump}
          onChange={e => setMinJump(Number.parseInt(e.target.value))}
        />
        <div>Maximum jump: {maxJump}</div>
        <input
          type="range"
          min={Math.ceil(edoSteps/size)}
          max={edoSteps - size + 1}
          value={maxJump}
          onChange={e => setMaxJump(Number.parseInt(e.target.value))}
        />
        <div className="xenbutton" onClick={updateScales}>Regenerate scales</div>
      </div>
      <div className="col-12 col-md-8 offset-md-2">
        <ScaleDisplay scales={scales}/>
      </div>
    </div>
  );
}
