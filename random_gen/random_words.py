import json
import bisect
import random

# Load the dataset3.json
with open('../data/dataset3.json', 'r') as f:
    data = json.load(f)

words = list(data.keys())

# Precompute cumulative weights
cum_weights = []
total_weight = 0
for i in range(len(words)):
    total_weight += 1 / (i + 1)
    cum_weights.append(total_weight)

# Custom weighted random choice function
def weighted_choice(words, cum_weights):
    r = random.uniform(0, cum_weights[-1])
    idx = bisect.bisect_left(cum_weights, r)
    return words[idx]

# Select 25 words using the weighted_choice function
selected_words = []
selected_word_objects = []

for _ in range(25):
    word = weighted_choice(words, cum_weights)
    selected_words.append(word)
    selected_word_objects.append({word: data[word]})

# Print the word objects
print(json.dumps(selected_word_objects, indent=2))

# Print the 25 words
print(" ".join(selected_words))
