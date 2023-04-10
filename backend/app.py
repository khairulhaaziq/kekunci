from flask import Flask, jsonify
from flask_cors import CORS
from word_generator import get_words

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/words', methods=['GET'])
def api_get_words():
    selected_word_objects = get_words()
    word_data = {}

    for word_object in selected_word_objects:
        word = list(word_object.keys())[0]
        word_data[word] = word_object[word]

    response_data = {
        **word_data,
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
