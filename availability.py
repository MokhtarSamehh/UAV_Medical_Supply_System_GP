import numpy as np
import pandas as pd
from scipy.optimize import linprog
import folium, math
from math import radians, sin, cos, sqrt, atan2
from shapely.geometry import Polygon
from shapely.affinity import translate, scale

def is_number(element):
    return isinstance(element, (int, float)) and not math.isnan(element)

def enlarge_shape_at_centroid(coordinates, scale_factor):
    # Create a shapely Polygon from the coordinates
    original_shape = Polygon(coordinates)

    # Calculate the centroid
    centroid = original_shape.centroid

    # Translate the shape to have its centroid at the origin
    translated_shape = translate(original_shape, -centroid.x, -centroid.y)

    # Scale the translated shape
    scaled_shape = scale(translated_shape, xfact=scale_factor, yfact=scale_factor)

    # Translate the scaled shape back to its original position
    enlarged_shape = translate(scaled_shape, centroid.x, centroid.y)

    return enlarged_shape

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of the Earth in kilometers (you can change it to miles if needed)
    R = 6371.0

    # Calculate the distance
    distance = R * c

    return distance

coord = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='H,J', skiprows=[0]).values.tolist()
percentage = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='R', skiprows=[0]).values.tolist()
btc = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='F', skiprows=[0]).values.tolist()
hubs = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='A', skiprows=[0]).values.tolist()
distance_matrix = pd.read_csv('result.csv').values.tolist()
distance_matrix = [row[1:] for row in distance_matrix]
max_range = 80                                            # input('Enter Maximum Range:')
availability_parameter = []
for i in range(0,len(percentage)):
    if percentage[i] >= [9] and btc[i] == ['Yes']:
        availability_parameter.append(1)
    elif percentage[i] >= [9] and btc[i] == ['No']:
        availability_parameter.append(1.5)
    elif percentage[i] >= [5] and percentage[i] < [9] and btc[i] == ['Yes']:
        availability_parameter.append(2)
    elif percentage[i] >= [5] and percentage[i] < [9] and btc[i] == ['No']:
        availability_parameter.append(2.5)
    elif percentage[i] >= [1] and percentage[i] < [5] and btc[i] == ['Yes']:
        availability_parameter.append(3)
    elif percentage[i] >= [1] and percentage[i] < [5] and btc[i] == ['No']:
        availability_parameter.append(3.5)
    elif percentage[i] >= [0.8] and percentage[i] < [1] and btc[i] == ['Yes']:
        availability_parameter.append(4)
    elif percentage[i] >= [0.8] and percentage[i] < [1] and btc[i] == ['No']:
        availability_parameter.append(4.5)
    elif percentage[i] >= [0.6] and percentage[i] < [0.8] and btc[i] == ['Yes']:
        availability_parameter.append(5)
    elif percentage[i] >= [0.6] and percentage[i] < [0.8] and btc[i] == ['No']:
        availability_parameter.append(5.5)
    elif percentage[i] >= [0.4] and percentage[i] < [0.6] and btc[i] == ['Yes']:
        availability_parameter.append(6)
    elif percentage[i] >= [0.4] and percentage[i] < [0.6] and btc[i] == ['No']:
        availability_parameter.append(6.5)
    elif percentage[i] >= [0.2] and percentage[i] < [0.4] and btc[i] == ['Yes']:
        availability_parameter.append(7)
    elif percentage[i] >= [0.2] and percentage[i] < [0.4] and btc[i] == ['No']:
        availability_parameter.append(7.5)
    elif percentage[i] >= [0.1] and percentage[i] < [0.2] and btc[i] == ['Yes']:
        availability_parameter.append(8)
    elif percentage[i] >= [0.1] and percentage[i] < [0.2] and btc[i] == ['No']:
        availability_parameter.append(8.5)
    elif percentage[i] >= [0.05] and percentage[i] < [0.1] and btc[i] == ['Yes']:
        availability_parameter.append(9)
    elif percentage[i] >= [0.05] and percentage[i] < [0.1] and btc[i] == ['No']:
        availability_parameter.append(9.5)
    elif percentage[i] >= [0] and percentage[i] < [0.05] and btc[i] == ['Yes']:
        availability_parameter.append(9.8)
    else: 
        availability_parameter.append(10)

A = (np.array(distance_matrix) < max_range).astype(int)
B = np.ones(len(hubs))
variable_bounds = [(0,1)for _ in range(len(hubs))]
result = linprog(availability_parameter, A_ub = -A, b_ub = -B, bounds = variable_bounds, method = 'highs')
integer_result_x = result.x.astype(int) == 1
hubs = np.array(hubs)
optimal_sol = hubs[integer_result_x]

print(optimal_sol)

coordinates = [(lat,lon) for lat, lon in coord]

indices = [index for index, value in enumerate(hubs) if value in optimal_sol]

optimal_coord = [coordinates[i] for i in indices]

print(optimal_coord)


map_center = [27.165862605978425, 31.164374416309347]
my_map_sol = folium.Map(location=map_center, zoom_start=6)
i = 0
for coord in optimal_coord:
    folium.Marker(location=coord, popup=f"{optimal_sol[i]}").add_to(my_map_sol)
    i += 1


restricted = pd.read_excel("Prohibited flying areas.xlsx", sheet_name='Sheet1').values.tolist()


rest = []

for column in restricted:
    if is_number(column[1]):
        rest.append(column)



for res in rest:
    restricted_coordinates = []
    coordinates_list = []
    for coord in res:
        # print(is_number(coord))
        if is_number(coord):
            restricted_coordinates.append(coord)
    coordinates_list = [(restricted_coordinates[i], restricted_coordinates[i+1]) for i in range(0, len(restricted_coordinates), 2)]
    print(coordinates_list)
    coordinates_enlarged = enlarge_shape_at_centroid(coordinates_list, 3)
    polygon_coordinates = list(coordinates_enlarged.exterior.coords)
    polygon_coordinates.pop()
    folium.PolyLine(locations = coordinates_list + [coordinates_list[0]], color='red').add_to(my_map_sol)
    folium.PolyLine(locations = polygon_coordinates + [polygon_coordinates[0]], color='green').add_to(my_map_sol)
 



my_map_sol.save("optimal_solution.html")

# for i in range(len(comb_coord)):
#     lat1, lon1 = comb_coord[i]
#     for j in range(len(comb_coord)):
#         lat2, lon2 = comb_coord[j]
#         row.append(haversine(lat1, lon1, lat2, lon2))
    
#     dist_mat.append(row)
#     row =[]

# print(dist_mat)