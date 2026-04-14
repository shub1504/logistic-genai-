# services/distance_matrix.py

import requests
from config import MAPS_API_KEY

def get_distance_matrix(locations: list[dict]) -> dict[str, dict[str, float]]:
    """
    Call the Google Maps Distance Matrix API for a list of locations.

    Args:
        locations: list of {"address": str, "lat": float, "lng": float}

    Returns:
        Nested dict: {origin_address: {destination_address: distance_km}}
    """
    # Format as "lat,lng" strings for the API
    coords = [f"{loc['lat']},{loc['lng']}" for loc in locations]
    labels = [loc["address"] for loc in locations]

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins":      "|".join(coords),
        "destinations": "|".join(coords),
        "units":        "metric",
        "key":          MAPS_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "OK":
        print(f"[DistanceMatrix] API error: {data['status']}")
        return {}

    matrix = {}
    for i, row in enumerate(data["rows"]):
        origin = labels[i]
        matrix[origin] = {}
        for j, element in enumerate(row["elements"]):
            dest = labels[j]
            if element["status"] == "OK":
                # Convert metres → kilometres
                matrix[origin][dest] = element["distance"]["value"] / 1000
            else:
                matrix[origin][dest] = float("inf")

    return matrix


def get_duration_matrix(locations: list[dict]) -> dict[str, dict[str, float]]:
    """
    Same as get_distance_matrix but returns travel time in minutes
    instead of distance. Useful for time-sensitive deliveries.
    """
    coords = [f"{loc['lat']},{loc['lng']}" for loc in locations]
    labels = [loc["address"] for loc in locations]

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins":      "|".join(coords),
        "destinations": "|".join(coords),
        "units":        "metric",
        "key":          MAPS_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    matrix = {}
    for i, row in enumerate(data["rows"]):
        origin = labels[i]
        matrix[origin] = {}
        for j, element in enumerate(row["elements"]):
            dest = labels[j]
            if element["status"] == "OK":
                # Convert seconds → minutes
                matrix[origin][dest] = element["duration"]["value"] / 60
            else:
                matrix[origin][dest] = float("inf")

    return matrix