from EcoNameTranslator import to_species

def convert(names: list[str]) -> dict:

    '''
    Converts a list of common names into a key value mapping
    of vernacular/scientific names. Per the official documentation:

    *Any Unstandardised Names To Scientific Species*

    A list of ecological names, in any format, is accepted as input. This undergoes a data-cleaning procedure (namely, removing nomenclature flags and other redundant information), after which the following actions are taken:

    1. Names that are already in a standard species format (that is, genus + species), have any spelling errors corrected and are passed back

    2. Names at higher levels of taxonomy again have any spelling mistakes corrected, and are then mapped to a list of specific species names

    3. Common names (currently, English only) are mapped to all of the scientific species names that can be described by the common name)

    Args:
        `names: list[str]`: the list of all the names to be converted
    
    Returns:
        `dict`: mapping with the key as the common name and
        a list of all the scientific names that can be described as the values
    '''

    return to_species(names, sanityCorrect=True)


def main() -> None:

    print(convert(input("Enter a Query > ")))


if __name__ == "__main__":

    main()