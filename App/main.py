from flask import Flask, request, jsonify
from flask_cors import CORS
from Modules.api import API_response
from Modules.gemini import narrate
from Modules.coords import coords
from Modules.audio import get_inaturalist_audio

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])  
def index():
    if request.method == "POST":
        location = request.json.get('location')
        
        if not location:
            return jsonify({"undocumented-location": "Unfortunately, we don't have that location documented :("})
        
        try:
            map_plots = coords(location)
            species = API_response(location)

            specie_list = list(species.keys())
            narrations = narrate(specie_list, location)  # Get narrations as a list

            species_data = {
                specie: {
                    "narration": narrations[index],  # Map each narration to the corresponding species
                    "images": species[specie],
                    "coords": map_plots,
                    "audio": get_inaturalist_audio(specie)
                } for index, specie in enumerate(specie_list)
            }

            return jsonify(species_data)
        
        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'})
    
    else:
        return ""

    
if __name__ == "__main__":
    app.run(debug=True)