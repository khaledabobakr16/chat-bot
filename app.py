from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)


try:
    with open('intents.json') as json_file:
        intents = json.load(json_file)
except Exception as e:
    print(f"Error loading intents.json: {e}")
    intents = {"intents": []}  

def match_intent_with_similarity(user_input):
    """
    Matches the user input with patterns in intents.json using cosine similarity.
    """
    patterns = []
    responses = {}
    tags = []

    
    for intent in intents['intents']:
        if 'patterns' in intent and 'responses' in intent:  
            for pattern in intent['patterns']:
                patterns.append(pattern)
                responses[pattern] = intent['responses']  
            tags.append(intent['tag'])

    if not patterns or not responses:  
        return "Error: No patterns or responses available."

    
    vectorizer = TfidfVectorizer().fit_transform([user_input] + patterns)
    vectors = vectorizer.toarray()

    
    user_vector = vectors[0]  
    patterns_vectors = vectors[1:]  
    similarities = cosine_similarity([user_vector], patterns_vectors)[0]

    
    max_index = np.argmax(similarities)
    max_similarity = similarities[max_index]

    
    if max_similarity > 0.5:  
        matched_pattern = patterns[max_index]
        matched_responses = responses[matched_pattern]  
        return random.choice(matched_responses)  

    return "Sorry, I couldn't understand that. Could you clarify?"  


@app.route("/", methods=["GET"])
def home():
    return "Chatbot API is running!"


@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.get_json()  
    user_input = data.get("message")  

    if user_input:
        response = match_intent_with_similarity(user_input)  
        return jsonify({"response": response})  
    else:
        return jsonify({"response": "No message received."})  

if __name__ == "__main__":
    app.run(debug=True)


