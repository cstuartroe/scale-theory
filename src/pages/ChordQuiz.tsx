import React, {useContext, useState} from "react";
import classNames from "classnames";

import {EDOStepsContext} from "../common/contexts";
import {randomElement, randrange, range, toggleInclusion} from "../common/utils";
import {allUniqueEDOChords, NamedEDOChord} from "../common/edo";
import {getAudio} from "../common/audioCache";
import {midi440, midiNumbersForChord} from "../common/midi";
import ScaleLine from "../components/ScaleLine";

const inversionOptions = ["No Inversion", "Allow Inversion", "Quiz on Inversions"] as const;

type InversionAllowance = (typeof inversionOptions)[number];

type Answer = {
  shapeName: string,
  inversion?: number,
}

function getNotes(a: Answer, edoSteps: number, tonicMidi: number) {
  return midiNumbersForChord(
    {
      chord: allUniqueEDOChords(edoSteps).find(c => c.name === a.shapeName)!,
      inversion: a.inversion || 0,
    },
    tonicMidi,
  );
}

const defaultChords = ["major", "minor"];

export default function ChordQuiz() {
  const edoSteps = useContext(EDOStepsContext);
  const edoChords = allUniqueEDOChords(edoSteps);

  const [shapesToQuiz, setShapesToQuiz] = useState<string[]>(defaultChords);
  const [inversionAllowance, setInversionAllowance] = useState<InversionAllowance>("No Inversion");
  const [roundsPlayed, setRoundsPlayed] = useState<number>(0);
  const [roundsCorrect, setRoundsCorrect] = useState<number>(0);
  const [tonicMidi, setTonicMidi] = useState<number | null>(null);
  const [correctAnswer, setCorrectAnswer] = useState<Answer | null>(null);
  const [userAnswer, setUserAnswer] = useState<Answer | null>(null);
  const [displayedInversionByChord, setDisplayedInversionByChord] = useState<{ [key: string]: number }>({});

  const audioParams = {
    timbre: "piano",
    duration: 1000,
    edoSteps,
  } as const;

  function newChord() {
    const shapeName = randomElement(shapesToQuiz);
    const inversion = (inversionAllowance === "No Inversion") ? undefined : randrange(edoChords.find(c => c.name === shapeName)!.intervals.length + 1);

    const newAnswer = {shapeName, inversion};
    const newTonicMidi = 69 - randrange(edoSteps);
    setCorrectAnswer(newAnswer);
    setTonicMidi(newTonicMidi);

    getAudio({...audioParams, notes: [getNotes(newAnswer, edoSteps, newTonicMidi)]}).play();
  }

  function answersMatch(a1: Answer, a2: Answer) {
    if (inversionAllowance === "Quiz on Inversions") {
      return a1.shapeName === a2.shapeName && a1.inversion === a2.inversion;
    } else {
      return a1.shapeName === a2.shapeName;
    }
  }

  function submitUserAnswer(ua: Answer) {
    if (correctAnswer === null) {
      throw new Error("Answer was submitted when there was no correct answer");
    }

    setUserAnswer(ua);
    setRoundsPlayed(roundsPlayed + 1);
    if (answersMatch(ua, correctAnswer)) {
      setRoundsCorrect(roundsCorrect + 1);
    }
  }

  function resetQuiz() {
    setTonicMidi(null);
    setCorrectAnswer(null);
    setUserAnswer(null);
    setDisplayedInversionByChord({});
  }

  let topText: string;
  if (correctAnswer === null) {
    topText = "You can update your quiz preferences below. Toggle whether shapes will be quizzed on by clicking them.";
  } else if (userAnswer === null) {
    topText = "Good luck!";
  } else if (answersMatch(userAnswer, correctAnswer)) {
    topText = "Well done! You can listen to what other choices would have sounded like by clicking.";
  } else {
    topText = "Better luck next time! Take a listen to the correct or other answers by clicking.";
  }

  function unsafeInversionToDisplay(shapeName: string): number {
    let out = 0;

    if (userAnswer === null) {
      return 0;
    } else {
      switch (inversionAllowance) {
        case "No Inversion":
          return 0;
        case "Allow Inversion":
          return correctAnswer!.inversion || 0;
        case "Quiz on Inversions":
          const storedToDisplay = displayedInversionByChord[shapeName];
          if (storedToDisplay === undefined) {
            return correctAnswer!.inversion || 0;
          } else {
            return storedToDisplay;
          }
      }
    }
  }

  function inversionToDisplay(shapeName: string, chordSize: number): number {
    return unsafeInversionToDisplay(shapeName) % chordSize;
  }

  function playArpegPair(shapeName: string, inversion: number | undefined) {
    const isCorrect = shapeName === correctAnswer?.shapeName && inversion === correctAnswer?.inversion;
    const arpegClickable = correctAnswer === null || userAnswer !== null;
    const answerUsingPlayButton = (inversionAllowance === "Quiz on Inversions" && shapesToQuiz.includes(shapeName));
    const playClickable = arpegClickable || answerUsingPlayButton;

    return (
      <>
        <div
          className={classNames("xenbutton", {
            xencorrect: userAnswer !== null && isCorrect,
            xennoclick: !playClickable,
          })}
          onClick={() => {
            if (arpegClickable) {
              setDisplayedInversionByChord({...displayedInversionByChord, [shapeName]: inversion || 0});
              getAudio({
                ...audioParams,
                notes: [getNotes({shapeName, inversion}, edoSteps, tonicMidi || midi440)]
              }).play()
            } else if (answerUsingPlayButton) {
              submitUserAnswer({shapeName, inversion});
            }
          }}
        >
          {inversion === undefined ? "play" : `${inversion}inv`}
        </div>
        <div
          className={classNames("xenbutton", {
            xennoclick: !arpegClickable,
          })}
          onClick={() => {
            if (!arpegClickable) { return; }
            setDisplayedInversionByChord({...displayedInversionByChord, [shapeName]: inversion || 0});
            getAudio({
              ...audioParams,
              duration: 750,
              notes: getNotes({shapeName, inversion}, edoSteps, tonicMidi || midi440).map(n => [n])
            }).play()
          }}
        >
          arpeg
        </div>
      </>
    );
  }

  return (
    <div className="row">
      <div className="col-12 col-md-8 offset-md-2">
        <h1>Chords Quiz</h1>

        <h3>{roundsCorrect}/{roundsPlayed} {Math.round(roundsCorrect * 100 / roundsPlayed)}%</h3>

        <div className="row" style={{height: "15vh"}}>
          <p style={{textAlign: "center"}}>{topText}</p>

          <div className="col-12 col-md-4 offset-md-4">
            {correctAnswer === null ? (
              <div className="xenbutton" onClick={() => newChord()}>
                {roundsPlayed === 0 ? "Start" : "Next"}
              </div>
            ) : userAnswer === null ? (
              <div className="xenbutton" onClick={() => getAudio({
                ...audioParams,
                notes: [getNotes(correctAnswer, edoSteps, tonicMidi!)]
              }).play()}>
                Play again
              </div>
            ) : (
              <div className="xenbutton" onClick={() => resetQuiz()}>
                Done
              </div>
            )}
          </div>
        </div>

        <div className={classNames("row", {xennoclick: correctAnswer !== null})}
             style={{border: "1px solid black", margin: "2vh 0"}}>
          {inversionOptions.map(ia => (
            <div key={ia} className="col-4"
                 style={{display: "flex", flexDirection: "column", textAlign: "center", paddingTop: "10px"}}>
              <input type="radio" name="inversion" value={ia} checked={ia === inversionAllowance} onChange={(e) => {
                if (correctAnswer !== null) {
                  return;
                }
                setInversionAllowance(e.target.value as InversionAllowance);
              }}/>
              <p>{ia}</p>
            </div>
          ))}
        </div>

        <div className="row">
          {edoChords.map(chordShape => {
            let onClickTop: undefined | (() => void);
            if (correctAnswer === null) {
              onClickTop = () => setShapesToQuiz(toggleInclusion(shapesToQuiz, chordShape.name));
            } else if (inversionAllowance === "Quiz on Inversions") {
              // Nothing
            } else if (userAnswer === null && shapesToQuiz.includes(chordShape.name)) {
              onClickTop = () => submitUserAnswer({shapeName: chordShape.name, inversion: undefined});
            }

            return (
              <div
                key={chordShape.name}
                className="col-12 col-md-6 col-lg-4"
                style={{height: "15vh"}}
              >
                <div
                  className={classNames("xenbutton", {
                    xenactive: (correctAnswer === null) && shapesToQuiz.includes(chordShape.name),
                    xennoclick: onClickTop === undefined,
                  })}
                  onClick={onClickTop}
                >
                  {chordShape.name}
                </div>

                <ScaleLine chord={{chord: chordShape, inversion: inversionToDisplay(chordShape.name, chordShape.intervals.length + 1)}}
                           diminished={chordShape.name.includes("diminish")}/>

                {(inversionAllowance === "Quiz on Inversions" || (inversionAllowance === "Allow Inversion" && userAnswer !== null)) ? (
                  <div style={{display: "flex", flexDirection: "row"}}>
                    {range(chordShape.intervals.length + 1).map(i => (
                      <div key={i} style={{flex: 1}}>
                        {playArpegPair(chordShape.name, i)}
                      </div>
                    ))}
                  </div>
                ) : playArpegPair(chordShape.name, undefined)}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
