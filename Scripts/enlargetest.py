from shapely.geometry import Polygon
from shapely.affinity import translate, scale
import folium, pandas as pd
from shapely.wkt import loads

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

restircted_coordinates = [(29.409974444139348, 27.15493376332929 ), 
                          (27.74947541281428, 27.041311065800567), 
                          (27.842808013450828, 29.7114444577256), 
                          (29.3604724221642, 29.69521264379293)]



map_center = [27.165862605978425, 31.164374416309347]
my_map_res = folium.Map(location=map_center, zoom_start=6)

enlarged_shape = enlarge_shape_at_centroid(restircted_coordinates, 1.1)


# for coord in restircted_coordinates:
#      folium.Marker(location=coord, popup='Point').add_to(my_map_res)

# folium.PolyLine(locations = restircted_coordinates + [restircted_coordinates[0]], color='red').add_to(my_map_res)



# Extract the coordinates from the Polygon object
polygon_coordinates = list(enlarged_shape.exterior.coords)

print(polygon_coordinates)

folium.Polygon(locations=restircted_coordinates, color='red', fill=True, fill_color='lightred').add_to(my_map_res)

# Plot the polygon
folium.Polygon(locations=polygon_coordinates, color='blue', fill=True, fill_color='lightblue').add_to(my_map_res)


# for coord in enlarged_shape:
#      folium.Marker(location=coord, popup='Point').add_to(my_map_res)

# folium.PolyLine(locations = enlarged_shape + [enlarged_shape[0]], color='green').add_to(my_map_res)



my_map_res.save("test_map_with_restricted_areas_shape.html")