package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"sort")


func main() {
	// Load the index data
	file, err := os.Open("../data/dataset3_index.json")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	decoder := json.NewDecoder(file)
	var indexData map[string]int64
	decoder.Decode(&indexData)

	// Get the list of indices
	indices := make([]string, 0, len(indexData))
	for k := range indexData {
		indices = append(indices, k)
	}

	// Precompute cumulative weights
	cumWeights := make([]float64, len(indices))
	totalWeight := 0.0
	for i := range indices {
		totalWeight += 1 / float64(i+1)
		cumWeights[i] = totalWeight
	}

	fmt.Println("Finished counting weights")

	// Custom weighted random choice function
	weightedChoice := func(indices []string, cumWeights []float64) string {
		r := rand.Float64() * cumWeights[len(cumWeights)-1]
		idx := sort.Search(len(cumWeights), func(i int) bool { return cumWeights[i] >= r })
		return indices[idx]
	}

	// Select 25 words using the weighted_choice function
	selectedWords := make([]string, 0, 25)
	selectedWordObjects := make([]map[string]interface{}, 0, 25)

	for i := 0; i < 25; i++ {
		index := weightedChoice(indices, cumWeights)
		byteOffset := indexData[index]

		// Access the word in the JSONL file using the byte offset
		file, err := os.Open("../data/dataset3.jl")
		if err != nil {
			panic(err)
		}
		defer file.Close()

		file.Seek(byteOffset, 0)
		reader := bufio.NewReader(file)
		line, _, err := reader.ReadLine()
		if err != nil {
			panic(err)
		}

		var entry map[string]interface{}
		json.Unmarshal(line, &entry)
		for k := range entry {
			selectedWords = append(selectedWords, k)
			selectedWordObjects = append(selectedWordObjects, map[string]interface{}{k: entry[k]})
			break
		}
	}

	// Print the word objects
	wordObjectsJson, _ := json.MarshalIndent(selectedWordObjects, "", "  ")
	fmt.Println(string(wordObjectsJson))

	// Print the 25 words
	fmt.Println(selectedWords)
}


