import folium, pandas as pd
from math import radians, sin, cos, sqrt, atan2
import numpy as np
import pandas as pd
from shapely.geometry import Polygon
from shapely.affinity import translate, scale



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
    return shortest_distance, previous_vertex

map_center = [27.165862605978425, 31.164374416309347]

hubs = [(30.08635694111855, 26.11838449777327),
        (27.024200593372797, 28.037788768125484),
        (27.66189028663055, 30.651920298481837),
        (30.00279539433303, 28.46819886036796)]

restircted_coordinates = [(29.409974444139348, 27.15493376332929 ), 
                          (27.74947541281428, 27.041311065800567), 
                          (27.842808013450828, 29.7114444577256), 
                          (29.3604724221642, 29.69521264379293)]

x_range = [29.409974444139348, 27.74947541281428, 27.842808013450828, 29.3604724221642]

enlarged_shape = enlarge_shape_at_centroid(restircted_coordinates, 1.1)
polygon_coordinates = list(enlarged_shape.exterior.coords)
polygon_coordinates.pop()

start = [(28.842808013450828, 30.7114444577256)]

row = []
dist_mat = []
comb = start + hubs + polygon_coordinates
comb_coord = start + hubs + polygon_coordinates

for i in range(len(comb_coord)):
    lat1, lon1 = comb_coord[i]
    for j in range(len(comb_coord)):
        lat2, lon2 = comb_coord[j]
        row.append(haversine(lat1, lon1, lat2, lon2))
    
    dist_mat.append(row)
    row =[]

equation_res = equation_of_line(restircted_coordinates)
i = 0    
int_coord = []
for m in range(len(dist_mat)):
    equation_hub = equation_of_line_from_point(comb_coord)
    # print(equation_hub)
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
            print(x_intersect, y_intersect, m, j, i,k,c,d)
            (lat, lon) = comb[m]
            # dist_mat[m][j] >= haversine(lat,lon,x_intersect,y_intersect):
            if i != len(x_range) - 1 :  # and 
                if ((x_intersect > x_range[i] and x_intersect < x_range[i+1]) or (x_intersect < x_range[i] and x_intersect > x_range[i+1])) and dist_mat[m][j] >= haversine(lat,lon,x_intersect,y_intersect):
                    dist_mat[m][j] = inf
                    dist_mat[j][m] = inf                    
                    # print(dist_mat, x_intersect, y_intersect, m, j)
                    c += 1
                    break    
                else:
                    k += 1
                    # print(dist_mat, k)
            else:
                if ((x_intersect > x_range[i] and x_intersect < x_range[0]) or (x_intersect < x_range[i] and x_intersect > x_range[0])) and dist_mat[m][j] >= haversine(lat,lon,x_intersect,y_intersect):
                    dist_mat[m][j] = inf
                    dist_mat[j][m] = inf
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

    print(dist_mat)


# shortest_dist, shortest_route = dijkastra(dist_mat,4)

# for points in shortest_route[1:]:

#     while k != N:
#         shortest_distance, shortest_route = dijkastra(dist_mat, 4)

#         print(shortest_distance, shortest_route)
#         equation_hub = []

#         for coord in shortest_route:
#             equation_hub.append(comb_coord[coord])

#         print(range(len(equation_hub)))

#         equation_hub = equation_of_line(equation_hub)

#         print(equation_hub)

#         k = 0
#         N = 0
#         i = 0
#         for eq in equation_hub:
#             m1, b1 = eq
#             j = 0
#             for res in equation_res:
#                 m2, b2 = res
#                 x_intersect, y_intersect = find_intersection(m1, b1, m2, b2)
#                 int_coord.append((x_intersect, y_intersect))
#                 N += 1
#                 if i != len(x_range)-1:
#                     if (x_intersect > x_range[j] and x_intersect < x_range[j+1]) or (x_intersect < x_range[j] and x_intersect > x_range[j+1]):
#                         dist_mat[shortest_route[i]][shortest_route[i+1]] = inf  
#                         dist_mat[shortest_route[i+1]][shortest_route[i]] = inf
#                         c += 1
#                         break    
#                     else:
#                         k += 1
#                 else:
#                     if (x_intersect > x_range[j] and x_intersect < x_range[0]) or (x_intersect < x_range[j] and x_intersect > x_range[0]):
#                         dist_mat[shortest_route[i]][shortest_route[i+1]] = inf  
#                         dist_mat[shortest_route[i+1]][shortest_route[i]] = inf
#                         d += 1
#                         break
                        
#                     else:
#                         k += 1
#                 print(x_intersect, y_intersect, i, j, N, k,c,d)
#                 j += 1       
#             i += 1

#         print(dist_mat, c)
# int_coord = []

# inf = float('inf')
# c = 0
# d = 0
# k = 0
# i = 0
# for eq in equation_hub:
#     m1, b1 = eq
#     j = 0
#     for res in equation_res:
#         m2, b2 = res
#         x_intersect, y_intersect = find_intersection(m1, b1, m2, b2)
#         int_coord.append((x_intersect, y_intersect))
#         if j != len(x_range)-1:
#             if (x_intersect > x_range[j] and x_intersect < x_range[j+1]) or (x_intersect < x_range[j] and x_intersect > x_range[j+1]):
#                 dist_mat[i][j-1] = inf  
#                 dist_mat[j-1][i] = inf
#                 c += 1
#                 break
#             else:
#                 k += 1
#         else:
#             if (x_intersect > x_range[j] and x_intersect < x_range[0]) or (x_intersect < x_range[j] and x_intersect > x_range[0]):
#                 dist_mat[i][j-1] = inf  
#                 dist_mat[j-1][i] = inf
#                 d += 1
#                 break
#             else:
#                 k += 1
#         print(x_intersect, y_intersect, i, j,k,c,d)
#         j += 1      
#     i += 1

#     print(dist_mat, c)

shortest_distance, shortest_route = dijkastra(dist_mat,4)

print(shortest_distance, shortest_route)

P = 1
end = P
route = []
while P != 0:
    P = shortest_route[int(P)]
    route.append(P)

shortest_route = route[::-1]
shortest_route.append(end)
print(shortest_route)
route_coordinates = []

for i in shortest_route:
    route_coordinates.append(comb[i])
# # print(dist_mat)



my_map_res = folium.Map(location=map_center, zoom_start=6)
i = 0
for coord in comb:
     i += 1
     folium.Marker(location=coord, popup=f"{i}").add_to(my_map_res)
# folium.Marker(location=int_coord[0], popup=f"Int{i}").add_to(my_map_res)
# j = 30
# for coord in int_coord[30:]:
#     j += 1
#     folium.Marker(location=coord, popup=f"Int{j}").add_to(my_map_res)
#     if j == 40:
#         break
folium.PolyLine(locations = restircted_coordinates + [restircted_coordinates[0]], color='red').add_to(my_map_res)
folium.PolyLine(locations=route_coordinates, color='blue').add_to(my_map_res)
my_map_res.save("test_map_with_restricted_areas_test.html")
