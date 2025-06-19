import {defaultEDO} from "./types";

type StringConverter<T> = {
  fromString(s: string): T,
  toString(t: T): string,
}

function queryParam<T>(name: string, defaultValue: T, converter: StringConverter<T>) {
  const get = (): T => {
    const urlValue = new URLSearchParams(window.location.search).get(name);
    return (urlValue === null) ? defaultValue : converter.fromString(urlValue);
  }
  const setter = (value: T): ((params: URLSearchParams) => void) => {
    return (params: URLSearchParams) => params.set(name, converter.toString(value));
  }
  const set = (value: T): void => {
    const params = new URLSearchParams(window.location.search);
    params.set(name, converter.toString(value));
    window.location.search = params.toString();
  }
  return {get, set, setter};
}

type Setter = (params: URLSearchParams) => void;

export function setSimultaneously(...setters: Setter[]) {
  const params = new URLSearchParams(window.location.search);
  setters.forEach(setter => {setter(params)})
  window.location.search = params.toString();
}

const stringConverter: StringConverter<string> = {
  fromString: s => s,
  toString: s => s,
}

const intConverter: StringConverter<number> = {
  fromString: s => Number.parseInt(s),
  toString: n => n + "",
}

const edoStepsParam = queryParam("edo", defaultEDO, intConverter);
const sizeParam = queryParam("size", 5, intConverter);
const minJumpParam = queryParam("minjump", 1, intConverter);
const maxJumpParam = queryParam<number | undefined>("maxjump", undefined, intConverter);
const scalePropertiesParam = queryParam("scaleproperties", "count(P5)", stringConverter);

export {edoStepsParam, sizeParam, minJumpParam, maxJumpParam, scalePropertiesParam};
