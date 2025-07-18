import folium, pandas as pd
from math import radians, sin, cos, sqrt, atan2

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
hubs = pd.read_excel("blood banks 30 km.xlsx", sheet_name='Sheet1', header=None, usecols='A', skiprows=[0])
lat = pd.read_excel("blood banks 30 km.xlsx", sheet_name='Sheet1', header=None, usecols='H', skiprows=[0])
lon = pd.read_excel("blood banks 30 km.xlsx", sheet_name='Sheet1', header=None, usecols='J', skiprows=[0])
hublist = hubs.values.tolist()
latlist = lat.values.tolist()
lonlist = lon.values.tolist()
# print(latlist)
# start_point = input('Enter Start Point:')   #Here you Enter where you want your start point
# lsthub = hublist[int(start_point)]
# lstlat = latlist[int(start_point)]
# lstlon = lonlist[int(start_point)]
# hublist.remove(lsthub)
# latlist.remove(lstlat)
# lonlist.remove(lstlon)
# hublist = [lsthub] + hublist
# latlist = [lstlat] + latlist
# lonlist = [lstlon] + lonlist
# print(hublist)
distmat = []

for index in range(len(latlist)):
    lat1 = latlist[index][0]
    lon1 = lonlist[index][0]
    row = []

    for index2 in range(len(latlist)):
        lat2 = latlist[index2][0]
        lon2 = lonlist[index2][0]

        distance = haversine(lat1, lon1, lat2, lon2)

        row.append(distance)

    distmat.append(row)



print(distmat)
exportdistmat = pd.DataFrame(distmat)
exportdistmat.to_csv("result.csv", index=hublist, header=hublist)

