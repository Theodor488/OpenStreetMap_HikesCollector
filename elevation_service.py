import json
import pyodbc
import requests
from geopy.distance import geodesic
import geopy.distance

from trail_utils import meters_to_feet

# Parse out trail data
def get_elevation(lat, lon):
    url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    response = requests.get(url).text
    trailhead_elevation = json.loads(response)["elevation"][0]
    return trailhead_elevation

def get_elevations(trailhead, coordinates):
    elevations = []
    if isinstance(trailhead[0], list):
        coordinates = coordinates[0]
    
    coordinates = coordinates[::-1]

    for i in range(1, len(coordinates), 10):
        lat = (coordinates[i][1])
        lon = (coordinates[i][0])
        elevation = get_elevation(lat, lon)
        elevations.append(meters_to_feet(elevation))

    return elevations

def get_elevation_gain(elevations):
    elevation_gain = 0

    for i in range(1, len(elevations)):
        elevation_1 = elevations[i-1]
        elevation_2 = elevations[i]
        if elevation_2 > elevation_1:
            elevation_gain += (elevation_2 - elevation_1)
    return round(elevation_gain, 2)



