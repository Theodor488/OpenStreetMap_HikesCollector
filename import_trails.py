import json
import pyodbc
import requests
from geopy.distance import geodesic

trails_list = []

with open("export2.geojson", "r") as file:
    data = json.load(file)

# Parse out trail data
for i in range(len(data["features"])):

    curr_trail_dict = {}
    name = json.dumps(data["features"][i]["properties"].get("name", "Unknown"))

    # Check if trail name exists
    if name != '"Unknown"':
        # Name
        print(f"{i}. {name}")
        curr_trail_dict["name"] = name

        # trailhead_lat / trailhead_lon
        trailhead = data["features"][i]["geometry"]["coordinates"][0]
        # Check if 'trailhead' contains multiple corrdinates (nested list)
        if isinstance(trailhead[0], list):
            trailhead = trailhead[0]
        curr_trail_dict["trailhead_lat"] = trailhead[0]
        curr_trail_dict["trailhead_lon"] = trailhead[1]
        print(trailhead)

        #elevation_gain_ft
        elevation_gain_ft = 0
        curr_trail_dict["elevation_gain_ft"] = elevation_gain_ft

        #min_elevation_ft
        min_elevation_ft = 0
        curr_trail_dict["min_elevation_ft"] = min_elevation_ft

        trailhead_elevation = 0
        lat = curr_trail_dict["trailhead_lat"]
        lon = curr_trail_dict["trailhead_lon"]
        url = f"https://api.open-meteo.com/v1/elevation?latitude={lon}&longitude={lat}"
        response = requests.get(url).text
        elevation = json.loads(response)["elevation"][0]

        #max_elevation_ft
        max_elevation_ft = 0
        curr_trail_dict["max_elevation_ft"] = max_elevation_ft

        #geometry
        geometry = data["features"][i]["geometry"]
        curr_trail_dict["geometry"] = geometry

        #length_miles
        length_miles = 0

        coordinates = data["features"][i]["geometry"]["coordinates"]

        trailhead = data["features"][i]["geometry"]["coordinates"][0]
        if isinstance(trailhead[0], list):
            coordinates = coordinates[0]

        for i in range(1, len(coordinates)):
            lat_1 = (coordinates[i-1][1])
            lon_1 = (coordinates[i-1][0])
            lat_2 = (coordinates[i][1])
            lon_2 = (coordinates[i][0])
            length_miles += geodesic((lat_1, lon_1), (lat_2, lon_2)).miles

        curr_trail_dict["length_miles"] = round(length_miles, 2)

        trails_list.append(curr_trail_dict)
    
print("e")


