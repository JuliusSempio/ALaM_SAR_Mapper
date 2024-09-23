import geopandas as gpd
from geocube.api.core import make_geocube # module for conversion of vectors into rasters
import altair as alt # module for plot charting
import altair_viewer

# Initialize global variables #
PLATFORM = None
SCAN_MODE = None
BAND = None
CROP_REFERENCE_TYPE = None
CROP_REFERENCE_GEOMETRY = None
CROP_REFERENCE_YEAR = None
TEST_YEAR = None
DATE_FORMAT = None
START_OF_CROP_REFERENCE_YEAR = None
START_OF_TEST_YEAR = None
STUDY_AREA_NAME = None
STUDY_AREA_GEOM = None
CROP_REFERENCE_FOLDER_PATH = None
TEST_FOLDER_PATH = None
DTW_WINDOW_SIZE = None
DTW_PSI = None
DTW_MAX_DIST = None
DTW_USE_PRUNING = None
DTW_USE_C = None
DTW_COST_THRESHOLD = None

# Parameter loading - needed for preparing differences in S1 and P2 inputs #
def get_global_var_dict(dictionary):
        ## Idenfity local declarations as global instead
        global PLATFORM
        global SCAN_MODE
        global BAND
        global CROP_REFERENCE_TYPE
        global CROP_REFERENCE_GEOMETRY
        global CROP_REFERENCE_YEAR
        global TEST_YEAR
        global DATE_FORMAT
        global START_OF_CROP_REFERENCE_YEAR
        global START_OF_TEST_YEAR
        global STUDY_AREA_NAME
        global STUDY_AREA_GEOM
        global CROP_REFERENCE_FOLDER_PATH
        global TEST_FOLDER_PATH
        global DTW_WINDOW_SIZE
        global DTW_PSI
        global DTW_MAX_DIST
        global DTW_USE_PRUNING
        global DTW_USE_C
        global DTW_COST_THRESHOLD
        
        ## Platform parameter configurations ##
        PLATFORM = dictionary['platform']
        SCAN_MODE = dictionary['scan_mode']
        BAND = dictionary['band']

        ## Data directory configurations ##
        # Shapefile for for generating reference temporal signature
        CROP_REFERENCE_TYPE = dictionary['croptype']
        CROP_REFERENCE_GEOMETRY = gpd.read_file(dictionary['sample_shp'])
        CROP_REFERENCE_YEAR = dictionary['crop_reference_startDate'][:4]
        TEST_YEAR = dictionary['test_data_startDate'][:4]

        if(PLATFORM == 'Sentinel-1'):
            DATE_FORMAT = "%Y-%m-%d"
            START_OF_CROP_REFERENCE_YEAR = dictionary['crop_reference_startDate'].replace("/", "-")
            START_OF_TEST_YEAR = dictionary['test_data_startDate'].replace("/", "-")
        elif(PLATFORM == 'PALSAR-2'):
            DATE_FORMAT = "%y-%m-%d"
            START_OF_CROP_REFERENCE_YEAR = dictionary['crop_reference_startDate'][2:].replace("/", "-")
            START_OF_TEST_YEAR = dictionary['test_data_startDate'][2:].replace("/", "-")
        else:
            DATE_FORMAT = "%Y/%m/%d"
            START_OF_CROP_REFERENCE_YEAR = dictionary.crop_reference_startDate.replace("/", "-")
            START_OF_TEST_YEAR = dictionary['test_data_startDate'].replace("/", "-")

        # Study area boundary shapefile
        STUDY_AREA_NAME = dictionary['studyarea_name']
        STUDY_AREA_GEOM = gpd.read_file(dictionary['studyarea_shp'])

        # Preprocessed reference and test data paths
        CROP_REFERENCE_FOLDER_PATH = dictionary['reference_directory']
        TEST_FOLDER_PATH = dictionary['test_directory']

        ## DTW parameter configurations ##
        # allowance for dynamic diagonal shifting, using 1 will make the algorithm calculate the Euclidean distance
        DTW_WINDOW_SIZE = dictionary['dtw_window_size']
        # PSI (Prefix and Suffix-Invariant) relaxation parameter
        DTW_PSI = dictionary['dtw_psi']
        # avoid computing partial paths that will be larger than this value, returning infinity
        DTW_MAX_DIST = float("inf")
        # automates determination of the above MAX_DIST parameter
        DTW_USE_PRUNING = dictionary['dtw_use_pruning']
        # DTAIdistance-exclusive call to use pure C-based compiled functions (default is False)
        DTW_USE_C = dictionary['dtw_use_C']
        DTW_COST_THRESHOLD = 20 # maximum allowable distance cost threshold before pixels are masked out of the final map

# The Main Body #
def run_Mapper():
    
    ## Test if parameters are properly recorded from dictionary to global variables ##
    #     print(PLATFORM)
    #     print(SCAN_MODE)
    #     print(BAND)
    #     print(CROP_REFERENCE_TYPE)
    #     print(CROP_REFERENCE_GEOMETRY)
    #     print(CROP_REFERENCE_YEAR)
    #     print(TEST_YEAR)
    #     print(DATE_FORMAT)
    #     print(START_OF_CROP_REFERENCE_YEAR)
    #     print(START_OF_TEST_YEAR)
    #     print(STUDY_AREA_NAME)
    #     print(STUDY_AREA_GEOM)
    #     print(CROP_REFERENCE_FOLDER_PATH)
    #     print(TEST_FOLDER_PATH)
    #     print(DTW_WINDOW_SIZE)
    #     print(DTW_PSI)
    #     print(DTW_MAX_DIST)
    #     print(DTW_USE_PRUNING)
    #     print(DTW_USE_C)
    #     print(DTW_COST_THRESHOLD)    
    
    ## Creating the reference temporal signature based on scan mode ##
    from modules.generate_temporal_signature import generate_temporal_signature
    
    print("### REFERENCE YEAR: %s || TEST YEAR: %s ###" %(CROP_REFERENCE_YEAR, TEST_YEAR))
    print("### REFERENCE PARCEL AND TEMPORAL SIGNATURE PLOTS ###")
    crop_reference_temporal_signature_1D, crop_reference_temporal_signature_df = \
        generate_temporal_signature(PLATFORM,
                                    BAND,
                                    SCAN_MODE,
                                    START_OF_CROP_REFERENCE_YEAR,
                                    DATE_FORMAT,
                                    CROP_REFERENCE_FOLDER_PATH,
                                    CROP_REFERENCE_GEOMETRY)

    reference_temporal_signature_plot = alt.Chart(crop_reference_temporal_signature_df).mark_line().encode(
        x = 'days',
        y = 'band ' + str(BAND)
    )
    alt.renderers.enable('default')
    reference_temporal_signature_plot.show()

    ## Preparing the test dataset ##
    from modules.generate_test_dataset import generate_test_dataset
    print("### SAMPLE TEST DATASET PLOT ###")
    test_data_list, IMG_DIMENSIONS, LON_INCREMENT, LAT_INCREMENT = generate_test_dataset(PLATFORM,
                                                                                         BAND,
                                                                                         SCAN_MODE,
                                                                                         TEST_FOLDER_PATH,
                                                                                         STUDY_AREA_GEOM)

    ## Generation of accumulated distance cost map ##
    from modules.generate_accumulated_distance_cost_map import generate_accumulated_distance_cost_map
    print("### BEGINNING ACCUMULATED DISTANCE COST MAP GENERATION ###")
    accumulated_distance_cost_map_df = generate_accumulated_distance_cost_map(test_data_list,
                                                                              PLATFORM,
                                                                              BAND,
                                                                              STUDY_AREA_GEOM,
                                                                              START_OF_TEST_YEAR,
                                                                              DATE_FORMAT,
                                                                              crop_reference_temporal_signature_1D,
                                                                              DTW_WINDOW_SIZE,
                                                                              DTW_PSI,
                                                                              DTW_MAX_DIST,
                                                                              DTW_USE_PRUNING,
                                                                              IMG_DIMENSIONS,
                                                                              LON_INCREMENT,
                                                                              LAT_INCREMENT)

    # Output Generation #
    print("### SAVING GENERATED ACCUMULATED DISTANCE COST MAP ###")
    accumulated_distance_cost_map_gdf = gpd.GeoDataFrame(
        accumulated_distance_cost_map_df, geometry=gpd.points_from_xy(
            accumulated_distance_cost_map_df.longitude, accumulated_distance_cost_map_df.latitude), crs="EPSG:4326"
    )
    
    # Conversion to raster form
    out_grid = make_geocube(
        vector_data=accumulated_distance_cost_map_gdf,
        measurements=['distance_cost'],
        resolution=(-LON_INCREMENT, LAT_INCREMENT),
    )
    
    output_filename = "out/distmap_" + STUDY_AREA_NAME + "_" + CROP_REFERENCE_TYPE + "_" + SCAN_MODE +  "_b" + str(BAND) + \
        "_refpclyear"+ str(CROP_REFERENCE_YEAR) + "_testyear"+ str(TEST_YEAR) + "_dtw_ws" + str(DTW_WINDOW_SIZE) + \
        "_psi" + str(DTW_PSI) + "_pr" + str(DTW_USE_PRUNING) + "_C" + str(DTW_USE_C) + "_full.tif"
    out_grid.rio.to_raster(output_filename)
    
    print("### ALL DONE :) ###")