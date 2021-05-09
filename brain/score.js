const stdDeviation = require("../math/deviation.js");
const toArray = require("../array/toArray.js");

function getScore(data, val) {
  let arr = toArray(data, "score");
  let output = stdDeviation(arr);
  return output[val];
}

module.exports = getScore;
