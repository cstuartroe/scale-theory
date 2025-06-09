import {Timbre} from "./types";

const globalAudioCache = new Map<string, HTMLAudioElement>([]);

export type AudioParams = {
  timbre: Timbre,
  duration: number,
  edoSteps: number,
  notes: number[][],
}

export function getAudio({timbre, duration, edoSteps, notes}: AudioParams): HTMLAudioElement {
  const uri = `/api/notes?timbre=${timbre}&duration=${duration}&edo=${edoSteps}&notes=${JSON.stringify(notes)}`;

  const cachedAudio = globalAudioCache.get(uri)

  if (cachedAudio !== undefined) {
    return cachedAudio;
  } else {
    const audio = new Audio(uri);
    globalAudioCache.set(uri, audio);
    return audio;
  }
}
