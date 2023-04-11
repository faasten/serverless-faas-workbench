#!/bin/sh

IID=$(docker build -q .)
cidfile=$(mktemp --dry-run)
docker run --cidfile="$cidfile" -w /app -v "$(realpath $1)":/src "$IID" sh -c 'cp -r /src/* .; make'
tmpdir=$(mktemp -d)
docker export `cat $cidfile` | tar -C "$tmpdir" -x app/out --strip-components 2

gensquashfs --pack-dir "$tmpdir" "$2"
rm -Rf "$cidfile" "$tmpdir"
