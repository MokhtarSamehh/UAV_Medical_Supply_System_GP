import rasterio , os
from rasterio.merge import merge
from rasterio.plot import show
import tifffile as tiff
from shapely.geometry import box
from rasterio.mask import mask
import geopandas as gpd

# upper_left_x = 699934.584491
# upper_left_y = 6169364.0093
# lower_right_x = 700160.946739
# lower_right_y = 6168703.00544

# bbox = (lower_right_x,lower_right_y,upper_left_x,upper_left_y)

# gdal.Translate('output_crop_raster.tif', 'output.tif', projWin = bbox)

# lowerright = rasterio.open('10_DEM_y20x30.tif')
# lowerleft = rasterio.open('10_DEM_y20x20.tif')
# upperright = rasterio.open('10_DEM_y30x20.tif')
# upperleft = rasterio.open('10_DEM_y30x30.tif')
# datasetlr = lowerright.read()
# datasetll = lowerleft.read()
# datasetul = upperleft.read()
# datasetur = upperright.read()
# #print(datasetlr.shape)
# #print(datasetll.shape)

# dem1_path = os.path.join("10_DEM_y20x30.tif")
# dem2_path = os.path.join("10_DEM_y20x20.tif")
dem3_path = os.path.join("10_DEM_y30x20.tif")
# dem4_path = os.path.join("10_DEM_y30x30.tif")

# with rasterio.open(dem1_path) as src1:
#     dem1 = src1.read(1, masked=True)
#     transform1 = src1.transform
#     crs1 = src1.crs

# with rasterio.open(dem2_path) as src2:
#     dem2 = src2.read(1, masked=True)
#     transform2 = src2.transform
#     crs2 = src2.crs

with rasterio.open(dem3_path) as src3:
    dem3 = src3.read(1, masked=True)
    transform3 = src3.transform
    crs3 = src3.crs

# with rasterio.open(dem4_path) as src4:
#     dem4 = src4.read(1, masked=True)
#     transform4 = src4.transform
#     crs4 = src4.crs

# egypt, out_trans = merge([rasterio.open(dem1_path), rasterio.open(dem2_path), rasterio.open(dem3_path), rasterio.open(dem4_path)])
# show(egypt, cmap='terrain')

# image_array = egypt

# tiff.imwrite('output.tif', image_array)

# bbox = box(2500, 4000, 10000, 8000) #xmin, ymin, xmax, ymax

# with rasterio.open('output.tif') as src:
#     out_image, out_transform = mask(src, [bbox], crop=True)
#     out_meta = src.meta.copy()

# show(out_image, cmap='terrain')
print(src3)