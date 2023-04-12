#!/bin/bash

# TODO
# setup files for image/video funtions


jsons=($(ls jsons))
for json in "${jsons[@]}"; do
    filename=$(basename -- "$json")
    action="${filename%.*}"
    wsk action invoke $action --param-file jsons/$filename -i -r
done
