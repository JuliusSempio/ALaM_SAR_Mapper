import numpy as np
import pandas as pd
import datetime as dt
from tqdm import tqdm # module for visual progress bars

import math # module for quick detection of NaN pixels

from dtaidistance import dtw # the mother module for obtaining the distance accumulated cost
# from dtaidistance import dtw_ndim # accessory module for testing multi-dimensional DTW
# from dtaidistance import dtw_visualisation as dtwvis # accessory module for visualizing DTW results


def generate_accumulated_distance_cost_map(test_data_list,
                                           band,
                                           study_area_geom,
                                           start_of_test_year,
                                           date_format,
                                           crop_parcel_reference_temporal_signature_1d,
                                           dtw_window_size,
                                           dtw_psi,
                                           dtw_max_dist,
                                           dtw_use_pruning,
                                           img_dimensions,
                                           lon_increment,
                                           lat_increment):
    
    pixel_cost_array_df = pd.DataFrame(columns = ["distance_cost", "x", "longitude", "y", "latitude"])

    lon_track = study_area_geom.bounds["minx"][0]

    for col in tqdm(range(img_dimensions[1] - 1)):
        lat_track = study_area_geom.bounds["maxy"][0]
    
        for row in range(img_dimensions[0] - 1):
            pixel_timeseries_array = [] # Temporarily stores date and pixel data array information for DTW computation
        
            for count in range(len(test_data_list)):
                # Skips blank and NaN pixels
                if (test_data_list[count][1].sel(band=band).data[row][col] == 0. or
                    math.isnan(test_data_list[count][1].sel(band=band).data[row][col])):
                    continue
            
                # Procedures for valid pixels
                else:
                    day_of_acquisition = (dt.datetime.strptime(test_data_list[count][0], date_format) -
                        dt.datetime.strptime(start_of_test_year, date_format)).days
                    pixel_value = test_data_list[count][1].sel(band=band).data[row][col]
                    pixel_timeseries_array.append([day_of_acquisition, pixel_value])
                
            # Skips the DTW calculator phase if timeseries array is empty
            if not pixel_timeseries_array:
                lat_track = lat_track - lat_increment
                continue
            
            # activates the DTW calculator phase for non-empty array
            else:
                #pixel_timeseries_array[pixel_timeseries_array[:, 0].argsort()]
                pixel_timeseries_array_1d = np.array([row[1] for row in pixel_timeseries_array])
                distance_1d = dtw.distance(
                    pixel_timeseries_array_1d,
                    crop_parcel_reference_temporal_signature_1d,
                    window=dtw_window_size,
                    psi=dtw_psi,
                    #max_dist = dtw_max_dist,
                    use_pruning = dtw_use_pruning
                )
                pixel_cost_array_df.loc[len(pixel_cost_array_df)] = [distance_1d, col, lon_track, row, lat_track]
                lat_track = lat_track - lat_increment
            
        lon_track = lon_track + lon_increment
    
    return pixel_cost_array_df