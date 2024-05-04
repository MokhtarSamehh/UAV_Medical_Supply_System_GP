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
# distance_matrix = np.array([
#      [0, 6, inf, 1, inf],
#      [6, 0,   5, 2,  2 ],
#      [inf, 5, 0, inf, 5],
#      [1, 2, inf,   0, 1],
#      [inf, 2, 5,   1, 0]
#   ])
# points = ['A', 'B', 'C', 'D', 'E']
unvisited = pts
visited = []
lst = [0] + [np.inf for i in range(N-1)]
shortest_distance = np.array(lst)
previous_vertex = np.empty_like(pts, dtype=object)
# print(previous_vertex)
k = 0
Q = 0
c = 0
print(shortest_distance)
print(previous_vertex)
# print(distance_matrix)
print(unvisited)
for i in range(N):
    for j in unvisited:
        if shortest_distance[j] > distance_matrix[k][j] + shortest_distance[k]:
            shortest_distance[j] = distance_matrix[k][j] + shortest_distance[k]
            # print(points[k])
            c += 1
            # print(k)
            previous_vertex[j] = k
            # print(previous_vertex)
            print(shortest_distance)
    # print(len(visited), len(points))
    unvisited.remove(k)
    print(unvisited)
    visited.append(k)
    print(visited)
    if len(visited) == N:
        Q = 1
        break
   
    k = unvisited[np.argmin(shortest_distance[unvisited])]
    # print(k)
    # print(visited)
    # print(unvisited)
    # print(shortest_distance)
    # print(previous_vertex)

print(N, Q, c)
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

