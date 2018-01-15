#!/bin/bash
set -e

if [ ! -f ${RESULT_TIF} ]; then
    gdalwarp -cutline ${CUTLINE_AREA_SHP} -crop_to_cutline -srcnodata 0 ${TIF_SOURCE} ${RESULT_TIF}
fi


# TODO: finally
# rm ${RESULT_TIF}

echo "DONE"
