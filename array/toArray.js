function toArray(data, attr) {
  let arr = [];
  for (let i in data) {
    arr.push(data[i][attr]);
  }
  return arr;
}

module.exports = toArray;
