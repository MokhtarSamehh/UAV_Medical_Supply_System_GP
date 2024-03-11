import numpy as np
import pandas as pd
from scipy.optimize import linprog
import folium
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

for coord in optimal_coord:
    folium.Marker(location=coord, popup='Point').add_to(my_map_sol)

my_map_sol.save("optimal_solution.html")