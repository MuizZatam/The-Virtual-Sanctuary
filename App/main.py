# Defining Imports
from Modules.voice_tts import male, female


# Main function
def main() -> None:

    male.tts_male("Hello World! I am Ryan!")
    female.tts_female("Hello World! I am Aria!")


if __name__ == "__main__":

    main()