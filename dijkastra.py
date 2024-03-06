import numpy as np
import pandas as pd
# distance_matrix = pd.read_csv('result.csv').values.tolist()
# points = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='A', skiprows=[0]).values.tolist()
# points = [i for i in range(0, len(distance_matrix))]
# print(distance_matrix)
# print(len(distance_matrix))
inf = float('inf')
distance_matrix = np.array([
     [0, 6, inf, 1, inf],
     [6, 0,   5, 2,  2 ],
     [inf, 5, 0, inf, 5],
     [1, 2, inf,   0, 1],
     [inf, 2, 5,   1, 0]
  ])
# points = [i for i in range(0, len(distance_matrix))]
# start_point = input('Enter Start Point:')
# distance_row = distance_matrix [int(start_point)]
# distance_matrix = np.delete(distance_matrix, int(start_point), axis=0)
# distance_matrix_new = np.vstack((distance_row ,distance_matrix))
# print(start_point, distance_matrix_new)
pts = ['A', 'B', 'C', 'D', 'E']
points = ['A', 'B', 'C', 'D', 'E']
unvisited = points
unvisited_index = np.arange(0,len(points))
visited = []
lst = [0] + [np.inf for i in range(len(points)-1)]
shortest_distance = np.array(lst)
previous_vertex = np.empty_like(points, dtype=object)
k = 0
for i in range(len(distance_matrix)):
    for j in unvisited_index:
        if shortest_distance[j] > distance_matrix[k][j] + shortest_distance[k]:
            shortest_distance[j] = distance_matrix[k][j] + shortest_distance[k]
            previous_vertex[j] = pts[k] 
    unvisited.remove(pts[k])
    unvisited_index = unvisited_index[unvisited_index != k]
    visited.append(pts[k])
    print(shortest_distance)
    if len(visited) == len(pts):
        break
    k = unvisited_index[np.argmin(shortest_distance[unvisited_index])]

print(previous_vertex, shortest_distance)
end_point = input('Enter the End Point:')
start_point = input('Enter Start Point:')
P = end_point
route = []

while P != start_point:
    P = previous_vertex[pts.index(P)]
    route.append(P)
    
shortest_route = route[::-1]
shortest_route.append(end_point)
print(shortest_route)
print(shortest_distance[pts.index(end_point)])

