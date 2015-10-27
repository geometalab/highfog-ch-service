# Maptiles from GeoTiff
* This script creates white tiles from a GeoTiff using Floodfill in a height range with custom steps and zoom levels.
* MapTiler Pro and GDAL must be installed and set in the PATH variable in order for this script to execute.
* Executing this script might take several hours depending on zoom levels.

## Usage (all parameters are mandatory, height in metres, output directory must be empty):
* tiler.py calc inputfile outputdirectory min_height max_height step min_zoom max_zoom