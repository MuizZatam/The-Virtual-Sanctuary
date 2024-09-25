import requests

def get_inaturalist_audio(scientific_name, per_page=10):
    """
    Fetch audio recordings from iNaturalist by scientific name.
    """
    url = "https://api.inaturalist.org/v1/observations"
    params = {
        'q': scientific_name,
        'media_type': 'sound',  # Only get observations with audio
        'per_page': per_page  # Limit the number of results
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        observations = response.json().get('results', [])
        audio_list = []

        for obs in observations:
            if 'sounds' in obs:
                for sound in obs['sounds']:
                    audio_list.append({
                        'id': obs['id'],
                        'species_guess': obs.get('species_guess', 'Unknown'),
                        'sound_url': sound['file_url'],
                        'place': obs.get('place_guess', 'Unknown'),
                        'date': obs.get('observed_on', 'Unknown')
                    })

        return audio_list[0].get('sound_url')
    else:
        print(f"Error: {response.status_code}")
        return None

def main():

    scientific_name = "Tamiasciurus hudsonicus" 

    print(get_inaturalist_audio(scientific_name))

    

if __name__ == "__main__":
    main()
