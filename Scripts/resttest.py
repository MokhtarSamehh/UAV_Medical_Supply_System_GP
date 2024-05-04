import numpy as np
import pandas as pd
import math, folium

def is_number(element):
    return isinstance(element, (int, float)) and not math.isnan(element)

restricted = pd.read_excel("Prohibited flying areas.xlsx", sheet_name='Sheet1').values.tolist()
# print(restricted)
# restricted_col = restricted.select_dtypes(include='number').columns

rest = []

for column in restricted:
    if is_number(column[1]):
        rest.append(column)


map_center = [27.165862605978425, 31.164374416309347]
my_map_res = folium.Map(location=map_center, zoom_start=6)

for res in rest:
    restricted_coordinates = []
    coordinates_list = []
    for coord in res:
        # print(is_number(coord))
        if is_number(coord):
            restricted_coordinates.append(coord)
    coordinates_list = [(restricted_coordinates[i], restricted_coordinates[i+1]) for i in range(0, len(restricted_coordinates), 2)]
    print(coordinates_list)
    folium.PolyLine(locations = coordinates_list + [coordinates_list[0]], color='red').add_to(my_map_res)

my_map_res.save("restricted_areas_test.html")
