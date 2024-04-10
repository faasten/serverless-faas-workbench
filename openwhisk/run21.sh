#!/bin/bash

if [ $# -ne 2 ]; then
    echo 'usage: ./run_benchmarks MINIO_ADDR BENCHDATA_DIR' >&2
    exit 1
fi

MINIO=$1     # E.g., http://10.11.107.12:9000
BENCHDATA=$2 # Bench data directory
# set alias & access key
mc alias set minio-test $MINIO minioadmin minioadmin 1>&2
# setup buckets
mc mb minio-test/test 1>&2
mc mb minio-test/test-out 1>&2
# setup files for image/video funtions
mc cp $BENCHDATA/image/image.jpg minio-test/test 1>&2
mc cp $BENCHDATA/video/SampleVideo_1280x720_10mb.mp4 minio-test/test 1>&2
mc cp $BENCHDATA/model/haarcascade_frontalface_default.xml minio-test/test 1>&2
mc cp $BENCHDATA/amzn_fine_food_reviews/reviews100mb.csv minio-test/test 1>&2

jsons=(chameleon.json float_operation.json image_processing.json linpack.json matmul.json pyaes.json video_processing.json)

RUNS=21

for (( i=0; i<$RUNS; i=i+1 )); do
    for json in "${jsons[@]}"; do
        filename=$(basename -- "$json")
        action="${filename%.*}"
        echo $action 1>&2
        result=$(wsk action invoke $action --param-file <(jq '.endpoint_url="'$MINIO'"' jsons/$filename) -i -r 2>&1 | \
                sed "s/ok: invoked .*, but the request has not yet finished, with id \([[:xdigit:]]*\)/\1/g")
        maybe_id=$result
        echo "$result" | jq > /dev/null 2>&1
        while [ $? -ne 0 ]; do
          sleep 1
          result=$( (wsk activation get $maybe_id -i 2>&1 || echo 'output to fail jq') | tail -n +2 | jq .response.result 2>&1)
        done
        echo "$result"
    done
done
