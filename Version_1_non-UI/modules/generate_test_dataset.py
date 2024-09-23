# import numpy as np
# import pandas as pd
import os, glob
import re # module for extracting and tabulating date information from filename

import rioxarray as rxr # module for xarray-based recording of GeoTIFF data
import xarray as xr
import earthpy.plot as ep # module for fast plotting of GeoTIFF images

def generate_test_dataset(band,
                          scan_mode,
                          test_folder_path,
                          study_area_geom):
    
    test_data_list = []

    for filename in glob.glob(os.path.join(test_folder_path, '*' + scan_mode + '*.tif')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            date = re.search("([0-9]{4}[0-9]{2}[0-9]{2})", filename).group()
            formatted_date = date[:4] + "-" + date[4:6] + "-" + date[6:8]
            test_data_list.append([formatted_date, rxr.open_rasterio(filename,
                                masked=True
                                ).rio.clip(
                                study_area_geom.geometry.values, study_area_geom.crs, from_disk=True
                                )])
            
    # Making a sample plot of the test dataset
    titles = [band]
    ep.plot_bands(test_data_list[0][1].sel(band=band), title=titles)
    
    # Creation of new accessory constants based on test dataset
    img_dimensions = test_data_list[0][1].sel(band=band).shape
    
    # Formulation of equivalents to pixel dimensions in lat-long degree measure
    lon_increment = (study_area_geom.bounds['maxx'][0] - study_area_geom.bounds['minx'][0]) / img_dimensions[1]
    lat_increment = (study_area_geom.bounds['maxy'][0] - study_area_geom.bounds['miny'][0]) / img_dimensions[0]

    # CAUTION: Keep in mind that an image's Cartesian y-axis may be the opposite of a geographical y-axis
    print("Longitude Increment: ", lon_increment, "\nLatitude Decrement: ", lat_increment)
    
    return test_data_list, img_dimensions, lon_increment, lat_increment