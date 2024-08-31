# Defining Imports
from Modules.tts import tts
from Modules.bing_images import fetch_bing_images
from Modules.geocode import geocode
from Modules.responses import narrate

def main() -> None:

    print(narrate("Saraca Asoca", "Western Ghats"))


if __name__ == "__main__":

    main()
