import React from "react";

import {harmonicsInOrder} from "../common/just_intonation";

type Props = {
  maxHarmonicIndex: number,
  setMaxHarmonicIndex: (index: number) => void,
}

export default function MaxHarmonicSlider({maxHarmonicIndex, setMaxHarmonicIndex}: Props) {
  return <>
        <input
          type="range"
          min="0"
          max={harmonicsInOrder.length - 1}
          value={maxHarmonicIndex}
          onChange={e => setMaxHarmonicIndex(Number.parseInt(e.target.value))}
          style={{width: "100%"}}
        />
        <p style={{textAlign: "center"}}>Max harmonic: {harmonicsInOrder[maxHarmonicIndex]}</p>
  </>;
}