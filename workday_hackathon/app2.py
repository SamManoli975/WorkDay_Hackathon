import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Import AI functions from main2.py ---
try:
    print("Importing functions from main2...")
    from main2 import run_ai_edit, run_ai_suggestions
    print("Functions imported successfully.")
except SystemExit as e:
    # Catch SystemExit if main2.py exited early
    print(f"CRITICAL: Exiting Flask app because main2.py failed to initialize. Error: {e}")
    exit(1)
except ImportError as e:
    print(f"CRITICAL: Failed to import from main2.py. Is it in the same directory? Error: {e}")
    exit(1)
except Exception as e:
    print(f"CRITICAL: Unexpected error importing main2.py: {e}")
    exit(1)

# --- Flask App Setup ---
app = Flask(__name__)

# Configure CORS more explicitly
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5000", "*"],  # Allow all origins for API endpoints
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# --- API Routes ---
@app.route('/api/ai_edit', methods=['POST', 'OPTIONS'])
def ai_edit():
    """API endpoint to improve text clarity and grammar."""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    # Handle POST request
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    text = data.get('text')
    
    if text is None:
        return jsonify({"error": "Missing 'text' field in JSON payload"}), 400
    
    print(f"Received for edit (first 50 chars): '{text[:50]}...'")
    
    try:
        # Call the function imported from main2.py
        response_text = run_ai_edit(text)
        # Ensure we have a string to return
        if response_text is None:
            response_text = ""
        
        print(f"Sending edit response (first 50 chars): '{response_text[:50]}...'")
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error processing /api/ai_edit: {e}")
        # Return error as JSON
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

@app.route('/api/ai_suggestions', methods=['POST', 'OPTIONS'])
def ai_suggestions():
    """API endpoint to suggest improvements or alternatives for text."""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 204
    
    # Handle POST request
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    text = data.get('text')
    
    if text is None:
        return jsonify({"error": "Missing 'text' field in JSON payload"}), 400
    
    print(f"Received for suggestions (first 50 chars): '{text[:50]}...'")
    
    try:
        # Call the function imported from main2.py
        response_text = run_ai_suggestions(text)
        # Ensure we have a string to return
        if response_text is None:
            response_text = ""
            
        print(f"Sending suggestions response (first 50 chars): '{response_text[:50]}...'")
        return jsonify({"response": response_text})
    except Exception as e:
        print(f"Error processing /api/ai_suggestions: {e}")
        # Return error as JSON 
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

# --- Debug Endpoint ---
@app.route('/debug', methods=['GET', 'POST'])
def debug_endpoint():
    """Debug endpoint that echoes back request information."""
    if request.method == 'GET':
        return jsonify({
            "message": "Debug endpoint working",
            "method": "GET",
            "args": request.args.to_dict()
        })
    else:  # POST
        return jsonify({
            "message": "Debug endpoint working",
            "method": "POST",
            "json": request.get_json() if request.is_json else None,
            "headers": {k: v for k, v in request.headers.items()}
        })

# --- Health Check Route ---
@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "ok"}), 200

# --- Run Flask App ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    print(f"Starting Flask server on port {port} with debug={debug_mode}")
    app.run(debug=debug_mode, port=port, host='0.0.0.0')