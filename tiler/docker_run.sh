#!/bin/bash
set -e

if [ ! -f ${RESULT_TIF} ]; then
    gdalwarp -cutline ${CUTLINE_AREA_SHP} -crop_to_cutline -srcnodata 0 ${TIF_SOURCE} ${RESULT_TIF}
fi

./tiler.py ${RESULT_TIF} ${RESULT_DIR} ${START_ELEVATION:-0} ${STOP_ELEVATION:-5000} ${STEP_SIZE_ELEVATION:-20} ${ZOOM_LEVEL_MIN:-7} ${ZOOM_LEVEL_MAX:-14} ${NUM_CORES:-1}


find ./data/result/ -name '*.png' -print0 | xargs -0 -P${NUM_CORES:-1} -L9 pngquant --ext .png --force 16

rm ${RESULT_TIF}

echo "DONE"
