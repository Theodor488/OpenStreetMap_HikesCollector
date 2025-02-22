from geopy.distance import geodesic
import geopy.distance

def get_coordinates(data, trail_idx, curr_trail_dict, node_idx):
    trail_point = data["features"][trail_idx]["geometry"]["coordinates"][node_idx]
        # Check if 'trailhead' contains multiple coordinates (nested list)
    if isinstance(trail_point[0], list):
        trail_point = trail_point[0]
    trail_point = [trail_point[1], trail_point[0]]
    return trail_point

def is_loop(lat_start, lon_start, lat_end, lon_end):
    coords_start = (lat_start, lon_start)
    coords_end = (lat_end, lon_end)
    start_to_end_distance = geopy.distance.geodesic(coords_start, coords_end).mi

    # If trailhead is within 1/4 mile of trailend then it's a loop
    if start_to_end_distance < 0.25:
        return True
    return False

def get_trail_length_miles(trailhead, length_miles, coordinates, curr_trail_dict):
    if isinstance(trailhead[0], list):
        coordinates = coordinates[0]

    for i in range(1, len(coordinates)):
        lat_1 = (coordinates[i-1][1])
        lon_1 = (coordinates[i-1][0])
        lat_2 = (coordinates[i][1])
        lon_2 = (coordinates[i][0])
        length_miles += geodesic((lat_1, lon_1), (lat_2, lon_2)).miles
    
    if is_loop(lat_1, lon_1, lat_2, lon_2):
        length_miles *= 2
        curr_trail_dict["is_loop"] = "True"
    else:
        curr_trail_dict["is_loop"] = "False"
    return length_miles

def meters_to_feet(meters):
    return meters * 3.28084
