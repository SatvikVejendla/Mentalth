const tf = require("@tensorflow/tfjs");
require("@tensorflow/tfjs-node");

const toxicity = require("@tensorflow-models/toxicity");
const threshold = require("../config/toxicity.js").threshold;

function classify(str) {
  return new Promise((resolve) => {
    toxicity.load(threshold).then((model) => {
      const sentences = str[0].constructor === Array ? str : [str];
      model.classify(sentences).then((predictions) => {
        resolve(predictions);
      });
    });
  });
}

module.exports = classify;
