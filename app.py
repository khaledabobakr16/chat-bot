from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import re  # Regular expressions module for better pattern matching

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load intents from the intents.json file
try:
    with open('intents.json') as json_file:
        intents = json.load(json_file)
except Exception as e:
    intents = {"intents": []}  # Fallback if loading fails

# Function to match user input with patterns
def match_intent(user_input):
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # Using regex search to match patterns more flexibly (case-insensitive)
            if re.search(re.escape(pattern), user_input, re.IGNORECASE):
                return random.choice(intent['responses'])
    return "Sorry, I didn't understand that."  # Default fallback response

# Define a simple route for the root path
@app.route("/", methods=["GET"])
def home():
    return "Chatbot API is running!"

# Define a route for the chatbot API
@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.get_json()  # Expecting JSON input from the Flutter frontend
    user_input = data.get("message")  # The "message" key contains the user's input
    
    if user_input:
        response = match_intent(user_input)  # Get response from matching function
        return jsonify({"response": response})  # Returning response as JSON
    else:
        return jsonify({"response": "No message received."})  # Handle empty input

if __name__ == "__main__":
    app.run(debug=True)
