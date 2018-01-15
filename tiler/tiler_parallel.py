#!/usr/bin/env python3

"""
Creates maptiles from a GeoTiff using MapTiler pro.
"""
# import pprint
import os
import shlex

import run_commands_async


def create_tiles_parallel(input_file, output_dir, min_height, max_height, step, min_zoom, max_zoom):
    parallel_commands = []
    for height in range(min_height, max_height + step, step):
        for zoom in range(min_zoom, max_zoom + 1):
            parallel_commands.append(
                shlex.split(" ".join([str(i) for i in ['/code/tiler.py', input_file, output_dir, height, height, step, zoom, zoom]]))
            )
    # pprint.pprint(parallel_commands)
    run_commands_async.run_in_parallel(parallel_commands)


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

    create_tiles_parallel(input_file, output_dir, min_height, max_height, step, min_zoom, max_zoom)
