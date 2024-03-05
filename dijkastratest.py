import numpy as np
import pandas as pd
distance_matrix = pd.read_csv('result.csv').values.tolist()
points = pd.read_excel("blood banks with virtual hubs 3.xlsx", sheet_name='Sheet1', header=None, usecols='A', skiprows=[0]).values.tolist()
# print(distance_matrix[0])
# distance_matrix = distance_matrix[1:]
points = [i for i in range(0, len(distance_matrix))]
start_point = input('Enter Start Point:')
# print(distance_matrix)
# print(len(distance_matrix))
# print(points)
N = len(points)
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
Q = 0
c = 0
# print(shortest_distance)
# print(previous_vertex)
# print(len(distance_matrix))
# print(unvisited)
for i in range(len(points)):
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
while P != start_point:
    print(previous_vertex)
    P = previous_vertex[P]
    route.append(P)
    
shortest_route = route[::-1]
shortest_route.append(end_point)
print(shortest_route)
print(shortest_distance[points.index(end_point)])

