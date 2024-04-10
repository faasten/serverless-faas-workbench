#!/bin/bash -x
ACTIONDIR=$(dirname $(realpath $0))/cpu-memory
actions=($(ls $ACTIONDIR))

for action in "${actions[@]}"; do
    wsk action update $action $ACTIONDIR/$action/function.py --memory 2048 --timeout 120000 --docker somefish1/py3:$action -i
done

# Note: docker pull image somefish1/py3 -a on the invoker machine to sync images


#for action in "${actions[@]}"; do
#    wsk action delete $action -i
#done
