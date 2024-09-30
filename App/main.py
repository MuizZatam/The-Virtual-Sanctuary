from flask import Flask, request, jsonify
from flask_cors import CORS
from Modules.api import API_Response

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])  
def index():
    if request.method == "POST":
        location = request.json.get('location')
        
        if not location:
            return jsonify({"error": "Location not provided"}), 400
        
        try:
            result = API_Response(location)
            
            if "error" in result:
                return jsonify(result), 404

            return jsonify(result)
        
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    return ""

if __name__ == "__main__":
    app.run(debug=True)