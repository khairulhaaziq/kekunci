import json
import bisect
import random

with open('../data/dataset3_index.json', 'r') as f:
    index_data = json.load(f)

indices = list(index_data.keys())

cum_weights = []
total_weight = 0
for i in range(len(indices)):
    total_weight += 1 / (i + 1)
    cum_weights.append(total_weight)


def weighted_choice(indices, cum_weights):
    r = random.uniform(0, cum_weights[-1])
    idx = bisect.bisect_left(cum_weights, r)
    return indices[idx]


def get_words():
    selected_indices = set()  # Keep track of selected indices
    selected_words = []
    selected_word_objects = []

    while len(selected_words) < 25:
        index = weighted_choice(indices, cum_weights)
        if index not in selected_indices:
            selected_indices.add(index)
            byte_offset = index_data[index]

            with open('../data/dataset3.jl', 'r') as f:
                f.seek(byte_offset)
                line = f.readline()
                entry = json.loads(line)
                word = list(entry.keys())[0]
                selected_words.append(word)
                selected_word_objects.append({word: entry[word]})

    selected_word_objects.append({"all_words": selected_words})
    return selected_word_objects
