from flask import Flask, render_template, request
from Modules.bing_images import fetch_bing_images
from Modules.api import API_response
from Modules.gemini import narrate

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location = request.form.get("location")
        if location:
            species = API_response(location)
            narrations = narrate(species, location).split("\n--\n")
            species_data = []
            for specie in species:
                images_list = fetch_bing_images(specie)  # Fetch multiple images
                
                try:
                    narration = narrations.pop(0)
                    species_data.append((images_list, narration))

                except IndexError:

                    pass
            
            return render_template("index.html", species_data=species_data)
        else:
            return render_template("index.html", error="Unfortunately, we don't have that address documented :(")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
