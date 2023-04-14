import json, sys

names = [
    "chameleon",
    "float_operation",
    "image_processing",
    "linpack",
    "matmul",
    "ml_video_face_detection",
    "model_training",
    "pyaes",
    "video_processing",
]

file = sys.argv[1]

RUNS = 21

with open(file) as f:
    lines = f.readlines()
    assert len(lines) / len(names) == RUNS

    grouped = [
        lines[i:i+RUNS] if RUNS == 1 else lines[i:i+RUNS][1:]
        for i in range(0, len(lines), RUNS)
    ]

    grouped_times = [
        [
            float(json.loads(l)["timestamps"]["finishing_time"]) - float(json.loads(l)["timestamps"]["starting_time"])
            for l in ls
        ]
        for ls in grouped
    ]

    avgs = [
        sum(times) / len(times)
        for times in grouped_times
    ]

    for n, t in zip(names, avgs):
        print(n, t)

