import fs from 'fs'
import {bisector} from 'd3'

const bisect = bisector(i => i.float)

// Load the index data
const indexData = JSON.parse(fs.readFileSync('../../data/dataset3_index.json'));

// Get the list of indices
const indices = Object.keys(indexData);

// Precompute cumulative weights
let cumWeights = [];
cumWeights = fs.readFileSync('../../data/cum_weights.json');

console.log('Finished counting weights');

// Custom weighted random choice function
function weightedChoice(indices, cumWeights) {
  let r = Math.random() * cumWeights[cumWeights.length - 1];
  let idx = bisect.left(cumWeights, r);
  return indices[idx];
}

// Select 25 words using the weighted_choice function
let selectedWords = [];
let selectedWordObjects = [];

for (let i = 0; i < 25; i++) {
  let index = weightedChoice(indices, cumWeights);
  let byteOffset = indexData[index];

  // Access the word in the JSONL file using the byte offset
  let fileData = fs.readFileSync('../../data/dataset3.jl');
  let lines = fileData.toString().split('\n');
  let entry = JSON.parse(lines[index]);
  let word = Object.keys(entry)[0];
  selectedWords.push(word);
  selectedWordObjects.push({ [word]: entry[word] });
}

// Print the word objects
console.log(JSON.stringify(selectedWordObjects, null, 2));

// Print the 25 words
console.log(selectedWords.join(' '));

