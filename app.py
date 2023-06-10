from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
import string
import json
import nltk

app = Flask(__name__)

nltk.download('punkt')

def preprocess(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]

    # Join the tokens back into a single string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

# Load training data from file
def load_training_data():
    with open('data.txt', 'r') as file:
        data = json.load(file)
        training_data = [(qa['question'], qa['answer']) for qa in data]
    return training_data

# Preprocess training data
training_data = load_training_data()
preprocessed_data = [preprocess(question) for question, _ in training_data]

# Initialize the vectorizer
vectorizer = TfidfVectorizer(tokenizer=preprocess)

# Fit the vectorizer on the preprocessed training data
query_vector = vectorizer.fit_transform(preprocessed_data)

def get_chatbot_response(user_input, threshold=0.2):
    preprocessed_input = preprocess(user_input)
    query_vector_input = vectorizer.transform([preprocessed_input])  # Transform the preprocessed input
    similarities = cosine_similarity(query_vector_input, query_vector)  # Compute cosine similarities
    most_similar_indices = similarities.argsort()[0][::-1]  # Sort indices in descending order
    responses = []
    for index in most_similar_indices:
        similarity_score = similarities[0][index]
        if similarity_score >= threshold:
            responses.append((training_data[index][1], similarity_score))
    responses.sort(key=lambda x: x[1], reverse=True)  # Sort responses by similarity score in descending order
    return [response[0] for response in responses]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['user_input']
    responses = get_chatbot_response(user_input)
    return jsonify({'response': responses[0], 'alternatives': responses[1:]})

if __name__ == '__main__':
    app.run(debug=True)
