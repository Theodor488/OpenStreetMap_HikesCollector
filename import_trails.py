import json
import pyodbc
from geopy.distance import geodesic


with open("export2.geojson", "r") as file:
    data = json.load(file)

for i in range(len(data["features"])):
    #name = json.dumps(data["features"][i]["properties"]["name"])
    name = json.dumps(data["features"][i]["properties"].get("name", "Unknown"))
    '''
    if name == '"Unknown"':
        name = json.dumps(data["features"][i]["properties"]["@relations"][0]["reltags"].get("name"))
        alt_name = json.dumps(data["features"][i]["properties"]["@relations"][0]["reltags"].get("alt_name", "Unknown"))
        if alt_name != '"Unknown"':
            name = f"{name}: {alt_name}"
    '''

    print(f"{i}. {name}")

# get all hike names
#names = [data["name"] for data in data["features"]] 

#print(names)


# -121.49 / 47.37