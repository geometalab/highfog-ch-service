#!/usr/bin/env python3

"""
Creates maptiles from a GeoTiff using MapTiler pro.
"""
import os
import subprocess
import shlex
import uuid

COLOR_CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath("__file__")), "col.txt")

def run_with_log(command):
    # TODO: use actual logging!
    try:
        run = subprocess.run(shlex.split(command), check=True)
    except subprocess.CalledProcessError as err:
        print(err)
        raise
    print(run.stdout)
    print(run.stderr)


def create_tiles(input_file, output_dir, min_height, max_height, step, min_zoom, max_zoom):
    for height in range(min_height, max_height + step, step):
        print(f"Creating tiles for {height} metres above sea level.")

        unique_id = uuid.uuid4()

        calculated_temp_tif = f'{output_dir}/fog{height}{unique_id}.tif'
        relief_temp_tif = f'{output_dir}/fog{height}{unique_id}colored.tif'

        # Create 8bit GeoTiff. "Flooded" areas are assigned the Value 1, others 0/NoData using gdal_calc.py.
        calc_command = f'gdal_calc.py -A {input_file} --type=Byte --outfile={calculated_temp_tif} --calc="A<={height}" NotDataValue=0'

        # Color areas with the values 1 white and others black using gdaldem.
        color_command = f'gdaldem color-relief {calculated_temp_tif} {COLOR_CONFIG_FILE_PATH} {relief_temp_tif}'

        # Create map tiles using maptiler, black areas will be made transparent.
        if not os.path.exists(f'{output_dir}/{height}/'):
            os.makedirs(f'{output_dir}/{height}/', exist_ok=True)
        tiles_generation = f'gdal2tiles.py --no-kml --webviewer=none --resume --profile=mercator --zoom={min_zoom}-{max_zoom} --srcnodata=0 {relief_temp_tif} {output_dir}/{height}/'

        run_with_log(calc_command)
        run_with_log(color_command)
        run_with_log(tiles_generation)

        # Remove temporary files
        os.remove(calculated_temp_tif)
        os.remove(relief_temp_tif)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", type=str, help="input file (GeoTIF)")
    parser.add_argument("output_dir", type=str, help="empty(!) output directory")

    parser.add_argument("min_height", type=int, help="Height range: minimum elevation")
    parser.add_argument("max_height", type=int, help="Height range: maximum elevation")
    parser.add_argument("step", type=int, help="steps for elevation size")
    parser.add_argument("min_zoom", type=int, help="zoom-level start")
    parser.add_argument("max_zoom", type=int, help="zoom-level end")


    args = parser.parse_args()
    input_file, output_dir, min_height, max_height, step, min_zoom, max_zoom = \
        args.input_file, args.output_dir, args.min_height, args.max_height, args.step, args.min_zoom, args.max_zoom

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    assert os.path.isfile(input_file)
    assert os.path.isdir(output_dir)

    create_tiles(input_file, output_dir, min_height, max_height, step, min_zoom, max_zoom)
