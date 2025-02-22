import json
import pyodbc
import requests
from geopy.distance import geodesic
import geopy.distance

from elevation_service import *
from trail_utils import *

trails_list = []
MAX_LENGTH_MILES = 10 # Filter out all hikes more than 15 miles long

with open("export2.geojson", "r") as file:
    data = json.load(file)

for i in range(len(data["features"])):
    curr_trail_dict = {}
    name = json.dumps(data["features"][i]["properties"].get("name", "Unknown"))

    # Check if trail name exists
    if name != '"Unknown"':
        #length_miles
        length_miles = 0
        coordinates = data["features"][i]["geometry"]["coordinates"]
        trailhead = data["features"][i]["geometry"]["coordinates"][0]
        length_miles = round(get_trail_length_miles(trailhead, length_miles, coordinates, curr_trail_dict), 2)

        # Ignore all trails that are longer than MAX_LENGTH_MILES
        if length_miles > MAX_LENGTH_MILES:
            continue

        # Name
        curr_trail_dict["name"] = name
        print(f"{i}. {name}")

        #length_miles
        curr_trail_dict["length_miles"] = length_miles
        print(f"{curr_trail_dict['is_loop']}: is_loop")
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
        curr_trail_dict["elevation_gain_ft"] = elevation_gain_ft
        print(f"{elevation_gain_ft}: elevation_gain_ft")

        trails_list.append(curr_trail_dict)
    
print("e")


