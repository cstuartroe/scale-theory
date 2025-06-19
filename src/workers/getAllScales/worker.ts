import {getAllScales} from "../../common/edo_scales";

export type GetAllScalesArgs = {
  edoSteps: number,
  size: number,
  minJump: number,
  maxJump: number,
}

self.onmessage = (event: {data: GetAllScalesArgs}) => {
  const { edoSteps, size, minJump, maxJump } = event.data;

  const scales = getAllScales(edoSteps, size, minJump, maxJump);

  (self as DedicatedWorkerGlobalScope).postMessage(scales);
};
