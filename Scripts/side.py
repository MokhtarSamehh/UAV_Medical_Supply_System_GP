from rasterio.plot import show
import rasterio
src = rasterio.open('10_DEM_y30x30.tif')
print(src.read(1).dtype)
#show('output.tif', cmap='terrain')