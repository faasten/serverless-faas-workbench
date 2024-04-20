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


RUNS = 21

def get_result(file, names, runs):
    with open(file) as f:
        jsons = json.load(f)
        print(len(jsons), runs)
        assert len(jsons) % runs == 0
        n = len(jsons) // runs

        grouped = [
            jsons[i:i+runs] if runs == 1 else jsons[i:i+runs][1:]
            for i in range(0, len(jsons), runs)
        ]

        grouped_times = [
            sorted([
                j['timestamps']['finishing_time'] - j['timestamps']['starting_time']
                for j in g
            ])[1:-1]
            for g in grouped
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
    try:
        runs = int(sys.argv[3])
    except:
        runs = RUNS
    if type == "all":
        ns = names
    else:
        ns = [ type ]
    get_result(file, ns, runs)



