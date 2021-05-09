const mean = require("./mean.js");

// A variation of the standard deviation formula

function stdDeviation(arr) {
  let avg = mean(arr);
  let result = arr.map((i) => (i - avg) * Math.abs(i - avg)); //square it but keep the sign
  return result;
}

module.exports = stdDeviation;
