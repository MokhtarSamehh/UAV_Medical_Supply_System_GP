import rasterio as rio
import pandas as pd
import numpy as np
import geopandas as gpd
import csv

filename = 'DEM\\gt30e020n40.tif'
with rio.open(filename) as src:
    #read image
    image = src.read()
    
    # transform image
    bands, rows, cols = np.shape(image)
    
    image1 = image.reshape(rows*cols, bands)
    print(np.shape(image1))
    
    # bounding box of image
    l, b, r, t = src.bounds
    
    #resolution of image
    res = src.res
    
    # meshgrid of X and Y
    x = np.arange(l, r, res[0])
    y = np.arange(t, b, -res[0])
    X, Y = np.meshgrid(x, y)
    print (np.shape(X))
    
    # flatten X and Y
    newX = X.flatten()
    newY = Y.flatten()
    print (np.shape(newX))
    
    # join XY and Z information
    export = np.column_stack((newX, newY, image1))
    fname = 'XYZ.csv'
    
    with open(fname, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(export)
        fp.close() # close file
