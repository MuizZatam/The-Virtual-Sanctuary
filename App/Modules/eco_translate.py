from EcoNameTranslator import to_species
from sys import argv

def convert(names: list[str]) -> dict:

    return to_species(names, sanityCorrect=True)


def main() -> None:

    print(convert(argv[1:]))


if __name__ == "__main__":

    main()