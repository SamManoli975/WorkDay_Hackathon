from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/ai_edit', methods=['POST'])
def ai_edit():
    data = request.get_json()
    text = data.get('text', '')
    print("Received for edit:", text)

    return jsonify({
        "response": f"✔️ AI Edited: '{text[:50]}'... (mock result)"
    })

@app.route('/api/ai_suggestions', methods=['POST'])
def ai_suggestions():
    data = request.get_json()
    text = data.get('text', '')
    print("Received for suggestions:", text)

    return jsonify({
        "response": f"💡 AI Suggestions for: '{text[:50]}'... (mock result)"
    })

if __name__ == '__main__':
    app.run(debug=True, port=3000)
