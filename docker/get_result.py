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

names_noml = [
    "chameleon",
    "float_operation",
    "image_processing",
    "linpack",
    "matmul",
    # "ml_video_face_detection",
    # "model_training",
    "pyaes",
    "video_processing",
]


RUNS = 21

def get_result(file, names):
    with open(file) as f:
        lines = f.readlines()
        assert len(lines) / len(names) == RUNS

        grouped = [
            lines[i:i+RUNS] if RUNS == 1 else lines[i:i+RUNS][1:]
            for i in range(0, len(lines), RUNS)
        ]

        grouped_times = [
            [
                float(json.loads(l)["timestamps"]["finishing_time"])
                - float(json.loads(l)["timestamps"]["starting_time"])
                for l in ls
            ]
            for ls in grouped
        ]

        # avgs = [
        #     sum(times) / len(times)
        #     for times in grouped_times
        # ]

        for n, ts in zip(names, grouped_times):
            avg = sum(ts) / len(ts)
            std = numpy.std(ts)
            print(n, avg, std)

if __name__ == "__main__":
    type = sys.argv[1]
    file = sys.argv[2]
    if type == "all":
        get_result(file, names)
    elif type == "noml":
        get_result(file, names_noml)
    else:
        get_result(file, [type])

