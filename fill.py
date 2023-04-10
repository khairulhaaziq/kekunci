import csv
import json

# Load the dataset
with open('dataset2.json', 'r') as f:
    data = json.load(f)

# Load the words and their frequencies from the CSV file
words = []
with open('words.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        word, frequency = row
        words.append(word)

total_words = len(words)
progress_interval = 100

# Find matching prefixes and suffixes and update the examples
for i, word in enumerate(words):
    for morpheme in data.keys():
        clean_morpheme = morpheme.replace('-', '')

        if morpheme.endswith('-') and word.startswith(clean_morpheme):
            data[morpheme]['examples'].append(word)
        elif morpheme.startswith('-') and word.endswith(clean_morpheme):
            data[morpheme]['examples'].append(word)

    if (i + 1) % progress_interval == 0:
        progress = f"Processed {i+1}/{total_words} words"
        print(progress, end='\r')

# Write the updated dataset back to dataset2.json
with open('dataset2.json', 'w') as f:
    json.dump(data, f, indent=2)
