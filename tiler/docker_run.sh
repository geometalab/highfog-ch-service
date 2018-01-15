#!/bin/bash
set -e

if [ ! -f ${RESULT_TIF} ]; then
    gdalwarp -cutline ${CUTLINE_AREA_SHP} -crop_to_cutline -srcnodata 0 ${TIF_SOURCE} ${RESULT_TIF}
fi

./tiler_parallel.py ${RESULT_TIF} ${RESULT_DIR} 180 4700 20 7 14
# ./tiler_parallel.py ${RESULT_TIF} ${RESULT_DIR} 500 520 20 7 8
# TODO: finally
# rm ${RESULT_TIF}

echo "DONE"
