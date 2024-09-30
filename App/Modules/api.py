import aiohttp
import asyncio
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

async def fetch_wikipedia(session, species):
    wiki_url = f"https://en.wikipedia.org/wiki/{species.replace(' ', '_')}"
    try:
        async with session.get(wiki_url) as wiki_response:
            if wiki_response.status == 200:
                soup = BeautifulSoup(await wiki_response.text(), 'html.parser')
                paragraphs = soup.find_all('p')
                for p in paragraphs:
                    if p.find('b'):
                        summary = re.sub(r'\[\d+\]', '', p.text)
                        sentences = summary.split('. ')[:3]
                        return '. '.join(sentences) + '.'
    except Exception as e:
        print(f"Error fetching Wikipedia data: {e}")
    return "No Wikipedia summary found"

async def fetch_inaturalist(session, species):
    inaturalist_url = f"https://api.inaturalist.org/v1/taxa?q={species}"
    try:
        async with session.get(inaturalist_url) as inat_response:
            if inat_response.status == 200:
                inat_data = await inat_response.json()
                if inat_data['results']:
                    result = inat_data['results'][0]
                    return {
                        'name': result.get('preferred_common_name', species),
                        'scientific_name': result.get('name', 'N/A'),
                        'observations_count': result.get('observations_count', 'N/A'),
                        'conservation_status': result.get('conservation_status', {}).get('status', 'N/A'),
                        'wikipedia_url': result.get('wikipedia_url', 'N/A')
                    }
    except Exception as e:
        print(f"Error fetching iNaturalist data: {e}")
    return "No iNaturalist data found"

async def fetch_audio(session, species):
    xeno_canto_url = f"https://www.xeno-canto.org/api/2/recordings?query={species}"
    audio_list = []
    try:
        async with session.get(xeno_canto_url) as xc_response:
            if xc_response.status == 200:
                xc_data = await xc_response.json()
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
                    audio_list.append(audio_data)
    except Exception as e:
        print(f"Error fetching Xeno-canto data: {e}")
    return audio_list

async def fetch_species_data(session, species):
    tasks = [
        fetch_wikipedia(session, species),
        fetch_inaturalist(session, species),
        fetch_audio(session, species)
    ]
    wikipedia_summary, inaturalist_data, audio_data = await asyncio.gather(*tasks)

    return {
        "wikipedia": wikipedia_summary,
        "inaturalist": inaturalist_data,
        "audio": audio_data
    }

async def fetch_gbif_data(min_lat, max_lat, min_lon, max_lon, n=8):
    gbif_url = "https://api.gbif.org/v1/occurrence/search"
    params = {
        'decimalLatitude': f'{min_lat},{max_lat}',
        'decimalLongitude': f'{min_lon},{max_lon}',
        'hasCoordinate': 'true',
        'hasGeospatialIssue': 'false',
        'limit': 300,
        'mediaType': 'StillImage'
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(gbif_url, params=params) as response:
            if response.status == 200:
                results = await response.json()
                excluded_groups = {
                    'Fungi', 'Bacteria', 'Protista', 'Insecta', 'Arachnida', 
                    'Mollusca', 'Annelida', 'Nematoda', 'Platyhelminthes', 
                    'Plankton', 'Cestoda', 'Trematoda', 'Gastropoda', 'Bivalvia'
                }

                species_data = {}
                tasks = []
                for result in results.get('results', []):
                    taxon_class = result.get('class')
                    if 'species' in result and taxon_class not in excluded_groups:
                        species_name = result['species']
                        media = result.get('media', [])
                        media_urls = [m['identifier'] for m in media if 'identifier' in m]

                        if media_urls and species_name not in species_data:
                            tasks.append(fetch_species_data(session, species_name))

                            species_data[species_name] = {
                                "images": media_urls,
                            }

                        if len(species_data) == n:
                            break
                
                if tasks:
                    additional_data = await asyncio.gather(*tasks)
                    for species_name, data in zip(species_data.keys(), additional_data):
                        species_data[species_name].update(data)

                return species_data

async def API_Response(address: str, n: int = 8) -> dict:
    geo_data = geocode(address)
    if not geo_data:
        return {"error": "Address not documented"}

    (min_lat, max_lat, min_lon, max_lon), map_plots = geo_data

    species_data = await fetch_gbif_data(min_lat, max_lat, min_lon, max_lon, n)
    return {
        "species_data": species_data,
        "coords": map_plots
    }

def main():
    address = input("Enter the address: ")
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(API_Response(address))
    
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

if __name__ == "__main__":
    main()
