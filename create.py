import json

# Load the dataset
with open('morphemes.json', 'r') as f:
    data = json.load(f)

# Create a new dataset with empty examples arrays for each morpheme
new_data = {}
for morpheme in data.keys():
    separated_morphemes = morpheme.split(', ')
    for single_morpheme in separated_morphemes:
        new_data[single_morpheme] = {
            "examples": []
        }

# Write the new dataset to dataset2.json
with open('dataset2.json', 'w') as f:
    json.dump(new_data, f, indent=2)