import json
import pyodbc
import requests
from geopy.distance import geodesic

trails_list = []
MAX_LENGTH_MILES = 10 # Filter out all hikes more than 15 miles long

with open("export2.geojson", "r") as file:
    data = json.load(file)

# Parse out trail data
def get_elevation(lat, lon):
    url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    response = requests.get(url).text
    trailhead_elevation = json.loads(response)["elevation"][0]
    return trailhead_elevation

def get_coordinates(data, trail_idx, curr_trail_dict, node_idx):
    trail_point = data["features"][trail_idx]["geometry"]["coordinates"][node_idx]
        # Check if 'trailhead' contains multiple coordinates (nested list)
    if isinstance(trail_point[0], list):
        trail_point = trail_point[0]
    trail_point = [trail_point[1], trail_point[0]]
    return trail_point

def get_trail_length_miles(trailhead, length_miles, coordinates):
    if isinstance(trailhead[0], list):
        coordinates = coordinates[0]

    for i in range(1, len(coordinates)):
        lat_1 = (coordinates[i-1][1])
        lon_1 = (coordinates[i-1][0])
        lat_2 = (coordinates[i][1])
        lon_2 = (coordinates[i][0])
        length_miles += geodesic((lat_1, lon_1), (lat_2, lon_2)).miles
    return length_miles

def meters_to_feet(meters):
    return meters * 3.28084

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
        lat_1 = (coordinates[i-1][1])
        lon_1 = (coordinates[i-1][0])
        lat_2 = (coordinates[i][1])
        lon_2 = (coordinates[i][0])
        elevation_1 = get_elevation(lat_1, lon_1)
        elevation_2 = get_elevation(lat_2, lon_2)
        if elevation_2 > elevation_1:
            elevation_gain += (elevation_2 - elevation_1)
    return elevation_gain

for i in range(len(data["features"])):

    curr_trail_dict = {}
    name = json.dumps(data["features"][i]["properties"].get("name", "Unknown"))

    # Check if trail name exists
    if name != '"Unknown"':

        #length_miles
        length_miles = 0
        coordinates = data["features"][i]["geometry"]["coordinates"]
        trailhead = data["features"][i]["geometry"]["coordinates"][0]
        length_miles = round(get_trail_length_miles(trailhead, length_miles, coordinates), 2)

        # Ignore all trails that are longer than MAX_LENGTH_MILES
        if length_miles > MAX_LENGTH_MILES:
            continue

        # Name
        curr_trail_dict["name"] = name
        print(f"{i}. {name}")

        #length_miles
        curr_trail_dict["length_miles"] = length_miles
        print(f"{length_miles}: length_miles")

        #geometry
        geometry = data["features"][i]["geometry"]
        curr_trail_dict["geometry"] = geometry

        # trailhead_lat / trailhead_lon
        trailhead = get_coordinates(data, i, curr_trail_dict, -1)
        curr_trail_dict["trailhead_lat"] = trailhead[0]
        curr_trail_dict["trailhead_lon"] = trailhead[1]
        print(f"{trailhead}: trailhead")

        # trailend_lat / trailend_lon
        trailend = get_coordinates(data, i, curr_trail_dict, 0)
        curr_trail_dict["trailend_lat"] = trailend[0]
        curr_trail_dict["trailend_lon"] = trailend[1]
        print(f"{trailend}: trailend")

        #trailhead_elevation
        lat = curr_trail_dict["trailhead_lat"]
        lon = curr_trail_dict["trailhead_lon"]
        trailhead_elevation = round(meters_to_feet(get_elevation(lat, lon)), 0)
        curr_trail_dict["trailhead_elevation"] = trailhead_elevation
        print(f"{trailhead_elevation}: trailhead_elevation")

        #trailend_elevation
        lat = curr_trail_dict["trailend_lat"]
        lon = curr_trail_dict["trailend_lon"]
        trailend_elevation = round(meters_to_feet(get_elevation(lat, lon)), 0)
        curr_trail_dict["trailend_elevation"] = trailend_elevation
        print(f"{trailend_elevation}: trailend_elevation")

        #elevation_gain_ft
        elevations = get_elevations(trailhead, coordinates)

        elevation_gain_ft = get_elevation_gain(elevations)
        elevation_gain_ft = meters_to_feet(elevation_gain_ft) # fix this. not high enough
        curr_trail_dict["elevation_gain_ft"] = elevation_gain_ft
        print(f"{elevation_gain_ft}: elevation_gain_ft")

        trails_list.append(curr_trail_dict)
    
print("e")


