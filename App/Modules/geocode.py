from geopy.geocoders import Nominatim
from math import cos, radians

def geocode(address: str, length: int = 10) -> list | str:

    '''
    Using the Nomination function from the geopy.geocoders library,
    it returns a list of of geographical latitudes and longitudes,
    geographically describing the area in address and in a square area
    region with size length^2

    Args:
        `address: str`: The physical address needed to be converted
        `length: int = 10`: Length of the side of the area interest in Km (default 10)

    Returns:
        `list | str`: If the location is geocoded, returns the list of start and
        end latitudes and longitudes else, a generic string "Address not Documented"
        is returned
    '''

    geolocator = Nominatim(user_agent="narrate-life")
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