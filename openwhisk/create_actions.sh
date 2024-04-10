#!/bin/bash -x
ACTIONDIR=$(dirname $(realpath $0))/cpu-memory
actions=($(ls $ACTIONDIR))

for action in "${actions[@]}"; do
    wsk action update $action $ACTIONDIR/$action/function.py --docker yuetan/py3:$action -i
done


#for action in "${actions[@]}"; do
#    wsk action delete $action -i
#done
