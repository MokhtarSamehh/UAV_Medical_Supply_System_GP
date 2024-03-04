import numpy as np
import pandas as pd
distance_matrix = pd.read_csv('result.csv').values.tolist()
points = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='A', skiprows=[0]).values.tolist()
distance_matrix = distance_matrix[1:]
points = [i for i in range(0, len(distance_matrix))]
print(distance_matrix)
print(len(distance_matrix))
inf = float('inf')
# distance_matrix = np.array([
#      [0, 6, inf, 1, inf],
#      [6, 0,   5, 2,  2 ],
#      [inf, 5, 0, inf, 5],
#      [1, 2, inf,   0, 1],
#      [inf, 2, 5,   1, 0]
#   ])
# points = ['A', 'B', 'C', 'D', 'E']
unvisited = points
unvisited_index = np.arange(0,len(points))
visited = []

lst = [0] + [np.inf for i in range(len(points)-1)]
shortest_distance = np.array(lst)
previous_vertex = np.empty_like(points, dtype=object)
# print(previous_vertex)
k = 0
# print(shortest_distance)
# print(previous_vertex)
# print(len(distance_matrix))
print(unvisited)
for i in range(len(distance_matrix)):
    for j in unvisited_index:
        if shortest_distance[j] > distance_matrix[k][j] + shortest_distance[k]:
            shortest_distance[j] = distance_matrix[k][j] + shortest_distance[k]
            previous_vertex[j] = points[k] 
            #print(previous_vertex)
            #print(shortest_distance)
    unvisited.remove(points[k])
    unvisited_index = unvisited_index[unvisited_index != k]
    #print(unvisited_index)
    visited.append(points[k])
    #print(visited)
    if len(visited) == len(points):
        break
    # print(shortest_distance[unvisited_index])
    k = unvisited_index[np.argmin(shortest_distance[unvisited_index])]
    # print(k)
    # print(visited)
    # print(unvisited)
    # print(shortest_distance)
    # print(previous_vertex)
end_point = input('Enter the End Point:')
start_point = input('Enter Start Point:')
P = end_point
route = []
while P != start_point:
    P = previous_vertex[points.index(P)]
    route.append(P)
    
shortest_route = route[::-1]
shortest_route.append(end_point)
print(shortest_route)
print(shortest_distance[points.index(end_point)])

