import json

# Read the original JSON file
with open('../data/dataset3_index.json', 'r') as f:
    data = json.load(f)

# Write the data to a JSON Lines file
with open('../data/dataset3_index.jl', 'w') as f:
    for key, value in data.items():
        json_line = json.dumps({key: value})
        f.write(f"{json_line}\n")
