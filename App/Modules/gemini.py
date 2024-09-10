import google.generativeai as genai
from dotenv import load_dotenv
from os import environ

load_dotenv()
genai.configure(api_key=environ["API"])
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def narrate(species: list[str], location: str) -> str:

    response = model.generate_content(

        f"You are David Attenborough, providing a documentary-style narration in his style of speech about the list of following species - {species} found at {location}, explain the species' role and importance within its native ecosystem. Use the common name for the specified species in narration even if the given species is in scientific name. Offer details on the population status, including any relevant conservation data. Describe intriguing or amusing aspect of the species' life. Note any unique significance the species might have, whether to the ecosystem, culture, or human history. With all that being said, do not provide any ambiguous information. Do not provide any additional context such as background tone or what your name or role is or any clarifications. Stick to the request only. Use a simple markdown format with the common name as the heading and rest all content as simple paragraphs with no headings. In the end, create a seperate section to describe how these species behave in a food chain altogether - use the title 'Food Chain' for this section specifically. Use '--' to denote end of a section (be it a specie section or be it the foodchain). Each section should be around 3 minutes of narration."
    )
    return response.text

def main():

    print(narrate(["Falcon", "Kangaroo", "Monitor Lizard", "Koala"], "Australia"))

if __name__ == "__main__":

    main()