from flask import Flask, request, jsonify
from flask_cors import CORS
from main2 import run_ai_edit, run_ai_suggestions  # Import from main2

app = Flask(__name__)
CORS(app)

@app.route('/api/ai_edit', methods=['POST'])
def ai_edit():
    data = request.get_json()
    text = data.get('text', '')
    print("Received for edit:", text)

    response_text = run_ai_edit(text)
    return jsonify({"response": response_text})

@app.route('/api/ai_suggestions', methods=['POST'])
def ai_suggestions():
    data = request.get_json()
    text = data.get('text', '')
    print("Received for suggestions:", text)

    response_text = run_ai_suggestions(text)
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
