import folium
import pandas as pd
from itertools import chain
# Create a folium map centered at a specific location
map_center = [27.165862605978425, 31.164374416309347]
my_map = folium.Map(location=map_center, zoom_start=6)
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

my_map_res = folium.Map(location=map_center, zoom_start=6)

restircted_coordinates = [(29.409974444139348, 27.15493376332929 ), 
                          (27.74947541281428, 27.041311065800567), 
                          (27.842808013450828, 29.7114444577256), 
                          (29.3604724221642, 29.69521264379293)]

for coord in restircted_coordinates:
     folium.Marker(location=coord, popup='Point').add_to(my_map_res)

folium.PolyLine(locations = restircted_coordinates + [restircted_coordinates[0]], color='red').add_to(my_map_res)

my_map_res.save("map_with_restricted_areas.html")
#
#
#
#