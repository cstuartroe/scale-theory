import React, {useState} from "react";
import classNames from "classnames";

import {edoStepsParam} from "../common/query_params";
import {randomElement, randrange, range, toggleInclusion} from "../common/utils";
import {allUniqueEDOChords} from "../common/edo";
import {getAudio} from "../common/audioCache";
import {midi440, midiNumbersForChord} from "../common/midi";
import ScaleLine from "../components/ScaleLine";

const inversionOptions = ["No Inversion", "Allow Inversion", "Quiz on Inversions"] as const;

type InversionAllowance = (typeof inversionOptions)[number];

type Answer = {
  shapeName: string,
  inversion?: number,
}

type RoundDefinition = {
  correctAnswer: Answer,
  tonicMidi: number,
  userAnswer?: Answer,
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
  const edoSteps = edoStepsParam.get();
  const edoChords = allUniqueEDOChords(edoSteps);

  const [shapesToQuiz, setShapesToQuiz] = useState<string[]>(defaultChords);
  const [inversionAllowance, setInversionAllowance] = useState<InversionAllowance>("Allow Inversion");

  const [roundsPlayed, setRoundsPlayed] = useState<number>(0);
  const [roundsCorrect, setRoundsCorrect] = useState<number>(0);

  const [round, setRound] = useState<RoundDefinition | null>(null);

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

    setRound({
      correctAnswer: newAnswer,
      tonicMidi: newTonicMidi,
    });
    setDisplayedInversionByChord({});

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
    if (round === null) {
      throw new Error("User answer submitted not during round");
    }

    setRound({...round, userAnswer: ua});
    setRoundsPlayed(roundsPlayed + 1);
    if (answersMatch(ua, round.correctAnswer)) {
      setRoundsCorrect(roundsCorrect + 1);
    }
  }

  function openSettings() {
    setRound(null);
  }

  function topText(): string {
    if (round === null) {
      return "You can update your quiz preferences below. Toggle whether shapes will be quizzed on by clicking them.";
    } else {
      const {userAnswer, correctAnswer} = round;

      if (userAnswer === undefined) {
        return "Good luck!";
      } else if (answersMatch(userAnswer, correctAnswer)) {
        return "Well done! You can listen to what other choices would have sounded like by clicking.";
      } else {
        return "Better luck next time! Take a listen to the correct or other answers by clicking.";
      }
    }
  }

  function topContents() {
    if (round === null) {
      return (
        <div className="xenbutton" onClick={() => newChord()}>
          {roundsPlayed === 0 ? "Start" : "Done"}
        </div>
      );
    } else if (round.userAnswer === undefined) {
      return (
        <div className="xenbutton" onClick={() => getAudio({
          ...audioParams,
          notes: [getNotes(round.correctAnswer, edoSteps, round.tonicMidi)]
        }).play()}>
          Play audio again
        </div>
      );
    } else {
      return (
        <div className="row">
          <div className="col-4">
            <div className="xenbutton" onClick={() => openSettings()}>
              Settings
            </div>
          </div>
          <div className="col-8">
            <div className="xenbutton" onClick={() => newChord()}>
              Next
            </div>
          </div>
        </div>
      );
    }
  }

  function bottomContent() {
    if (round === null) {
      const optionsStyle = {
        display: "flex",
        flexDirection: "column",
        textAlign: "center",
        paddingTop: "10px"
      } as const;

      return (
        <>
          <div
            className="row"
            style={{border: "1px solid black", margin: "2vh 0"}}
          >
            {inversionOptions.map(ia => (
              <div key={ia} className="col-4" style={optionsStyle}>
                <input type="radio" name="inversion" value={ia} checked={ia === inversionAllowance} onChange={(e) => {
                  setInversionAllowance(e.target.value as InversionAllowance);
                }}/>
                <p>{ia}</p>
              </div>
            ))}
          </div>
          <div
            className="row"
            style={{border: "1px solid black", margin: "2vh 0", paddingTop: "1vh"}}
          >
            <div className="col-6">
              <div className="xenbutton" onClick={() => setShapesToQuiz(edoChords.map(c => c.name))}>
                check all
              </div>
            </div>
            <div className="col-6">
              <div className="xenbutton" onClick={() => setShapesToQuiz([])}>
                uncheck all
              </div>
            </div>
            {edoChords.map(chord => {
              return (
                <div key={chord.name} className="col-4 col-md-3 col-lg-2" style={optionsStyle}>
                  <input type="checkbox" checked={shapesToQuiz.includes(chord.name)} onChange={e => {
                    setShapesToQuiz(toggleInclusion(shapesToQuiz, chord.name));
                  }}/>
                  <p>{chord.name}</p>
                </div>
              );
            })}
          </div>
        </>
      );
    } else {
      const {tonicMidi, correctAnswer, userAnswer} = round;

      const unsafeInversionToDisplay = (shapeName: string): number => {
        const {userAnswer, correctAnswer} = round;

        if (userAnswer === undefined) {
          return 0;
        } else {
          switch (inversionAllowance) {
            case "No Inversion":
              return 0;
            case "Allow Inversion":
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

      const inversionToDisplay = (shapeName: string, chordSize: number): number => {
        return unsafeInversionToDisplay(shapeName) % chordSize;
      }

      const guessButton = (shapeName: string, inversion: number | undefined) => {
        return (
          <div
            className="xenbutton"
            onClick={() => submitUserAnswer({shapeName, inversion})}
          >
            {inversion === undefined ? "guess" : `${inversion}inv`}
          </div>
        );
      }

      const playArpegPair = (shapeName: string, inversion: number | undefined) => {
        const isCorrect = shapeName === correctAnswer.shapeName && inversion === correctAnswer.inversion;

        return (
          <>
            <div
              className={classNames("xenbutton", {
                xencorrect: isCorrect,
              })}
              onClick={() => {
                setDisplayedInversionByChord({...displayedInversionByChord, [shapeName]: inversion || 0});
                getAudio({
                  ...audioParams,
                  notes: [getNotes({shapeName, inversion}, edoSteps, tonicMidi || midi440)]
                }).play()
              }}
            >
              {inversion === undefined ? "play" : `${inversion}inv`}
            </div>
            <div
              className="xenbutton"
              onClick={() => {
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

      const buttons = (shapeName: string, inversion: number | undefined) => {
        if (userAnswer === undefined) {
          return guessButton(shapeName, inversion);
        } else {
          return playArpegPair(shapeName, inversion);
        }
      }

      return (
        <div className="row">
          {edoChords.filter(c => shapesToQuiz.includes(c.name)).map(chordShape => {
            return (
              <div
                key={chordShape.name}
                className="col-12 col-md-6 col-lg-4"
                style={{height: "15vh"}}
              >
                <div style={{textAlign: "center"}}>{chordShape.name}</div>

                <ScaleLine
                  chord={{
                    chord: chordShape,
                    inversion: inversionToDisplay(chordShape.name, chordShape.intervals.length + 1)
                  }}
                />

                {(inversionAllowance === "Quiz on Inversions" || (inversionAllowance === "Allow Inversion" && userAnswer !== undefined)) ? (
                  <div style={{display: "flex", flexDirection: "row"}}>
                    {range(chordShape.intervals.length + 1).map(i => (
                      <div key={i} style={{flex: 1}}>
                        {buttons(chordShape.name, i)}
                      </div>
                    ))}
                  </div>
                ) : buttons(chordShape.name, undefined)}
              </div>
            );
          })}
        </div>
      );
    }
  }

  const scoreText = () => {
    if (roundsPlayed === 0) {
      return "0/0";
    } else {
      return `${roundsCorrect}/${roundsPlayed} ${Math.round(roundsCorrect * 100 / roundsPlayed)}%`
    }
  }

  return (
    <div className="row">
      <div className="col-12 col-md-8 offset-md-2">
        <h1>Chords Quiz!</h1>

        <h3>{scoreText()}</h3>

        <div className="row" style={{height: "15vh"}}>
          <p style={{textAlign: "center"}}>{topText()}</p>

          <div className="col-12 col-md-4 offset-md-4">
            {topContents()}
          </div>
        </div>

        {bottomContent()}
      </div>
    </div>
  );
}
