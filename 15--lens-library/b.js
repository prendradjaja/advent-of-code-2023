#!/usr/bin/env node

const fs = require('fs');
const { readInputAndPopulateBoxes } = require('./b.rest-of-the-owl');


const boxes = readInputAndPopulateBoxes();
const answer =
  boxes
    .flatMap((box, i) =>
      box.map((lens, j) => lens.focal_length * (j + 1) * (i + 1))
    )
    .reduce((a, b) => a + b);
console.log(answer);
