import requests
import random
from geopy.geocoders import Nominatim
from math import cos, radians


def geocode(address: str, length: int = 30) -> list | str:
    geolocator = Nominatim(user_agent="The-Virtual-Sanctuary")
    location = geolocator.geocode(address)

    if location:
        latitude, longitude = location.latitude, location.longitude
        radius_deg = length / 111  # Convert length in km to degrees

        min_lat = latitude - radius_deg
        max_lat = latitude + radius_deg
        min_lon = longitude - radius_deg / cos(radians(latitude))
        max_lon = longitude + radius_deg / cos(radians(latitude))

        return [min_lat, max_lat, min_lon, max_lon]
    
    else:
        return "Address not documented"


def select(species_with_media: list, n: int = 10) -> list:
    """
    Select `n` species randomly from the list, ensuring they have media associated.
    """
    if len(species_with_media) <= n:
        return species_with_media  # If less than or equal to `n` species with media, return all

    return random.sample(species_with_media, n)  # Randomly select `n` species with media


def API_response(address: str, n: int = 15) -> dict:
    """
    Retrieves species data based on the geolocation and returns a dictionary 
    where keys are species names and values are lists of media URLs.
    """
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
        'limit': 100  # Increase limit to get more results for species
    }

    response = requests.get(gbif_url, params=params)
    results = response.json()

    excluded_groups = [
        'Fungi', 'Bacteria', 'Protista', 'Insecta', 'Arachnida', 'Mollusca', 
        'Annelida', 'Nematoda', 'Platyhelminthes', 'Plankton', 'Cestoda', 
        'Trematoda', 'Gastropoda', 'Bivalvia'
    ]

    species_media_dict = {}

    for result in results.get('results', []):
        taxon_class = result.get('class')
        if 'species' in result and taxon_class not in excluded_groups:
            species_name = result['species']

            # Fetch media data if available
            media = result.get('media', [])
            media_urls = [m['identifier'] for m in media if 'identifier' in m]

            if media_urls:  # Only add species if it has associated media
                species_media_dict[species_name] = media_urls

    return species_media_dict



def main():
    address = input("Enter the address: ")
    species_with_media = API_response(address)
    
    if species_with_media:
        
        print(species_with_media)
    else:
        print("No species with media found or address not documented.")


if __name__ == "__main__":
    main()
