from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="theater_manager")


def get_coordinates(location):
    if not location or not location.strip():
        return None
    try:
        loc = geolocator.geocode(location)
        if loc:
            return (loc.latitude, loc.longitude)
    except Exception:
        pass
    return None