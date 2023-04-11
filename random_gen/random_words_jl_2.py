import sys
import json
import bisect
import random
import time
import os
import psutil

index_data = {}
limit = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
num_words = int(sys.argv[2]) if len(sys.argv) > 2 else 25
selected_char = sys.argv[3] if len(sys.argv) > 3 else ''
start_time = time.time()

with open('../data/dataset3_index.jl', 'r') as f:
    for i, line in enumerate(f):
        if i < limit:
            key, value = list(json.loads(line.strip()).items())[0]
            index_data[key] = value
        else:
            load_index_time = time.time() - start_time
            break

indices = list(index_data.keys())
cum_weights = []
total_weight = 0
for i in range(len(indices)):
    total_weight += 1 / (i + 1)
    cum_weights.append(total_weight)

elapsed_time = time.time() - start_time


def weighted_choice(indices, cum_weights):
    r = random.uniform(0, cum_weights[-1])
    idx = bisect.bisect_left(cum_weights, r)
    return indices[idx]


def checkContainSelectedChar(word):
    if (selected_char in word):
        return True
    return False

selected_words = []
selected_word_objects = []
selected_indices = set()

while len(selected_words) < num_words:
    index = weighted_choice(indices, cum_weights)
    if index not in selected_indices:
        selected_indices.add(index)
        byte_offset = index_data[index]

        with open('../data/dataset3.jl', 'r') as f:
            f.seek(byte_offset)
            line = f.readline()
            entry = json.loads(line)
            word = list(entry.keys())[0]
            if (selected_char == "" or (selected_char and (checkContainSelectedChar(word)))):
                selected_words.append(word)
                selected_word_objects.append({word: entry[word]})

print(json.dumps(selected_word_objects, indent=2))
print(" ".join(selected_words))
print(f"Load index time: {load_index_time:.3f} seconds")
print(f"Weight time: {elapsed_time:.3f} seconds")
#
#cpu_percent = psutil.cpu_percent(interval=1)
#memory_percent = psutil.virtual_memory().percent

# output_data = {
#     "elapsed_time": elapsed_time,
#     "cpu_percent": cpu_percent,
#     "memory_percent": memory_percent
# }
# with open("python_output.jl", "a") as f:
#     f.write(json.dumps(output_data) + '\n')
