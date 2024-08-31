# Defining Imports
from Modules.bing_images import fetch_bing_images
from Modules.responses import narrate
from Modules.api import API_response
import streamlit as st


def main() -> None:

    st.set_page_config(layout="wide")
    st.title("The Virtual Sanctuary")

    location = st.text_input("Enter a location: ")

    if location:

        species = API_response(location)

        for specie in species:

            images_list = fetch_bing_images(specie)
            narration = narrate(specie)

            st.image(images_list, width = 400)

            st.markdown(narration)

            st.html("</br></br></br>")


if __name__ == "__main__":

    main()
