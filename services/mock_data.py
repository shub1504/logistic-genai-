# services/mock_data.py

"""
Hardcoded Delhi-area delivery locations and a pre-built distance matrix.
Use this when USE_MOCK=True in config.py, or when running offline.
"""

MOCK_LOCATIONS = [
    {"address": "Connaught Place, New Delhi",      "lat": 28.6315, "lng": 77.2167},
    {"address": "Lajpat Nagar, New Delhi",         "lat": 28.5700, "lng": 77.2433},
    {"address": "Saket, New Delhi",                "lat": 28.5245, "lng": 77.2066},
    {"address": "Dwarka Sector 21, New Delhi",     "lat": 28.5526, "lng": 77.0588},
    {"address": "Rohini Sector 3, New Delhi",      "lat": 28.7196, "lng": 77.1197},
]

# Approximate road distances in km between mock locations
MOCK_DISTANCE_MATRIX = {
    "Connaught Place, New Delhi": {
        "Connaught Place, New Delhi":  0,
        "Lajpat Nagar, New Delhi":     8.2,
        "Saket, New Delhi":            13.5,
        "Dwarka Sector 21, New Delhi": 22.1,
        "Rohini Sector 3, New Delhi":  18.4,
    },
    "Lajpat Nagar, New Delhi": {
        "Connaught Place, New Delhi":  8.2,
        "Lajpat Nagar, New Delhi":     0,
        "Saket, New Delhi":            6.1,
        "Dwarka Sector 21, New Delhi": 24.3,
        "Rohini Sector 3, New Delhi":  26.0,
    },
    "Saket, New Delhi": {
        "Connaught Place, New Delhi":  13.5,
        "Lajpat Nagar, New Delhi":     6.1,
        "Saket, New Delhi":            0,
        "Dwarka Sector 21, New Delhi": 18.7,
        "Rohini Sector 3, New Delhi":  30.2,
    },
    "Dwarka Sector 21, New Delhi": {
        "Connaught Place, New Delhi":  22.1,
        "Lajpat Nagar, New Delhi":     24.3,
        "Saket, New Delhi":            18.7,
        "Dwarka Sector 21, New Delhi": 0,
        "Rohini Sector 3, New Delhi":  35.5,
    },
    "Rohini Sector 3, New Delhi": {
        "Connaught Place, New Delhi":  18.4,
        "Lajpat Nagar, New Delhi":     26.0,
        "Saket, New Delhi":            30.2,
        "Dwarka Sector 21, New Delhi": 35.5,
        "Rohini Sector 3, New Delhi":  0,
    },
}


def get_mock_locations() -> list[dict]:
    return MOCK_LOCATIONS


def get_mock_matrix() -> dict[str, dict[str, float]]:
    return MOCK_DISTANCE_MATRIX