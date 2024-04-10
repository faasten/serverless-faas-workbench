#!/usr/bin/env bash

ACTIONDIR=$(dirname $(realpath $0))/cpu-memory
actions=($(ls $ACTIONDIR))

if [[ -z "$1" ]]
then
   for action in "${actions[@]}"; do
       docker build -t py3:$action -f $ACTIONDIR/$action/Dockerfile .
   done
   exit 0
fi

action=$1
docker build -t py3:$action -f $ACTIONDIR/$action/Dockerfile .
