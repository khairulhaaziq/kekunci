import json

# Load the JSON data from the file
with open('dataset3.json', 'r') as f:
    data = json.load(f)

total_words = len(data)
progress_interval = 100

# Add an index key to each object
for i, key in enumerate(data):
    data[key]['index'] = i + 1

    if (i + 1) % progress_interval == 0:
        progress = f"Processed {i+1}/{total_words} words"
        print(progress, end='\r')

# Write the updated data back to the file
with open('dataset3.json', 'w') as f:
    json.dump(data, f, indent=2)