import folium
import pandas as pd
from itertools import chain
# Create a folium map centered at a specific location
map_center = [30.026151240978553, 31.21121373844104]
my_map = folium.Map(location=map_center, zoom_start=22)
lat = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='H', skiprows=[0])
lon = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='J', skiprows=[0])
latlist = lat.values.tolist()
lonlist = lon.values.tolist()
lat = list(chain(*latlist))
lon = list(chain(*lonlist))
coordinates = list(zip(lat, lon))
# Add markers for each coordinate point

for coord in coordinates:
     folium.Marker(location=coord, popup='Point').add_to(my_map)

# folium.PolyLine(locations=coordinates, color='blue').add_to(my_map)

my_map.save("map_with_markers.html")
