<<<<<<< Updated upstream
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# @app.route('/api/ai_edit', methods=['POST'])
# def ai_edit():
#     data = request.get_json()
#     text = data.get('text', '')
#     print("Received for edit:", text)

#     return jsonify({
#         "response": f"✔️ AI Edited: '{text[:50]}'... (mock result)"
#     })

# @app.route('/api/ai_suggestions', methods=['POST'])
# def ai_suggestions():
#     data = request.get_json()
#     text = data.get('text', '')
#     print("Received for suggestions:", text)

    
#     return jsonify({
#         "response": f"💡 AI Suggestions for: '{text[:50]}'... (mock result)"
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=3000)
=======
# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure this import is present
import os

# --- Import the core logic function ---
from mainV3 import summarize, llm

app = Flask(__name__)

# --- MODIFIED CORS Configuration ---
# Apply CORS globally, allowing requests from any origin (*)
# and specifically enabling common headers like Content-Type.
# For production, you might want to restrict origins more tightly.
CORS(app, resources={r"/api/*": {"origins": "*"}})
# ---------------------------------

# --- Check if LLM was initialized successfully ---
if llm is None:
    print("*"*20)
    print("WARNING: LLM failed to initialize in query_processor.py.")
    print("The /api/process_query endpoint will likely return errors.")
    print("Ensure GROQ_API_KEY is set correctly as an environment variable.")
    print("*"*20)

@app.route('/')
def home():
    return "Flask server is running!"

@app.route('/api/process_query', methods=['POST', 'OPTIONS']) # Add OPTIONS method
def handle_process_query():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    text = data.get('text')

    if text is None:
        return jsonify({"error": "Missing 'text' field in request body"}), 400
    if not isinstance(text, str):
         return jsonify({"error": "'text' field must be a string"}), 400

    print(f"Received for processing: '{text}'")

    if llm is None:
        return jsonify({"error": "Query processing unavailable due to LLM initialization failure."}), 503

    try:
        result = process_query(text)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error processing query '{text}': {e}")
        return jsonify({"error": "An internal error occurred during query processing."}), 500

@app.route('/api/ai_edit', methods=['POST', 'OPTIONS']) # Add OPTIONS method
def ai_edit():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    # Existing POST logic
    if not request.is_json:
         return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    text = data.get('text', '')
    print("Received for edit:", text)
    response_data = {"response": f"✔️ AI Edited: '{text[:50]}'... (mock result)"}
    return jsonify(response_data), 200


@app.route('/api/ai_suggestions', methods=['POST', 'OPTIONS']) # Add OPTIONS method
def ai_suggestions():
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    # Existing POST logic
    if not request.is_json:
         return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    text = data.get('text', '')
    print("Received for suggestions:", text)
    response_data = {"response": f"💡 AI Suggestions for: '{text[:50]}'... (mock result)"}
    return jsonify(response_data), 200

# --- Helper function for CORS preflight responses ---
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*") # Or specific origin
    response.headers.add('Access-Control-Allow-Headers', "*") # Allow all headers
    response.headers.add('Access-Control-Allow-Methods', "*") # Allow all methods
    return response

# --- Need to import make_response ---
from flask import make_response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
>>>>>>> Stashed changes
