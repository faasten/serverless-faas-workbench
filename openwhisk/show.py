import json, sys, numpy

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

def process(file, names):
    with open(file) as f:
        jsons = json.load(f)
        assert len(jsons) % RUNS == 0
        n = len(jsons) // RUNS

        grouped = [
            jsons[i:len(jsons):n] if RUNS == 1 else jsons[i:len(jsons):n][1:]
            for i in range(n)
        ]

        grouped_times = [
            [
                j['timestamps']['finishing_time'] - j['timestamps']['starting_time']
                for j in g
            ]
            for g in grouped
        ]

        avgs = [
            sum(times) / len(times)
            for times in grouped_times
        ]

        for n, ts in zip(names, grouped_times):
            avg = sum(ts) / len(ts)
            std = numpy.std(ts)
            print(n, avg, std)


process(file, names)



