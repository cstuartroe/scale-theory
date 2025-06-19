import {EDOScale} from "../../common/edo_scales";

export function getAllScalesInWorker(
  edoSteps: number,
  size: number,
  minJump: number,
  maxJump: number
): Promise<EDOScale[]> {
  return new Promise<EDOScale[]>((resolve, reject) => {
    const worker = new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' });

    worker.postMessage({ edoSteps, size, minJump, maxJump });

    worker.onmessage = (event: {data: EDOScale[]}) => {
      resolve(event.data);
      worker.terminate();
    };

    worker.onerror = (err) => {
      console.log(err);
      reject(err);
      worker.terminate();
    };
  });
}
