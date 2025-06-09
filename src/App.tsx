import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import React, {useContext} from "react";

import "./styles/style.scss";

import {defaultEDO} from "./common/types";
import {EDOStepsContext} from "./common/contexts";
import EDOHome from "./pages/EDOHome";
import ChordQuiz from "./pages/ChordQuiz";
import {supportedEDOs} from "./common/edo";

const EDORoot = (props: React.PropsWithChildren<{}>) => {
  const edoStepsString = (new URLSearchParams(window.location.search)).get("edo");

  let edoSteps = defaultEDO;
  if (edoStepsString !== null) {
    edoSteps = Number.parseInt(edoStepsString);

    if (Number.isNaN(edoSteps) || edoSteps + "" !== edoStepsString) {
      throw new Error("edoSteps not parseable as a number");
    } else if (!supportedEDOs.includes(edoSteps)) {
      return <p>Sorry, this EDO is not supported at present.</p>
    }
  }

  return (
    <EDOStepsContext.Provider value={edoSteps}>
      {props.children}
    </EDOStepsContext.Provider>
  );
};

const router = createBrowserRouter([
  {
    index: true,
    element: <div>
      Hello world!
      <img src="/static/img/favicon.png" alt="A loop with the notes of the harmonic minor scale wearing headphones"/>
    </div>,
  },
  {
    path: "/edo",
    element: <EDOHome/>,
  },
  {
    path: "/quiz",
    children: [
      {
        path: "chords",
        element: <ChordQuiz/>
      },
    ],
  },
]);

export default function App(_: {}) {
  return (
    <div className="container-fluid">
      <EDORoot>
        <RouterProvider router={router}/>
      </EDORoot>
    </div>
  );
}
