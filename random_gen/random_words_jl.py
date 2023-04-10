import json
import random

def get_random_word(scale):
    with open('../data/dataset3.jl', 'r') as f:
        lines = f.readlines()
        total_lines = len(lines)

        while True:
            random_index = int(random.weibullvariate(scale, 1))
            if random_index < total_lines:
                break

        json_line = lines[random_index].strip()
        word_data = json.loads(json_line)
        word = list(word_data.keys())[0]

    return word

selected_words = [get_random_word(scale=15) for _ in range(25)]
print(" ".join(selected_words))

selected_data = []
for word in selected_words:
    with open('../data/dataset3.jl', 'r') as f:
        for line in f:
            json_line = json.loads(line.strip())
            if word in json_line:
                selected_data.append(json_line)
                break

print(json.dumps(selected_data, indent=2))
