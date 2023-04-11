import process from 'process';
import fs from 'fs';
import readline from 'readline';
import { bisectLeft } from 'd3-array';
import os from 'os';

const limit = parseInt(process.argv[2]) || 1000;
const num_words = parseInt(process.argv[3]) || 25;
const selected_char = process.argv[4] || '';
const startTime = Date.now();
let loadIndexTime;

async function loadIndexData() {
  const indexData = {};
  const fileStream = fs.createReadStream('../data/dataset3_index.jl');

  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity,
  });

  let lineNumber = 0;
  for await (const line of rl) {
    if (lineNumber < limit) {
      const [key, value] = Object.entries(JSON.parse(line.trim()))[0];
      indexData[key] = value;
    } else {
      break;
    }
    lineNumber++;
  }

  loadIndexTime = (Date.now() - startTime) / 1000;

  return indexData;
}

function weightedChoice(indices, cumWeights) {
  const r = Math.random() * cumWeights[cumWeights.length - 1];
  const idx = bisectLeft(cumWeights, r);
  return indices[idx];
}

function readEntryFromFile(fd, byteOffset, callback) {
  const buffer = Buffer.alloc(200);
  fs.read(fd, buffer, 0, buffer.length, byteOffset, (err, bytesRead) => {
    if (err) {
      callback(err);
    } else {
      const entry = JSON.parse(buffer.slice(0, bytesRead).toString().split('\n')[0]);
      callback(null, entry);
    }
  });
}

function checkContainSelectedChar(word) {
  if (word.includes(selected_char)){
    return true
  }
  return false
}

(async function main() {
  const indexData = await loadIndexData(limit);
  const indices = Object.keys(indexData);

  const cumWeights = [];
  let totalWeight = 0;
  for (let i = 0; i < indices.length; i++) {
    totalWeight += 1 / (i + 1);
    cumWeights.push(totalWeight);
  }

  const selectedWords = [];
  const selectedWordObjects = [];
  const selectedIndices = new Set();

  let weightTime;

  const fd = fs.openSync('../data/dataset3.jl', 'r');

  while (selectedWords.length < num_words) {
    const batchIndices = new Set();
    const batchPromises = [];

    while (batchIndices.size < 100) {
      const index = weightedChoice(indices, cumWeights);

      weightTime = (Date.now() - startTime) / 1000;

      if (!selectedIndices.has(index)) {
        batchIndices.add(index);
        selectedIndices.add(index);
        const byteOffset = indexData[index];
        batchPromises.push(
          new Promise((resolve, reject) => {
            readEntryFromFile(fd, byteOffset, (err, entry) => {
              if (err) reject(err);
              else resolve(entry);
            });
          })
        );
      }
    }

    const batchResults = await Promise.all(batchPromises);
    for (const entry of batchResults) {
      const word = Object.keys(entry)[0];
      if (selectedWords.length < num_words && (selected_char ? checkContainSelectedChar(word) : true)) {
        selectedWords.push(word);
        selectedWordObjects.push({ [word]: entry[word] });
      }
    }
  }

  fs.closeSync(fd);

  console.log(JSON.stringify(selectedWordObjects, null, 2));
  console.log(selectedWords.join(' '));
  console.log('Load index time: ' + loadIndexTime + ' seconds');
  console.log('Weight time: ' + weightTime + ' seconds');

  // const cpuPercent = parseFloat((os.loadavg()[0] * 100).toFixed(2));
  // const memoryPercent = parseFloat(((os.freemem() / os.totalmem()) * 100).toFixed(2));
  // const outputData = { elapsed_time: weightTime, cpu_percent: cpuPercent, memory_percent: memoryPercent };
  // const outputString = JSON.stringify(outputData) + '\n';
  // fs.appendFileSync('node_output.jl', outputString);  
})();