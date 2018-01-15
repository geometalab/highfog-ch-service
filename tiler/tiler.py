'''
Creates maptiles from a GeoTiff using MapTiler pro.
'''
import sys
import os

def main(argv):
    if os.path.isfile(argv[0]):
        input_file = argv[0]
    else:
        exit_script(argv[0] + ' is not a file!')
    if os.path.isdir(argv[1]):
        if os.listdir(argv[1]) == []:
            output_dir = argv[1]
        else:
            exit_script(argv[1] + ' is not an empty directory!')
    else:
        exit_script(argv[1] + ' is not a directory!')
        
    min_height = int(argv[2])
    max_height = int(argv[3])
    step = int(argv[4])
    min_zoom = argv[5]
    max_zoom = argv[6]
    
    create_tiles(input_file, output_dir, min_height, max_height, step, min_zoom, max_zoom)  

def create_tiles(input_file, output_dir, min_height, max_height, step, min_zoom, max_zoom):
    for height in range(min_height, max_height + step, step):
        print "Creating tiles for " + str(height) + " metres above sea level."
        
        # Create 8bit GeoTiff. "Flooded" areas are assigned the Value 1, others 0/NoData using gdal_calc.py.
        calc_command = "gdal_calc.py -A " + input_file + " --type=Byte  --outfile=" + output_dir + "/fog" + str(height) + ".tif --calc=\"A<=" + str(height) + "\" NotDataValue=0"
        os.system(calc_command)
        
        # Color areas with the values 1 white and others black using gdaldem.
        color_config = os.path.dirname(os.path.realpath("__file__")) + "\col.txt"
        color_command = "gdaldem color-relief " + output_dir + "/fog" + str(height) + ".tif " + color_config + " " + output_dir + "/fog" + str(height) + "colored.tif"
        os.system(color_command)
        
        # Create map tiles using maptiler, black areas will be made transparent.
        command3 = "maptiler -o " + output_dir + "/"+ str(height) + " " + output_dir + "/fog" + str(height) + "colored.tif -zoom " + min_zoom + " " + max_zoom +" -nodata 0 0 0"
        os.system(command3)
        
        # Remove temporary files
        os.remove( output_dir + "/fog" + str(height) + ".tif") 
        os.remove(output_dir + "/fog" + str(height) + "colored.tif")

def exit_script(message):
    print "Usage: tiler.py calc inputfile outputdirectory min_height max_height step min_zoom max_zoom\n"
    print message
    sys.exit()  
    
if __name__ == "__main__":
    if len(sys.argv) == 8:
        main(sys.argv[1:])
    else:
        exit_script('Wrong amount of arguments given!')
