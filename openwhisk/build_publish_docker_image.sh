#!/bin/bash -x

ACTIONDIR=$(dirname $(realpath $0))/cpu-memory
actions=($(ls $ACTIONDIR))

if [[ -z "$1" ]]
then
    for action in "${actions[@]}"; do
        docker build -t py3:$action $ACTIONDIR/$action
        docker tag py3:$action somefish1/py3:$action
        docker push somefish1/py3:$action
    done
    exit 0
fi

action=$1
docker build -t py3:$action $ACTIONDIR/$action
docker tag py3:$action somefish1/py3:$action
docker push somefish1/py3:$action
