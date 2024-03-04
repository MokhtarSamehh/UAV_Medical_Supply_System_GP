import folium
# Create a folium map centered at a specific location
map_center = [30.026151240978553, 31.21121373844104]
my_map = folium.Map(location=map_center, zoom_start=22)
# Add markers for each coordinate point
coordinates = [(30.026151240978553, 31.21121373844104), (30.025501381982846, 31.247521125378718)]  # Add your coordinate points here

for coord in coordinates:
     folium.Marker(location=coord, popup='Point').add_to(my_map)

folium.PolyLine(locations=coordinates, color='blue').add_to(my_map)

my_map.save("map_with_markers.html")
