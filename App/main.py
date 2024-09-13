from flask import Flask, request, jsonify
from Modules.api import API_response
from Modules.gemini import narrate
from Modules.coords import coords

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        location = request.form.get("location")
        
        if not location:

            return jsonify({"undocumented-location": "Unfortunately, we don't have that location documented :("})
        
        try:

            map_plots = coords(location)
            species = API_response(location)

            specie_list = list()
            narrations = list()

            for key in species.keys():

                specie_list.append(key)
            
            narrations = narrate(specie_list, location).split('sep')

            species_data = dict()
            for index, specie in enumerate(specie_list):
                
                species_data[specie] = {

                    "narration": narrations[index],
                    "images": species[specie],
                    "coords": map_plots
                }

            return  jsonify({'species_data': species_data})
        
        except Exception as e:
            # Add general error handling
            return jsonify({'error':'An error occurred: str(e)'})
    

if __name__ == "__main__":
    app.run(debug=True)
