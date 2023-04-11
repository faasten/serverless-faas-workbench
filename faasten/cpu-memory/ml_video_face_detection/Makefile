all: out

out: pyproject.toml workload.py
	apk add py3-opencv
	mkdir -p out/lib
	cp `python3 -c "import cv2; print(cv2.__file__)"` out/
	ldd out/cv2.*.so  2> /dev/null | awk 'NF == 4 { system("cp " $$3 " out/lib/") }'
	MAKEFLAGS="-j12" PYTHONPATH=out/ pip install . -t out
	cp workload.py out/
