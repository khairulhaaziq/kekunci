#this code fills the words with no morphemes with the words themselves

import json

with open('dataset3.json', 'r')as f:
        data = json.load(f)

for word, morphemes_dict in data.items():
        if not morphemes_dict['morphemes']:
                morphemes_dict['morphemes'] = [word]

with open('dataset3.json', 'w')as f:
        json.dump(data, f, indent=2)