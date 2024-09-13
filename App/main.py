from flask import Flask, render_template, request
from Modules.api import API_response
from Modules.gemini import narrate
from Modules.coords import coords

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        location = request.form.get("location")
        
        if not location:

            return render_template("index.html", error="Unfortunately, we don't have that location documented :(")
        
        try:

            map_plots = coords(location)
            species = API_response(location)

            specie_list = list()
            narrations = list()

            for key in species.keys():

                specie_list.append(key)
            
                narrations.append(narrate(key, location))

            species_data = dict()
            for index, specie in enumerate(specie_list):
                
                species_data[specie] = {
                    "narration": narrations[index],
                    "images": species[specie],
                    "coords": map_plots
                }

            return render_template("index.html", species_data=species_data)
        
        except Exception as e:
            # Add general error handling
            return render_template("index.html", error=f"An error occurred: {str(e)}")
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
