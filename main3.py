import json
import random
import re

# Function to check if a word has more than 5 consonants
def has_more_than_five_consonants(word):
    consonant_count = len(re.findall(r"[bcdfghjklmnpqrstvwxyz]", word))
    return consonant_count > 5

# Load the dataset
with open('morphemes.json', 'r') as f:
    data = json.load(f)

# Filter morphemes to have 3 or fewer characters (excluding '-')
filtered_morphemes = []
for morpheme in data.keys():
    if len(morpheme.replace('-', '').replace(',', '')) > 3:
        continue

    examples = data[morpheme]['examples']
    valid_examples = [word for word in examples if not has_more_than_five_consonants(word)]

    if len(valid_examples) > 0:
        filtered_morphemes.append(morpheme)

# Get 22 unique morphemes and their example words
selected_morphemes = random.sample(filtered_morphemes, 22)
selected_words = [random.choice(data[morpheme]['examples']) for morpheme in selected_morphemes]

# Get 3 random words with more than 3 characters
long_word_candidates = [(word, morpheme) for morpheme, value in data.items() for word in value['examples'] if len(word) > 3 and not has_more_than_five_consonants(word)]
long_words = random.sample(long_word_candidates, 3)

selected_words.extend([word for word, _ in long_words])
selected_morphemes.extend([morpheme for _, morpheme in long_words])

# Print the 25 words
print(" ".join(selected_words))

# Print the word-morpheme pairs
word_morpheme_pairs = []

for word, morpheme in zip(selected_words, selected_morphemes):
    word_morpheme_pairs.append({
        "word": word,
        "morpheme": morpheme
    })

print(json.dumps(word_morpheme_pairs, indent=2))
