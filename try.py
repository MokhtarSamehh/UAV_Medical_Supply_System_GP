import rasterio

# Open the GeoTIFF file
with rasterio.open("output.tif") as src:
    # Access raster data
    data = src.read()

# Now you can work with the raster data as a NumPy array
print(data)