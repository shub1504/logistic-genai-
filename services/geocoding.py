# services/geocoding.py

import requests
from config import MAPS_API_KEY

def geocode_address(address: str) -> dict | None:
    """
    Convert a plain-text address into lat/lng coordinates.

    Returns:
        {"address": str, "lat": float, "lng": float}
        or None if the address couldn't be resolved.
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": MAPS_API_KEY}

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "OK":
        print(f"[Geocoding] Failed for '{address}': {data['status']}")
        return None

    result = data["results"][0]
    location = result["geometry"]["location"]

    return {
        "address": result["formatted_address"],
        "lat": location["lat"],
        "lng": location["lng"],
    }


def geocode_all(addresses: list[str]) -> list[dict]:
    """
    Geocode a list of addresses, skipping any that fail.
    Returns only successfully resolved locations.
    """
    results = []
    for addr in addresses:
        geocoded = geocode_address(addr)
        if geocoded:
            results.append(geocoded)
        else:
            print(f"[Geocoding] Skipping unresolved address: {addr}")
    return results