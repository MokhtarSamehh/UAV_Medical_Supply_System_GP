# GRAVEYARD

# dem = rio.open(dem_path)
# dem_array = dem.read(1).astype('float64')

# fig, ax = plt.subplots(1, figsize=(12, 12))
# show(dem_array, cmap='Greys_r', ax=ax)
# plt.axis("off")
# plt.show()

# fig, ax = plt.subplots(1, figsize=(12, 12))
# show(dem_array, cmap='Greys_r', ax=ax)
# show(dem_array, contour=True, ax=ax, linewidths=0.7)
# plt.axis("off")
# plt.show()




import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
import folium
import pandas as pd
import webbrowser

def plotDot(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=[point.latitude, point.longitude],
                        radius=2,
                        weight=5,
                        tooltip=f"{point.latitude}, {point.longitude}").add_to(this_map)
    
    
dem_path = 'DEM/gt30e020n40.dem'
dem_rows = 6000
dem_cols = 4800
max_approved_height = 1000

gtopo_rect_kw = {
    "color": "blue",
    "line_cap": "round",
    # "fill": True,
    # "fill_color": "red",
    "weight": 2,
    # "popup": "Tokyo, Japan",
    "tooltip": "<strong>Click me!</strong>",
}

unapproved_rec_kw = {
    # "color": "blue",
    "line_cap": "round",
    "fill": True,
    "fill_color": "red",
    "weight": 2,
    # "popup": "Tokyo, Japan",
    "tooltip": "<strong>Click me!</strong>",
}

#create a map
this_map = folium.Map(location=[20.0041, 39.9958], prefer_canvas=True, zoom_start=5)

with rio.open(dem_path, 'r') as raster_dem:
    points_list = []        # Points to draw on Folium map
    rectangles_list = []    # Map to be divided into rectangles to be studied and recorded here
    unapproved_areas = []   # List of lists each mapping an unapproved rectangle boundary
    
    # Get data into array
    data_array = raster_dem.read(1)
    
    upper_left_corner = raster_dem.xy(0, 0)
    points_list.append([upper_left_corner[1], upper_left_corner[0]])
    
    lower_right_corner = raster_dem.xy(dem_rows-1, dem_cols-1)
    points_list.append([lower_right_corner[1], lower_right_corner[0]])
    
    
    rows_step = int(dem_rows / 200)
    cols_step = int(dem_cols / 200)
    
    for x in range(0, dem_rows, rows_step):
        for y in range(0, dem_cols, cols_step):
            max_height = np.max(data_array[x:x + rows_step, y:y + cols_step])
            
            upper_left = raster_dem.xy(x, y)
            upper_right = raster_dem.xy(x + rows_step, y)
            lower_left = raster_dem.xy(x, y + cols_step)
            lower_right = raster_dem.xy(x + rows_step, y + cols_step)
            
            rectangle = {
                "approved": 1 if max_height < max_approved_height else 0,
                "upper_left": [upper_left[1], upper_left[0]],
                "upper_right": [upper_right[1], upper_right[0]],
                "lower_left": [lower_left[1], lower_left[0]],
                "lower_right": [lower_right[1], lower_right[0]]
            }
            
            rectangles_list.append(rectangle)
             
    
    for rectangle in rectangles_list:
        if not rectangle["approved"]:
            unapproved_areas.append(
                [
                    rectangle["upper_left"], rectangle["upper_right"], 
                    rectangle["lower_left"], rectangle["lower_right"]
                ]
            )
            
            # Create rectangle around GTOPO30 DEM file borders
            folium.Rectangle(
                bounds=[rectangle["upper_left"], rectangle["lower_right"]],
                line_join="round",
                dash_array="5, 5",
                **unapproved_rec_kw,
            ).add_to(this_map)
            
    
    points_df = pd.DataFrame(points_list, 
                            columns=["latitude", "longitude"])

    points_df.apply(plotDot, axis=1)

    # Create rectangle around GTOPO30 DEM file borders
    folium.Rectangle(
        bounds=[points_list[1], points_list[0]],
        line_join="round",
        dash_array="5, 5",
        **gtopo_rect_kw,
    ).add_to(this_map)

    # Save the map to an HTML file
    this_map.save('simple_dot_plot.html')
    webbrowser.open('simple_dot_plot.html')
    
