import json
import random
import math

# Load the dataset3.json
with open('../data/dataset3.json', 'r') as f:
    data = json.load(f)

words = list(data.keys())
num_words = len(words)


# Custom inverse exponential distribution function
def inverse_exponential_index(scale, num_words):
    r = random.random()
    idx = int(scale * (1 - math.log(1 - r)) - 1)
    return min(idx, num_words - 1)


# Select 25 words using the inverse_exponential_index function
selected_words = []
selected_word_objects = []
scale = 50

for _ in range(25):
    index = inverse_exponential_index(scale, num_words)
    word = words[index]
    selected_words.append(word)
    selected_word_objects.append({word: data[word]})

# Print the word objects
print(json.dumps(selected_word_objects, indent=2))

# Print the 25 words
print(" ".join(selected_words))
