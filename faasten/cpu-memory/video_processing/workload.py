import tempfile
from time import time
import cv2
import shutil

tmp = "/tmp/"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2

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
    with sc.fs_openblob(input_file) as input_blob:
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
            sc.fs_linkblob(output_file, bn)
        upload_latency = time() - start
        latencies["upload_data"] = upload_latency
        timestamps["finishing_time"] = time()

        return {"latencies": latencies, "timestamps": timestamps, "metadata": metadata}

def handle(args, syscall):
    global sc
    sc = syscall
    return main(args)

if __name__ == "__main__":
    print(main({'output_file': 'output.avi', 'input_file': '../../../dataset/video/SampleVideo_1280x720_10mb.mp4', 'metadata': 1}))
