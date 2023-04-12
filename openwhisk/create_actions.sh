#!/bin/bash -x
ACTIONDIR=$(dirname $(realpath $0))/cpu-memory
actions=($(ls $ACTIONDIR))

for action in "${actions[@]}"; do
    wsk action create $action $ACTIONDIR/$action/function.py --docker yuetan/py3:$action -i
done
