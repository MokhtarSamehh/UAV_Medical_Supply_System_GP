import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
import folium
import pandas as pd
import webbrowser

####### Adjust settings here #######
max_approved_height = 1000
row_division_denumerator = 200
col_division_denumerator = 200

# Defaults
dem_path = 'Scripts/DEM/gt30e020n40.dem'
dem_rows = 6000
dem_cols = 4800

#create a map
this_map = folium.Map(location=[20.0041, 39.9958], prefer_canvas=True, zoom_start=5)

# Args for the big boundary rectangle
gtopo_rect_kw = {
    "color": "blue",
    "line_cap": "round",
    # "fill": True,
    # "fill_color": "red",
    "weight": 2,
    # "popup": "Tokyo, Japan",
    "tooltip": "bob"
}


def plotDot(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=[point.latitude, point.longitude],
                        radius=2,
                        weight=5,
                        tooltip=f"{point.latitude}, {point.longitude}").add_to(this_map)


def unapproved_rec_kw(rectangle):
    return {
        # "color": "blue",
        "line_cap": "round",
        "fill": True,
        "fill_color": "red",
        "weight": 2,
        # "popup": "Tokyo, Japan",
        "tooltip": f"""
        <strong>Index: {rectangle["index"]}</strong><br><br>
        <strong>Upper Left: {rectangle["upper_left"]}</strong><br>
        <strong>Upper Right: {rectangle["upper_right"]}</strong><br>
        <strong>Lower Left: {rectangle["lower_left"]}</strong><br>
        <strong>Lower Right: {rectangle["lower_right"]}</strong><br>
        """,
    }


with rio.open(dem_path, 'r') as raster_dem:
    points_list = []        # Points to draw on Folium map
    unapproved_rectangles = []   # List of lists each mapping an unapproved rectangle
    
    # Get data into array
    data_array = raster_dem.read(1)
    
    upper_left_corner = raster_dem.xy(0, 0)
    points_list.append([upper_left_corner[1], upper_left_corner[0]])
    
    lower_right_corner = raster_dem.xy(dem_rows-1, dem_cols-1)
    points_list.append([lower_right_corner[1], lower_right_corner[0]])
    
    
    rows_step = int(dem_rows / row_division_denumerator)
    cols_step = int(dem_cols / col_division_denumerator)
    rect_rows = 0
    rect_cols = 0
    rect_counter = 0
    
    for x in range(0, dem_rows, rows_step):
        rect_rows += 1
        rect_cols = 0
        
        for y in range(0, dem_cols, cols_step):
            rect_cols += 1
            rect_counter += 1
            
            max_height = np.max(data_array[x:x + rows_step, y:y + cols_step])
            
            upper_left = raster_dem.xy(x, y)
            lower_left = raster_dem.xy(x + rows_step, y)
            upper_right = raster_dem.xy(x, y + cols_step)
            lower_right = raster_dem.xy(x + rows_step, y + cols_step)
            
            if max_height > max_approved_height:
                rectangle = {
                    "index": rect_counter - 1,
                    "upper_left": [upper_left[1], upper_left[0]],
                    "upper_right": [upper_right[1], upper_right[0]],
                    "lower_left": [lower_left[1], lower_left[0]],
                    "lower_right": [lower_right[1], lower_right[0]]
                }
            
                unapproved_rectangles.append(rectangle)
    
    # print(rect_rows, rect_cols)
    
    for idx, current_rectangle in enumerate(unapproved_rectangles):
        for next_rectangle in unapproved_rectangles[idx:]:            
            if current_rectangle["lower_right"] == next_rectangle["lower_left"] \
                and current_rectangle["upper_right"] == next_rectangle["upper_left"]:
                    current_rectangle["lower_right"] = next_rectangle["lower_right"]
                    current_rectangle["upper_right"] = next_rectangle["upper_right"]
                    
                    unapproved_rectangles.pop(idx + 1)
                    # print("popped")

        
    for rectangle in unapproved_rectangles:
        folium.Rectangle(
            bounds=[rectangle["upper_left"], rectangle["lower_right"]],
            line_join="round",
            dash_array="5, 5",
            **unapproved_rec_kw(rectangle),
        ).add_to(this_map)
    
    points_df = pd.DataFrame(points_list, 
                            columns=["latitude", "longitude"])

    points_df.apply(plotDot, axis=1)

    # Create rectangle around GTOPO30 DEM file borders
    # folium.Rectangle(
    #     bounds=[points_list[1], points_list[0]],
    #     line_join="round",
    #     dash_array="5, 5",
    #     **gtopo_rect_kw,
    # ).add_to(this_map)

    # Save the map to an HTML file
    this_map.save('elevation_map.html')
    webbrowser.open('elevation_map.html')
    
