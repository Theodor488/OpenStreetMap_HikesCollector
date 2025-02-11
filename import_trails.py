import json
import pyodbc
from geopy.distance import geodesic


with open("export.geojson", "r") as file:
    data = json.load(file)
print(json.dumps(data["type"]))
