import folium, pandas as pd
from math import radians, sin, cos, sqrt, atan2
import numpy as np
import pandas as pd

map_center = [27.165862605978425, 31.164374416309347]

hubs = [(30.08635694111855, 26.11838449777327),
        (27.024200593372797, 28.037788768125484),
        (27.66189028663055, 30.651920298481837),
        (30.00279539433303, 28.46819886036796)]

restircted_coordinates = [(29.409974444139348, 27.15493376332929 ), 
                          (27.74947541281428, 27.041311065800567), 
                          (27.842808013450828, 29.7114444577256), 
                          (29.3604724221642, 29.69521264379293)]



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

def find_intersection(m1, b1, m2, b2):
    # Calculate x coordinate of the intersection
    x_intersect = (b2 - b1) / (m1 - m2)

    # Calculate y coordinate using either equation
    y_intersect = m1 * x_intersect + b1

    return x_intersect, y_intersect


equation_res = equation_of_line(restircted_coordinates)
equation_hub = equation_of_line(hubs)
row = []
dist_mat = []
comb_coord  = hubs + restircted_coordinates
for i in range(len(comb_coord)):
    lat1, lon1 = comb_coord[i]
    for j in range(len(comb_coord)):
        lat2, lon2 = comb_coord[j]
        row.append(haversine(lat1, lon1, lat2, lon2))
    
    dist_mat.append(row)
    row =[]

print(dist_mat)

def dijkastra(distance_matrix, start_point, end_point, points):
    lstpoint = points[int(start_point)]
    points.remove(points[int(start_point)])
    points = [lstpoint] + points
    pts = [i for i in range(0, len(distance_matrix))]
    N = len(pts)
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
    
    P = end_point
    route = []
    while P != 0:
        print(previous_vertex)
        P = previous_vertex[int(P)]
        route.append(P)
    
    shortest_route = route[::-1]
    shortest_route.append(end_point)
    shortest_dist = shortest_distance[int(end_point)]

    return shortest_dist, shortest_route

shortest_distance, shortest_route = dijkastra(dist_mat, 0, 1, ['A', 'B', 'C', 'D'])

print(shortest_distance, shortest_route)
equation_hub = []

for coord in shortest_route:
    equation_hub.append(comb_coord[coord])

print(equation_hub)

equation_hub = equation_of_line(equation_hub)

print(equation_hub)

x_range = [29.409974444139348, 27.74947541281428, 27.842808013450828, 29.3604724221642]

my_map_res = folium.Map(location=map_center, zoom_start=6)


for coord in hubs:
     folium.Marker(location=coord, popup='Point').add_to(my_map_res)

for coord in restircted_coordinates:
     folium.Marker(location=coord, popup='Point').add_to(my_map_res)

folium.PolyLine(locations = restircted_coordinates + [restircted_coordinates[0]], color='red').add_to(my_map_res)

my_map_res.save("test_map_with_restricted_areas.html")

inf = float('inf')
int_coord = []
c = 0
for eq in equation_hub:
    m1, b1 = eq
    i = 0
    for res in equation_res:
        m2, b2 = res
        x_intersect, y_intersect = find_intersection(m1, b1, m2, b2)
        int_coord.append((x_intersect, y_intersect))
        print(x_intersect, y_intersect, i)
        if i != len(x_range)-1:
            if (x_intersect >= x_range[i] and x_intersect <= x_range[i+1]) or (x_intersect <= x_range[i] and x_intersect >= x_range[i+1]):
                dist_mat[equation_hub.index(eq)][len(equation_hub) + equation_res.index(res)] = inf  #index need revision
                dist_mat[len(equation_hub) + equation_res.index(res)][equation_hub.index(eq)] = inf
                c += 1
        else:
            if (x_intersect >= x_range[i] and x_intersect <= x_range[0]) or (x_intersect <= x_range[i] and x_intersect >= x_range[0]):
                dist_mat[equation_hub.index(eq)][len(equation_hub) + equation_res.index(res)] = inf
                dist_mat[len(equation_hub) + equation_res.index(res)][equation_hub.index(eq)] = inf
                c += 1
        i += 1


print(dist_mat)

i = 1
for coord in int_coord:
     folium.Marker(location=coord, popup=f"Res{i}").add_to(my_map_res)
     i += 1

my_map_res.save("test_map_with_restricted_areas.html")

print(c)
