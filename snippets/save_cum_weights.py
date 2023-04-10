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


with open('../data/cum_weights.json', 'w')as f:
        json.dump(cum_weights, f)
