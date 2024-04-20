#!/usr/bin/env bash

set -x

PIDS=($(pgrep -u root python))
CPUID_START=10

for i in $(seq 0 $(( ${#PIDS[@]} - 1 )))
do
    CPUID=$(( $CPUID_START + i ))
    sudo taskset -cap $CPUID ${PIDS[$i]}
done
