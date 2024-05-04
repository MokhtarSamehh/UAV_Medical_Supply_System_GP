import numpy as np
import pandas as pd
start_point = input('Enter Start Point:')
distance_matrix = pd.read_csv('result.csv').values.tolist()
points = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='A', skiprows=[0]).values.tolist()
lstpoint = points[int(start_point)]
points.remove(points[int(start_point)])
points = [lstpoint] + points
distance_matrix = [row[1:] for row in distance_matrix]
pts = [i for i in range(0, len(distance_matrix))]
N = len(pts)
inf = float('inf')
unvisited = pts
visited = []
lst = [0] + [np.inf for i in range(N-1)]
shortest_distance = np.array(lst)
previous_vertex = np.empty_like(pts, dtype=object)
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

end_point = input('Enter the End Point:')
P = end_point
route = []
while P != 0:
    print(previous_vertex)
    P = previous_vertex[int(P)]
    route.append(P)
    
shortest_route = route[::-1]
shortest_route.append(end_point)
print(shortest_route)
print(shortest_distance[int(end_point)])