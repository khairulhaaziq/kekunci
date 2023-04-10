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

word_morphemes = {}

# Find matching prefixes and suffixes
for i, word in enumerate(words):
    morphemes_for_word = []
    for morpheme in data.keys():
        clean_morpheme = morpheme.replace('-', '')

        if morpheme.endswith('-') and word.startswith(clean_morpheme):
            morphemes_for_word.append(morpheme)
        elif morpheme.startswith('-') and word.endswith(clean_morpheme):
            morphemes_for_word.append(morpheme)

    word_morphemes[word] = {"morphemes": morphemes_for_word}

    if (i + 1) % progress_interval == 0:
        progress = f"Processed {i+1}/{total_words} words"
        print(progress, end='\r')

# Write the word-morpheme mapping to dataset3.json
with open('dataset3.json', 'w') as f:
    json.dump(word_morphemes, f, indent=2)
