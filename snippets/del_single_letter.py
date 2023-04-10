import json

def delete_single_letter_objects(json_file):
    # Load the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Find all single letter keys
    single_letter_keys = [key for key in data.keys() if len(key) == 1]

    # Delete objects with single letter keys
    for key in single_letter_keys:
        del data[key]

    # Write the updated data back to the JSON file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)

delete_single_letter_objects("dataset3_copy.json")