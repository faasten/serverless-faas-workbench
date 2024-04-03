#!/bin/bash

if [ $# -ne 2 ]; then
    echo 'usage: ./run_benchmarks MINIO_ADDR BENCHDATA_DIR' >&2
    exit 1
fi

MINIO=$1
BENCHDATA=$2
# set alias & access key
mc admin alias set minio-test $MINIO minioadmin minioadmin 1>&2
# setup buckets
mc mb minio-test/test 1>&2
mc mb minio-test/test-out 1>&2
# setup files for image/video funtions
mc cp $BENCHDATA/image/image.jpg minio-test/test 1>&2
mc cp $BENCHDATA/video/SampleVideo_1280x720_10mb.mp4 minio-test/test 1>&2
mc cp $BENCHDATA/model/haarcascade_frontalface_default.xml minio-test/test 1>&2
mc cp $BENCHDATA/amzn_fine_food_reviews/reviews100mb.csv minio-test/test 1>&2

jsons=($(ls jsons))
for json in "${jsons[@]}"; do
    filename=$(basename -- "$json")
    action="${filename%.*}"
    echo $action 1>&2
    wsk action invoke $action --param-file <(jq '.endpoint_url="'$MINIO'"' jsons/$filename) -i -r
done
