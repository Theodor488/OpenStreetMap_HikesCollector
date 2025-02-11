import json
import os
#import pyodbc
#from geopy.distance import geodesic
cwd = os.getcwd()

# Construct the full file path
file_path = os.path.join(cwd, 'export2.json')

print("Current Working Directory:", os.getcwd())  

with open("export2.json", "r") as file:
    data = json.load(file)
print(json.dumps(data["type"], indent=2))
