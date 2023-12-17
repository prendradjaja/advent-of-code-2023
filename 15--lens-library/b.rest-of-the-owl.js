// I used ChatGPT 3.5 to port b.py to JavaScript. I did make some changes, but
// it did a solid job, and it seems to work!

const fs = require('fs');

/**
 * EqualsStep.type always == '='
 */
class EqualsStep {
  constructor(type, label, focal_length) {
    this.type = type;
    this.label = label;
    this.focal_length = focal_length;
  }
}

/**
 * DashStep.type always == '-'
 */
class DashStep {
  constructor(type, label) {
    this.type = type;
    this.label = label;
  }
}

class Lens {
  constructor(label, focal_length) {
    this.label = label;
    this.focal_length = focal_length;
  }
}

function readInputAndPopulateBoxes() {
  const fileContent = fs.readFileSync(process.argv[2], 'utf-8');
  const steps = fileContent.split(',').map(parseStep);

  // After auto-porting, I changed the implementation to use an array of boxes
  // instead of a dictionary of boxes.
  const boxes = [];
  for (let i = 0; i < 256; i++) {
    boxes.push([]);
  }

  steps.forEach((step) => {
    const box = boxes[getHash(step.label)];
    if (step.type === '-') {
      removeBy(box, (lens) => lens.label === step.label);
    } else if (step.type === '=') {
      const lens = new Lens(step.label, step.focal_length);
      // ChatGPT did not recognize that index_by was essentially the same as
      // Array.find, but with prompting it did replace and remove index_by.
      const existingLens = box.find((l) => l.label === step.label);
      if (existingLens) {
        existingLens.focal_length = step.focal_length;
      } else {
        box.push(lens);
      }
    }
  });

  return boxes;
}

function show(boxes) {
  function formatLens(lens) {
    return `[${lens.label} ${lens.focal_length}]`;
  }

  for (const [i, box] of Object.entries(boxes)) {
    if (box.length > 0) {
      console.log(`Box ${i} ${box.map(formatLens).join(' ')}`);
    }
  }
}

function getHash(s) {
  let n = 0;
  for (const ch of s) {
    n += ch.charCodeAt(0);
    n = (n * 17) % 256;
  }
  return n;
}

function parseStep(step) {
  const matchEquals = sscanf(step, '%s=%u');
  if (matchEquals) {
    return new EqualsStep('=', ...matchEquals);
  }

  const matchDash = sscanf(step, '%s-');
  if (matchDash) {
    return new DashStep('-', ...matchDash);
  }

  throw new Error('parse error ' + step);
}

function removeBy(lst, pred) {
  const matches = lst.reduce((acc, x, i) => (pred(x) ? [...acc, i] : acc), []);
  if (matches.length === 1) {
    lst.splice(matches[0], 1);
  } else if (matches.length === 0) {
    // do nothing
  } else {
    throw new Error('unexpected case');
  }
}

function sscanf(s, fmt) {
  const slotPattern = /(%s|%u)/;
  let pattern = '';
  const slotTypes = [];
  for (const part of fmt.split(slotPattern)) {
    const isSlot = slotPattern.test(part);
    if (isSlot) {
      slotTypes.push(part);
      if (part === '%s') {
        pattern += '(.+?)';
      } else if (part === '%u') {
        pattern += '(\\d+?)';
      } else {
        throw new Error('Invalid placeholder');
      }
    } else {
      pattern += part.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
    }
  }

  const match = new RegExp(pattern).exec(s);
  if (!match) {
    return null;
  }

  const result = [];
  for (let i = 1; i < match.length; i++) {
    const rawValue = match[i];
    const slotType = slotTypes[i - 1];
    let value;
    if (slotType === '%s') {
      value = rawValue;
    } else if (slotType === '%u') {
      value = parseInt(rawValue, 10);
    }
    result.push(value);
  }
  return result;
}

module.exports = {
  readInputAndPopulateBoxes
};
