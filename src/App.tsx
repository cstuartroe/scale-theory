import React from "react";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import "./styles/style.scss";

import EDOHome from "./pages/EDOHome";
import ChordQuiz from "./pages/ChordQuiz";
import ScaleExplorer from "./pages/ScaleExplorer";

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
    path: "/scales",
    element: <ScaleExplorer/>,
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
      <RouterProvider router={router}/>
    </div>
  );
}
