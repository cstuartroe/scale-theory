import {EDOScale, modes} from "./edo_scales";
import {abbreviate, intervalByAbbreviation} from "./edo";

export type ScaleProperty = {
  getValue: (scale: EDOScale) => number | string,
  name: string,
};

export function countIntervalOccurrences(scale: EDOScale, interval: number): number {
  const scaleModes = modes(scale);
  let out = 0;
  scaleModes.forEach(mode => {
    if (mode.intervals.includes(interval)) {
      out++;
    }
  });
  return out;
}

export function parseScaleProperties(edoSteps: number, propertiesString: string): ScaleProperty[] {
  const parts = propertiesString.split(",");
  const out: ScaleProperty[] = [];

  if (propertiesString === "") {
    return [];
  }

  parts.forEach(part => {
    const countMatch = /count\((.+)\)/.exec(part);
    if (countMatch !== null) {
      const steps = intervalByAbbreviation(edoSteps, countMatch[1]);
      const property: ScaleProperty = {
        getValue: (scale: EDOScale) => countIntervalOccurrences(scale, steps),
        name: `count(${abbreviate(edoSteps, steps)})`,
    };
      out.push(property);
      return;
    }

    throw new Error(`Unknown property: ${JSON.stringify(part)}`);
  });

  return out;
}

export function sortByScaleProperties(scales: EDOScale[], properties: ScaleProperty[]): [[string, number | string][], EDOScale][] {
  const propertiesAndScales: [[string, number | string][], EDOScale][] = scales.map(scale => [properties.map(p => [p.name, p.getValue(scale)]), scale]);
  propertiesAndScales.sort();
  return propertiesAndScales.reverse();
}
