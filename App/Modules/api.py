import requests
from bs4 import BeautifulSoup
import re
from functools import lru_cache
from geopy.geocoders import Nominatim
from math import cos, radians

@lru_cache(maxsize=128)
def geocode(address: str, length: int = 50) -> tuple:
    geolocator = Nominatim(user_agent="The-Virtual-Sanctuary")
    location = geolocator.geocode(address)

    if location:
        latitude, longitude = location.latitude, location.longitude
        radius_deg = length / 111  # Convert length in km to degrees

        min_lat = latitude - radius_deg
        max_lat = latitude + radius_deg
        min_lon = longitude - radius_deg / cos(radians(latitude))
        max_lon = longitude + radius_deg / cos(radians(latitude))

        return ([min_lat, max_lat, min_lon, max_lon], [longitude, latitude])
    
    return None

@lru_cache(maxsize=128)
def fetch_species_data(species):
    data = {
        "wikipedia": "No Wikipedia summary found",
        "inaturalist": "No iNaturalist data found",
        "audio": []
    }

    # Fetch Wikipedia summary
    wiki_url = f"https://en.wikipedia.org/wiki/{species.replace(' ', '_')}"
    try:
        wiki_response = requests.get(wiki_url)
        wiki_response.raise_for_status()
        soup = BeautifulSoup(wiki_response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            if p.find('b'):
                summary = re.sub(r'\[\d+\]', '', p.text)
                sentences = summary.split('. ')[:3]
                data["wikipedia"] = '. '.join(sentences) + '.'
                break
    except requests.RequestException as e:
        print(f"Error fetching Wikipedia data: {e}")

    # Fetch iNaturalist data
    inaturalist_url = f"https://api.inaturalist.org/v1/taxa?q={species}"
    try:
        inat_response = requests.get(inaturalist_url)
        inat_response.raise_for_status()
        inat_data = inat_response.json()
        if inat_data['results']:
            result = inat_data['results'][0]
            data["inaturalist"] = {
                'name': result.get('preferred_common_name', species),
                'scientific_name': result.get('name', 'N/A'),
                'observations_count': result.get('observations_count', 'N/A'),
                'conservation_status': result.get('conservation_status', {}).get('status', 'N/A'),
                'wikipedia_url': result.get('wikipedia_url', 'N/A')
            }
    except requests.RequestException as e:
        print(f"Error fetching iNaturalist data: {e}")

    # Fetch audio from Xeno-canto (for birds)
    xeno_canto_url = f"https://www.xeno-canto.org/api/2/recordings?query={species}"
    try:
        xc_response = requests.get(xeno_canto_url)
        xc_response.raise_for_status()
        xc_data = xc_response.json()
        recordings = xc_data.get('recordings', [])
        for recording in recordings[:2]:  # Limit to 2 recordings
            audio_data = {
                'source': 'Xeno-canto',
                'id': recording.get('id'),
                'url': recording.get('file'),
                'recordist': recording.get('rec'),
                'country': recording.get('cnt'),
                'quality': recording.get('q')
            }
            data["audio"].append(audio_data)
    except requests.RequestException as e:
        print(f"Error fetching Xeno-canto data: {e}")

    return data

def API_Response(address: str, n: int = 8) -> dict:
    geo_data = geocode(address)
    if not geo_data:
        return {"error": "Address not documented"}

    (min_lat, max_lat, min_lon, max_lon), map_plots = geo_data

    gbif_url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        'decimalLatitude': f'{min_lat},{max_lat}',
        'decimalLongitude': f'{min_lon},{max_lon}',
        'hasCoordinate': 'true',
        'hasGeospatialIssue': 'false',
        'limit': 300,
        'mediaType': 'StillImage'
    }

    try:
        response = requests.get(gbif_url, params=params)
        response.raise_for_status()
        results = response.json()
    except requests.RequestException as e:
        return {"error": f"Error fetching GBIF data: {e}"}

    excluded_groups = {
        'Fungi', 'Bacteria', 'Protista', 'Insecta', 'Arachnida', 'Mollusca', 
        'Annelida', 'Nematoda', 'Platyhelminthes', 'Plankton', 'Cestoda', 
        'Trematoda', 'Gastropoda', 'Bivalvia'
    }

    species_data = {}

    for result in results.get('results', []):
        taxon_class = result.get('class')
        if 'species' in result and taxon_class not in excluded_groups:
            species_name = result['species']
            media = result.get('media', [])
            media_urls = [m['identifier'] for m in media if 'identifier' in m]

            if media_urls and species_name not in species_data:
                additional_data = fetch_species_data(species_name)
                species_data[species_name] = {
                    "images": media_urls,
                    "wikipedia": additional_data["wikipedia"],
                    "inaturalist": additional_data["inaturalist"],
                    "audio": additional_data["audio"]
                }

            if len(species_data) == n:
                break

    return {
        "species_data": species_data,
        "coords": map_plots
    }

def main():
    address = input("Enter the address: ")
    result = API_Response(address)
    
    if "error" in result:
        print(result["error"])
    else:
        print(f"Coordinates: {result['coords']}")
        for species, data in result['species_data'].items():
            print(f"\n{species}:")
            print(f"Wikipedia summary: {data['wikipedia']}")
            print(f"iNaturalist data: {data['inaturalist']}")
            print(f"Images: {data['images']}")
            print(f"Audio recordings:")
            for audio in data['audio']:
                print(f"  - Source: {audio['source']}")
                print(f"    ID: {audio['id']}")
                print(f"    URL: {audio['url']}")
                print(f"    Recordist: {audio['recordist']}")
                if audio['source'] == 'Xeno-canto':
                    print(f"    Country: {audio['country']}")
                    print(f"    Quality: {audio['quality']}")
                elif audio['source'] == 'Macaulay Library':
                    print(f"    Details URL: {audio['details_url']}")

if __name__ == "__main__":
    main()