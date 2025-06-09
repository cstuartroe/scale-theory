import { createContext } from 'react';
import {defaultEDO} from "./types";

const EDOStepsContext = createContext<number>(defaultEDO);

export {EDOStepsContext};
