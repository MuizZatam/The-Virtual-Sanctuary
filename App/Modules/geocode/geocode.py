from geopy.geocoders import Nominatim
from math import cos, radians

def geocode(address: str, radius: int = 10) -> list | str:

    geolocator = Nominatim(user_agent="narrate-life")
    location = geolocator.geocode(address)

    if location:
        
        latitude, longitude = location.latitude, location.longitude
        
        radius_deg = radius / 111 # Assuming 1 degree to approximately 111 km

        min_lat = latitude - radius_deg
        max_lat = latitude + radius_deg
        min_lon = longitude - radius_deg / cos(radians(latitude))
        max_lon = longitude + radius_deg / cos(radians(latitude))

        return [min_lat, max_lat, min_lon, max_lon]
    
    else:

        return "Address not documented"