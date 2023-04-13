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
mode = sys.argv[2] if len(sys.argv) >= 3 else ''

i = 0
with open(file) as f:
    lines = [l for i, l in enumerate(f.readlines()) if mode != 'warm' or i % 2 == 1]
    for l in lines:
        try:
            obj = json.loads(l)
            ts = obj["timestamps"]
            print(names[i], float(ts["finishing_time"]) - float(ts["starting_time"]))
            i += 1
        except:
            pass

