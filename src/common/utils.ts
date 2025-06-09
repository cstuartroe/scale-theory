export function range(n: number) {
  return Array.from(Array(n).keys());
}

export function round(n: number, digits: number) {
  const pow10 = Math.pow(10, digits);
  return Math.round(n * pow10) / pow10;
}

export function toggleInclusion<T>(l: T[], e: T): T[] {
  if (l.includes(e)) {
    return l.filter(el => el !== e);
  } else {
    return [...l, e];
  }
}

export function randrange(n: number) {
  return Math.floor(Math.random()*n);
}

export function randomElement<T>(l: T[]): T {
  return l[randrange(l.length)];
}
