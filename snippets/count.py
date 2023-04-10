import json

# Load the dataset
with open('morphemes.json', 'r') as f:
    data = json.load(f)

# Count the number of morphemes
morpheme_count = len(data)

# Count the total number of examples
example_count = 0
for value in data.values():
    example_count += len(value['examples'])

# Print the results
print(f"Number of morphemes: {morpheme_count}")
print(f"Total number of examples: {example_count}")
