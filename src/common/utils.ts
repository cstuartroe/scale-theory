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

export function choose(m: number, n: number): number {
  let out = 1;

  const x = Math.max(n, m-n);
  const y = Math.min(n, m-n);
  for (let i = x + 1; i <= m; i++) {
    out *= i;
  }
  for (let i = 2; i <= y; i++) {
    out /= i;
  }

  return out;
}
