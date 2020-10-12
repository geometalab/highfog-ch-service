#!/usr/bin/env python3

"""
Creates maptiles from a GeoTiff using MapTiler pro.
"""
# import pprint
import os
import shlex
import collections
import math

import run_commands_async


CorePartition = collections.namedtuple(
    'CorePartition', ['spawner_cores', 'tiler_cores'])


def calculate_max_cores():
    spawner_cores = 1
    tiler_cores = 1
    cores_to_use = int(os.environ.get('NUM_CORES', 1))
    if cores_to_use > 4:
        spawner_cores = math.floor(math.sqrt(cores_to_use))
        tiler_cores = math.floor(math.sqrt(cores_to_use))
    return CorePartition(spawner_cores=spawner_cores, tiler_cores=tiler_cores)


def create_tiles_parallel(input_file, output_dir, min_height, max_height, step, min_zoom, max_zoom):
    cores = calculate_max_cores()
    spawner_cores = cores.spawner_cores
    number_processes = cores.tiler_cores
    parallel_commands = []
    for height in range(min_height, max_height + step, step):
        parallel_commands.append(
            shlex.split(" ".join([str(i) for i in [
                        '/code/tiler.py', input_file, output_dir, height, height, step, min_zoom, max_zoom, number_processes]]))
        )
    # pprint.pprint(parallel_commands)
    run_commands_async.run_in_parallel(
        parallel_commands, max_concurrent_tasks=spawner_cores)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", type=str, help="input file (GeoTIF)")
    parser.add_argument("output_dir", type=str,
                        help="empty(!) output directory")

    parser.add_argument("min_height", type=int,
                        help="Height range: minimum elevation")
    parser.add_argument("max_height", type=int,
                        help="Height range: maximum elevation")
    parser.add_argument("step", type=int, help="steps for elevation size")
    parser.add_argument("min_zoom", type=int, help="zoom-level start")
    parser.add_argument("max_zoom", type=int, help="zoom-level end")

    args = parser.parse_args()
    input_file, output_dir, min_height, max_height, step, min_zoom, max_zoom = args.input_file, args.output_dir, args.min_height, args.max_height, args.step, args.min_zoom, args.max_zoom

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    assert os.path.isfile(input_file)
    assert os.path.isdir(output_dir)

    create_tiles_parallel(input_file, output_dir, min_height,
                          max_height, step, min_zoom, max_zoom)
