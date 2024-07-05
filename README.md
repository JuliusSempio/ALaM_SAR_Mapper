# ALaM_SAR_Mapper
Repository for codes developed for using SAR datasets in mapping during my stint at the ASTI-ALaM Project

The codes provided herewith are working prototypes of the DTW-based crop mapping tools using catalogs of time-series Sentinel-1 images, initially developed for the ASTI-ALaM Project (https://asti.dost.gov.ph/projects/alam-project/) to assist clients in locating sugarcane fields around the Philippines.

Being prototypes, the provided codes are eventually going to be subject to changes. But they are stable enough to be used as is _provided_ the following items have been prepared accordingly:
* Vector features in shapefile format in the "shp" folder
  - the parcel of crop to be used for generating the reference temporal signature
  - the boundaries of the study area from which the output map is going to be based on
* Time-series Sentinel-1 data catalogs in the "img_data" folder
  - the filenames contain the date of acquisition, preferably in the %Y-%m-%d format
 
For others questions about running the prototype codes, feel free to send an email to either of the following:
* juliusnoah.sempio@asti.dost.gov.ph
* jhsempio@alum.up.edu.ph
