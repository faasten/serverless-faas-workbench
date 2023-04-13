import json
with open('faastenresult') as f:
    results = json.load(f)
for result in results:
    ts = result["timestamps"]
    start = ts["starting_time"]
    end = ts["finishing_time"]
    print(end-start)
