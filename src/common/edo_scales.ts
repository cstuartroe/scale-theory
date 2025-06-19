import {EDOChord} from "./edo";

export type EDOScale = EDOChord;

const sortedASCIIChars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

function sortableString(intervals: number[]): string {
  return intervals.map(n => sortedASCIIChars[n]).join("");
}

function sortedIntervals(intervals: number[][]): number[][] {
  const sortableIntervals: [string, number[]][] = intervals.map(ivl => [sortableString(ivl), ivl]);
  sortableIntervals.sort();
  return sortableIntervals.map(p => p[1]);
}

export function modes(scale: EDOScale): EDOScale[] {
  const {edoSteps, intervals} = scale;

  const rotations = [intervals];
  for (let i = 0; i < intervals.length; i++) {
    const shift = rotations[i][0];
    rotations.push([...rotations[i].slice(1).map(steps => steps - shift), edoSteps - shift]);
  }

  return rotations.map(intervals => ({edoSteps, intervals}));
}

export function citationForm(scale: EDOScale): EDOScale {
  const {edoSteps, intervals} = scale;
  return {
    edoSteps,
    intervals: sortedIntervals(modes(scale).map(m => m.intervals))[0],
  };
}

function findScalesWithLargestJump(base: number, stepsRemaining: number, sizeRemaining: number, minJump: number, maxJump: number): number[][] {
  if (sizeRemaining === 0) {
    return [[]];
  }

  const out: number[][] = [];

  for (let firstStep = minJump; firstStep <= Math.min(maxJump, stepsRemaining - (sizeRemaining * minJump)); firstStep++) {
    findScalesWithLargestJump(base + firstStep, stepsRemaining - firstStep, sizeRemaining - 1, minJump, maxJump).forEach(ivls => {
      out.push([base + firstStep, ...ivls]);
    })
  }

  return out;
}

const scalesCache = new Map<string, number[][]>();

function findScalesWithLargestJumpCached(base: number, stepsRemaining: number, sizeRemaining: number, minJump: number, maxJump: number): number[][] {
  const hashString = sortableString([base, stepsRemaining, sizeRemaining, minJump, maxJump]);
  if (scalesCache.has(hashString)) {
    return scalesCache.get(hashString)!;
  } else {
    const out = findScalesWithLargestJump(base, stepsRemaining, sizeRemaining, minJump, maxJump);
    scalesCache.set(hashString, out);
    return out;
  }
}

function findScalesLargestJumpFirst(edoSteps: number, size: number, minJump: number, maxJump: number): number[][] {
  const out: number[][] = [];

  for (let largestJump = Math.ceil(edoSteps/size); largestJump <= Math.min(edoSteps - size + 1, maxJump); largestJump++) {
    findScalesWithLargestJumpCached(largestJump, edoSteps - largestJump, size - 2, minJump, largestJump).forEach(ivls => {
      out.push([largestJump, ...ivls]);
    });
  }

  return out;
}

export function getAllScales(edoSteps: number, size: number, minJump: number, maxJump?: number): EDOScale[] {
  const seenSet = new Set<string>([]);
  const out: number[][] = [];
  if (maxJump === undefined) {
    maxJump = edoSteps;
  }

  findScalesLargestJumpFirst(edoSteps, size, minJump, maxJump).forEach(intervals => {
    const citForm = citationForm({edoSteps, intervals});
    const s = JSON.stringify(citForm.intervals);
    if (!seenSet.has(s)) {
      seenSet.add(s);
      out.push(citForm.intervals);
    }
  });

  return sortedIntervals(out).map(intervals => ({edoSteps, intervals}));
}
