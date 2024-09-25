from geopy.geocoders import Nominatim

def coords(address: str) -> list[float]:

    geolocator = Nominatim(user_agent="The-Virtual-Sanctuary")
    location = geolocator.geocode(address)

    return [location.longitude, location.latitude]

def main():

    print(coords('Thane'))

if __name__ == "__main__":

    main()