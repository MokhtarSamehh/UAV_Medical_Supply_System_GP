import numpy as np
import pandas as pd
from scipy.optimize import linprog
import folium, math
from math import radians, sin, cos, sqrt, atan2
from shapely.geometry import Polygon
from shapely.affinity import translate, scale
import random
import pulp
# -*- coding: utf-8 -*-

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

def equation_of_line(coords):
    equation = []
    for i in range(len(coords)):
        if i != len(coords)-1:
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
        else:
            x1, y1 = coords[i]
            x2, y2 = coords[0]
           # Calculate the slope
        slope = (y2 - y1) / (x2 - x1)

           # Use one of the points to find the y-intercept (b)
        b = y1 - slope * x1

        equation.append([slope, b]) 
    
    return equation

def equation_of_line_from_point(coords):
    equation = []
    for i in range(len(coords)-1):
        if i != len(coords)-1:
            x1, y1 = coords[0]
            x2, y2 = coords[i + 1]

           # Calculate the slope
        if x2 - x1 == 0:
            slope = 0
        else:
            slope = (y2 - y1) / (x2 - x1)
           # Use one of the points to find the y-intercept (b)
        b = y1 - slope * x1
        
        equation.append([slope, b]) 
    
    return equation

def find_intersection(m1, b1, m2, b2):
    # Calculate x coordinate of the intersection
    if m1 == m2: # if two lines are parallel or colinear
        x_intersect = 0
        y_intersect = 0
    else:
        x_intersect = (b2 - b1) / (m1 - m2)

        # Calculate y coordinate using either equation
        y_intersect = m1 * x_intersect + b1

    return x_intersect, y_intersect

def dijkastra(distance_matrix, hubs_number):
    # lstpoint = points[int(start_point)]
    # points.remove(points[int(start_point)])
    # points = [lstpoint] + points
    pts = [i for i in range(0, len(distance_matrix))]
    N = len(pts)
    ind = [i for i in range(0,N)]
    inf = float('inf')
    unvisited = pts
    visited = []
    lst = [0] + [np.inf for i in range(N-1)]
    shortest_distance = np.array(lst)
    previous_vertex = np.empty_like(pts, dtype=object)
    k = 0
    for i in range(N):
        for j in unvisited:
            if shortest_distance[j] > distance_matrix[k][j] + shortest_distance[k]:
                shortest_distance[j] = distance_matrix[k][j] + shortest_distance[k]
                previous_vertex[j] = k
        unvisited.remove(k)
        visited.append(k)
        if len(visited) == N:
            break
   
        k = unvisited[np.argmin(shortest_distance[unvisited])]
    
    P = ind[np.argmin(shortest_distance[1:hubs_number]) + 1]
    route = []
    while P != 0:
        P = previous_vertex[int(P)]
        route.append(P)
    
    shortest_dist = shortest_distance[np.argmin(shortest_distance[1:hubs_number]) + 1]
    shortest_route = route[::-1]
    shortest_route.append(ind[np.argmin(shortest_distance[1:hubs_number]) + 1])
    return shortest_distance, previous_vertex, shortest_dist, shortest_route

coord = pd.read_excel("blood banks with virtual hubs 80 km.xlsx", sheet_name='Sheet1', header=None, usecols='H,J', skiprows=[0]).values.tolist()
percentage = pd.read_excel("blood banks with virtual hubs 80 km.xlsx", sheet_name='Sheet1', header=None, usecols='R', skiprows=[0]).values.tolist()
btc = pd.read_excel("blood banks with virtual hubs 80 km.xlsx", sheet_name='Sheet1', header=None, usecols='F', skiprows=[0]).values.tolist()
hubs = pd.read_excel("blood banks with virtual hubs 80 km.xlsx", sheet_name='Sheet1', header=None, usecols='A', skiprows=[0]).values.tolist()
distance_matrix = pd.read_csv('result.csv').values.tolist()
distance_matrix = [row[1:] for row in distance_matrix]
max_range = 80                                 # input('Enter Maximum Range:')
availability_parameter = []
print(len(percentage))
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
    elif percentage[i] > [0] and percentage[i] < [0.05] and btc[i] == ['Yes']:
        availability_parameter.append(9.8)
    elif percentage[i] > [0] and percentage[i] < [0.05] and btc[i] == ['No']:
        availability_parameter.append(9.9)
    else: 
        availability_parameter.append(10000)

A = (np.array(distance_matrix) < max_range).astype(int)
B = 2 * np.ones(len(hubs))
N_hubs = 15

VH = []
VH_B = np.ones(N_hubs)
for i in range(N_hubs,0,-1):
    Virtual_Hubs = np.zeros(len(hubs))
    Virtual_Hubs [-i] = 1
    VH.append(Virtual_Hubs)

# print(VH)
    
A [-N_hubs:] = VH
B [-N_hubs:] = VH_B
i = 0

for i in range(1,len(hubs)-N_hubs):
    A[i][i] = 0

Sum_A = [sum(sublist[:len(hubs)]) for sublist in A]
print(Sum_A)
end_routes = np.array(Sum_A) < 2
print(end_routes)
end_routes = [i for i in range(len(end_routes)) if end_routes[i] == 1]
print(end_routes)

B[end_routes] = 1

A = np.array(-A)
B = np.array(-B)
# Create a minimization problem
problem = pulp.LpProblem("Integer Programming Problem", pulp.LpMinimize)

# Define decision variables
variables = [pulp.LpVariable(f"x{i}", lowBound=0, upBound=1, cat="Integer") for i in range(1, len(hubs)+1)]  

# Add objective function
problem += pulp.lpSum(availability_parameter[i - 1] * variables[i - 1] for i in range(1, len(hubs)))

# Add constraints
for i in range(A.shape[0]):
    constraint_expr = pulp.lpSum(A[i, j] * variables[j] for j in range(A.shape[1]))
    problem += constraint_expr <= B[i]

# Solve the problem
status = problem.solve()

# Print the solution

integer_result_x =[]
for var in variables:
    integer_result_x.append(pulp.value(var))
# hubs = np.array(hubs)
print(integer_result_x)
optimal_sol = [hubs[i] for i in range(len(hubs)) if integer_result_x[i] == 1]


# print(optimal_sol)

coordinates = [(lat,lon) for lat, lon in coord]

indices = [index for index, value in enumerate(hubs) if value in optimal_sol]

optimal_coord = [coordinates[i] for i in indices]
exportA = pd.DataFrame(A)
exportA.to_csv("binary.csv")


map_center = [27.165862605978425, 31.164374416309347]
my_map_sol = folium.Map(location=map_center, zoom_start=6)


# i = 0
# for coor in coordinates:
#     # custom_icon = folium.Icon(color='gray', icon='map-marker')
#     folium.Marker(location=coor, popup=f"{i+1}").add_to(my_map_sol)
#     i += 1


# my_map_sol.save("optimal_solution.html")
i = 0

for coord in optimal_coord:
    if i >= 52-15:
        custom_icon = folium.Icon(color='green', icon='map-marker')
    else:
        custom_icon = folium.Icon(color='red', icon='map-marker')
    folium.Marker(location=coord, icon=custom_icon).add_to(my_map_sol)
    i += 1
#     folium.Circle(
#     location=coord,
#     radius= max_range * 1000,
#     color='blue',
#     fill=True,
#     fill_color='lightblue',
#     fill_opacity=0.2,
# ).add_to(my_map_sol)
index = [end for end in end_routes if end <len(hubs)-N_hubs]
index.append(114)
index.append(134)
optimal_coord_add = [coordinates[i] for i in index]
for coord in optimal_coord_add:
    custom_icon = folium.Icon(color='red', icon='map-marker')
    folium.Marker(location=coord, icon=custom_icon).add_to(my_map_sol)
    i += 1
#     folium.Circle(
#     location=coord,
#     radius= max_range * 1000,
#     color='blue',
#     fill=True,
#     fill_color='lightblue',
#     fill_opacity=0.2,
# ).add_to(my_map_sol)
    
my_map_sol.save("optimal_solution.html")

print(len(index),sum(integer_result_x))

# optimal_coord += optimal_coord_add

for idx in index:
    integer_result_x[idx] = 1
optimal_sol = [hubs[i] for i in range(len(hubs)) if integer_result_x[i] == 1]


exportA = pd.DataFrame(optimal_sol)
exportA.to_csv("hubs.csv")
print(optimal_sol)

restricted = pd.read_excel("Prohibited flying areas.xlsx", sheet_name='Sheet1').values.tolist()


rest = []

for column in restricted:
    if is_number(column[1]):
        rest.append(column)


x_range =[]
rest_area = []
rest_area_list = []
rest_area_polygon = []
for res in rest:
    restricted_coordinates = []
    coordinates_list = []
    row =[]
    for coord in res:
        # print(is_number(coord))
        if is_number(coord):
            restricted_coordinates.append(coord)
    for i in range(0, len(restricted_coordinates), 2):
        rest_area.append((restricted_coordinates[i], restricted_coordinates[i+1])) 
    coordinates_list = [(restricted_coordinates[i], restricted_coordinates[i+1]) for i in range(0, len(restricted_coordinates), 2)]
    # print(coordinates_list)
    row = [restricted_coordinates[i] for i in range(0, len(restricted_coordinates), 2)]
    x_range.append(row)
    rest_area_list.append(coordinates_list)
    coordinates_enlarged = enlarge_shape_at_centroid(coordinates_list, 2)
    polygon_coordinates = list(coordinates_enlarged.exterior.coords)
    polygon_coordinates.pop()
    rest_area_polygon.append(polygon_coordinates)
    folium.PolyLine(locations = coordinates_list + [coordinates_list[0]], color='black').add_to(my_map_sol)
    # folium.PolyLine(locations = polygon_coordinates + [polygon_coordinates[0]], color='red').add_to(my_map_sol)
 

print(len(optimal_coord))
my_map_sol.save("optimal_solution.html")

# for i in range(len(comb_coord)):
#     lat1, lon1 = comb_coord[i]
#     for j in range(len(comb_coord)):
#         lat2, lon2 = comb_coord[j]
#         row.append(haversine(lat1, lon1, lat2, lon2))
    
#     dist_mat.append(row)
#     row =[]

# print(dist_mat)
rest_area_polygon = [item for sublist in rest_area_polygon for item in sublist]

# Generate random coordinates

lower_bound = 22
upper_bound = 31.65
lat = random.uniform(lower_bound, upper_bound)

lower_bound = 25
upper_bound = 36.9
lon = random.uniform(lower_bound, upper_bound)

start_coord = (lat, lon)
start = [(lat, lon)]
print(start)
row = []
dist_mat = []
comb = start + optimal_coord + rest_area_polygon
comb_coord = start + optimal_coord + rest_area_polygon
# print(comb)
# print(rest_area_list)
for i in range(len(comb_coord)):
    lat1, lon1 = comb_coord[i]
    for j in range(len(comb_coord)):
        lat2, lon2 = comb_coord[j]
        row.append(haversine(lat1, lon1, lat2, lon2))
    
    dist_mat.append(row)
    row =[]

int_coord = []
q = 0
co = []
e = 0
# print(x_range)
for list in rest_area_list:
    # print(list)
    equation_res = equation_of_line(list)
    i = 0    
    comb_coord = comb
    for m in range(len(dist_mat)):
        equation_hub = equation_of_line_from_point(comb_coord)
        inf = float('inf')
        c = 0
        d = 0
        k = 0
        j = m + 1
        for eq in equation_hub:
            m1, b1 = eq
            i = 0
            for res in equation_res:
                m2, b2 = res
                x_intersect, y_intersect = find_intersection(m1, b1, m2, b2)
                int_coord.append((x_intersect, y_intersect))
                if m == 7:
                    co.append((x_intersect, y_intersect))
                # print(x_intersect, y_intersect, m, j, i,k,c,d)
                (lat, lon) = comb[m]
                # dist_mat[m][j] >= haversine(lat,lon,x_intersect,y_intersect):
                if i != len(x_range[q]) - 1 :  # and 
                    if ((x_intersect > x_range[q][i] and x_intersect < x_range[q][i+1]) or (x_intersect < x_range[q][i] and x_intersect > x_range[q][i+1])) and dist_mat[m][j] >= haversine(lat,lon,x_intersect,y_intersect):
                        dist_mat[m][j] = inf
                        dist_mat[j][m] = inf
                        # if m == 0 and j == 7 and e == 0 and dist_mat[m][j] == inf:
                        #     co.append((x_intersect, y_intersect))   
                        #     e += 1                 
                        # print(dist_mat, x_intersect, y_intersect, m, j)
                        c += 1
                        break    
                    else:
                        k += 1
                        # print(dist_mat, k)
                else:
                    if ((x_intersect > x_range[q][i] and x_intersect < x_range[q][0]) or (x_intersect < x_range[q][i] and x_intersect > x_range[q][0])) and dist_mat[m][j] >= haversine(lat,lon,x_intersect,y_intersect):
                        dist_mat[m][j] = inf
                        dist_mat[j][m] = inf
                        # if  m == 0 and j == 7 and e == 0 and dist_mat[m][j] == inf:
                        #     co.append((x_intersect, y_intersect))
                        #     e += 1
                        # print(dist_mat, x_intersect, y_intersect, m, j)
                        d += 1
                        break
                        
                    else:
                        k += 1
                        # print(dist_mat, k)
                # print(x_intersect, y_intersect, m, j, i,k,c,d)
                i += 1
        # print(dist_mat)
            j += 1  
        comb_coord = comb_coord[1:]     
        # print(comb_coord)
        # comb_coord = comb_coord[::-1]

        # print(dist_mat)
    q += 1
folium.Marker(location=start_coord, popup=f"Start").add_to(my_map_sol)
hubs_number = len(optimal_coord)
ind = [i for i in range(0,hubs_number)]
shortest_distance, previous_vertex, shortest_dist, shortest_route = dijkastra(dist_mat,hubs_number)
    
# print(shortest_distance, previous_vertex,comb)
i = 0
# print(co)
# for coord in co:
#     # custom_icon = folium.Icon(color='gray', icon='map-marker')
#     folium.Marker(location=coord, popup=f"{i}").add_to(my_map_sol)
#     i += 1
# my_map_sol.save("optimal_solution.html")

# Getting ALL Routes

# for i in range(1,hubs_number+1):
#     route = []
#     while i != 0 and is_number(i):
#         route.append(i)
#         i = previous_vertex[i]
#     shortest_route =  [0] + route[::-1]
#     # print(shortest_route)

#     route_coordinates = []  
#     for i in shortest_route:
#         route_coordinates.append(comb[i])
#     # print(route_coordinates)  
#     folium.PolyLine(locations=route_coordinates, color='blue').add_to(my_map_sol)


# Getting closest N hubs
    
shortest_distance, previous_vertex, shortest_dist, shortest_route = dijkastra(dist_mat,hubs_number)
route_coordinates = [] 
N = 5
shortest_ind = []
for i in range(N):
    dist = min(shortest_distance[1:hubs_number])
    min_ind = [index for index, value in enumerate(shortest_distance) if value == dist]
    shortest_ind.append(min_ind)
    shortest_distance[min_ind] = inf
    print(dist, min_ind)

shortest_ind = [item for sublist in shortest_ind for item in sublist]
print(shortest_ind)

for i in shortest_ind:
    print(i)
    route = []
    while i != 0 and is_number(i):
        route.append(i)
        i = previous_vertex[i]
    shortest_route =  [0] + route[::-1]
    print(shortest_route)

    route_coordinates = []  
    for i in shortest_route:
        route_coordinates.append(comb[i])
    print(route_coordinates)  
    folium.PolyLine(locations=route_coordinates, color='blue').add_to(my_map_sol)

shortest_distance, previous_vertex, shortest_dist, shortest_route = dijkastra(dist_mat,hubs_number)

route_coordinates = []  
for i in shortest_route:
    route_coordinates.append(comb[i])

folium.PolyLine(locations=route_coordinates, color='red').add_to(my_map_sol)
my_map_sol.save("optimal_solution.html")