import json

# Read dataset3.jsonl and create an index file
with open('../data/dataset3.jl', 'r') as f:
    index_data = {}
    byte_offset = 0
    for line in f:
        entry = json.loads(line)
        word = list(entry.keys())[0]
        index = entry[word]['index']
        index_data[index] = byte_offset
        byte_offset += len(line)

# Write the index file
with open('../data/dataset3_index.json', 'w') as f:
    json.dump(index_data, f, indent=2)
