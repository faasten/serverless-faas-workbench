#!/bin/bash -x
ACTIONDIR=$(dirname $(realpath $0))/cpu-memory
actions=($(ls $ACTIONDIR))
for action in "${actions[@]}"; do
    docker build -t py3:$action $ACTIONDIR/$action
    docker tag py3:$action yuetan/py3:$action
    docker push yuetan/py3:$action
done
