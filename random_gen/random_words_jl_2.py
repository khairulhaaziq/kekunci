import json
import bisect
import random

# Load the index data
with open('../data/dataset3_index.json', 'r') as f:
    index_data = json.load(f)

# Get the list of indices
indices = list(index_data.keys())

# Precompute cumulative weights
cum_weights = []
total_weight = 0
for i in range(len(indices)):
    total_weight += 1 / (i + 1)
    cum_weights.append(total_weight)

#with open('../data/cum_weights.json', 'r')as f:
#   cum_weights = json.load(f)

print('finished counting weights')

# Custom weighted random choice function
def weighted_choice(indices, cum_weights):
    r = random.uniform(0, cum_weights[-1])
    idx = bisect.bisect_left(cum_weights, r)
    return indices[idx]

# Select 25 words using the weighted_choice function
selected_words = []
selected_word_objects = []

for _ in range(25):
    index = weighted_choice(indices, cum_weights)
    byte_offset = index_data[index]

    # Access the word in the JSONL file using the byte offset
    with open('../data/dataset3.jl', 'r') as f:
        f.seek(byte_offset)
        line = f.readline()
        entry = json.loads(line)
        word = list(entry.keys())[0]
        selected_words.append(word)
        selected_word_objects.append({word: entry[word]})

# Print the word objects
print(json.dumps(selected_word_objects, indent=2))

# Print the 25 words
print(" ".join(selected_words))
