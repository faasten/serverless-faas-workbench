import tempfile
from time import time
import cv2
import shutil
import json
import re

from syscalls import ResponseDict

tmp = "/tmp/"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2

def path(path: str):
    return list(filter(None, re.split(':<|>:|:', path)))

def video_processing(result_file_path, video_path):
    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    start = time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            with tempfile.NamedTemporaryFile(suffix=".jpg") as fp:
                tmp_file_path = fp.name
                cv2.imwrite(tmp_file_path, gray_frame)
                gray_frame = cv2.imread(tmp_file_path)
                out.write(gray_frame)
        else:
            break

    latency = time() - start

    video.release()
    out.release()
    return latency, result_file_path

def main(event):
    latencies = {}
    timestamps = {}

    timestamps["starting_time"] = time()
    output_file = event['output_file']
    input_file = event['input_file']
    metadata = event['metadata']

    download_path = tmp + "file.mp4"
    start = time()

    with sc.root().open_at(path(input_file)) as input_blob:
        with input_blob.get() as input_blob:
            with open(download_path, "wb+") as local_fp:
                shutil.copyfileobj(input_blob, local_fp)
    download_latency = time() - start
    latencies["download_data"] = download_latency

    with tempfile.NamedTemporaryFile(suffix=".avi") as result_file:
        video_processing_latency, upload_path = video_processing(result_file.name, download_path)
        latencies["function_execution"] = video_processing_latency

        start = time()
        #syscall.write_file(output_file, result_file)
        with sc.create_blob() as newblob:
            with open(upload_path, "rb") as local_fp:
                shutil.copyfileobj(local_fp, newblob)
            bn = newblob.finalize(b'')

            output_path = path(output_file)
            with sc.root().open_at(output_path[:-1]) as out_dir:
                out_dir.link(newblob, output_path[-1])
        upload_latency = time() - start
        latencies["upload_data"] = upload_latency
        timestamps["finishing_time"] = time()

        return ResponseDict({"latencies": latencies, "timestamps": timestamps, "metadata": metadata})

def handle(syscall, payload, **kwarg):
    global sc
    sc = syscall
    return main(json.loads(payload))

if __name__ == "__main__":
    print(main({'output_file': 'output.avi', 'input_file': '../../../dataset/video/SampleVideo_1280x720_10mb.mp4', 'metadata': 1}))
