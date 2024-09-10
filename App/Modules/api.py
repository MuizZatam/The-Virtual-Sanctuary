import requests
import random
from geopy.geocoders import Nominatim
from math import cos, radians


def geocode(address: str, length: int = 50) -> list | str:

    geolocator = Nominatim(user_agent="The-Virtual-Sanctuary")
    location = geolocator.geocode(address)

    if location:
        
        latitude, longitude = location.latitude, location.longitude
        
        radius_deg = length / 111  

        min_lat = latitude - radius_deg
        max_lat = latitude + radius_deg
        min_lon = longitude - radius_deg / cos(radians(latitude))
        max_lon = longitude + radius_deg / cos(radians(latitude))

        return [min_lat, max_lat, min_lon, max_lon]
    
    else:

        return "Address not documented"


def select(species: list, n: int = 15) -> list:

    selected = list()

    while len(selected) < n and species:

        selection = random.choice(species)

        if selection not in selected:
            selected.append(selection)

    return selected


def API_response(address: str) -> list | str:

    geo_data = geocode(address)
    if isinstance(geo_data, str):
        return None

    else:
        min_lat, max_lat, min_lon, max_lon = geo_data

    gbif_url = "https://api.gbif.org/v1/occurrence/search"

    params = {

        'decimalLatitude': f'{min_lat},{max_lat}',
        'decimalLongitude': f'{min_lon},{max_lon}',
        'hasCoordinate': 'true',
        'hasGeospatialIssue': 'false',
        'limit': 40000
    }

    response = requests.get(gbif_url, params=params)
    results = response.json()

    excluded_groups = [

        'Fungi',              # Fungi (Mushrooms, molds, etc.)
        'Bacteria',           # Bacteria (Microorganisms)
        'Protista',           # Protists (Algae, amoebas, etc.)
        'Insecta',            # Insects (Mosquitoes, ticks, etc.)
        'Arachnida',          # Arachnids (Spiders, mites, etc.)
        'Mollusca',           # Mollusks (Small snails, slugs, etc.)
        'Annelida',           # Annelids (Earthworms, leeches, etc.)
        'Nematoda',           # Nematodes (Roundworms)
        'Platyhelminthes',    # Flatworms (Parasitic worms)
        'Plankton',           # Plankton (Microscopic organisms in water)
        'Cestoda',            # Parasitic tapeworms
        'Trematoda',          # Parasitic flukes
        'Gastropoda',         # Sea snails and related species
        'Bivalvia'            # Clams, oysters, and other bivalve shellfish
    ]

    species_set = set()

    for result in results.get('results', []):
        taxon_class = result.get('class')
        if 'species' in result and taxon_class not in excluded_groups:
            species_set.add(result['species'])

    return select(list(species_set))


def main():

    address = input("Enter the address: ")
    print(API_response(address))

if __name__ == "__main__":

    main()
