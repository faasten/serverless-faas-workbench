#!/bin/sh

set -e


for d in */ ; do
  rm -f `basename $d`.img
  if [ -f $d/Makefile ]; then
    ./docker_build.sh "$d" $(basename "$d").img
  else
    gensquashfs --pack-dir "$d" $(basename "$d").img
  fi
done
