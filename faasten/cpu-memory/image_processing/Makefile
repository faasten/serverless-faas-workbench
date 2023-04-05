all: out

out: requirements.txt workload.py
	pip install -r requirements.txt -t out
	pip install . -t out
	cp workload.py out/
