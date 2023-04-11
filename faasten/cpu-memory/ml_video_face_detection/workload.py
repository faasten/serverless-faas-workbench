from time import time
import cv2
import shutil

tmp = "/tmp/"
FILE_NAME_INDEX = 0
FILE_PATH_INDEX = 2


def video_processing(object_key, video_path, model_path):
    file_name = object_key.split(".")[FILE_NAME_INDEX]
    result_file_path = tmp+file_name+'-detection.mp4'

    video = cv2.VideoCapture(video_path)

    width = int(video.get(3))
    height = int(video.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_file_path, fourcc, 20.0, (width, height))

    face_cascade = cv2.CascadeClassifier(model_path)

    start = time()
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            #print("Found {0} faces!".format(len(faces)))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            out.write(frame)
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
    
    download_path = event['input']
    output_dir = event['output_dir']
    model_path = event['model'] # example : haarcascade_frontalface_default.xml

    metadata = event['metadata']

    local_input_path = "/tmp/input.mp4"
    local_model_path = "/tmp/input.xml"

    with sc.fs_openblob(download_path) as input_blob:
        with open(local_input_path, "wb+") as local_fp:
            shutil.copyfileobj(input_blob, local_fp)
    with sc.fs_openblob(model_path) as model_blob:
        with open(local_model_path, "wb+") as local_fp:
            shutil.copyfileobj(model_blob, local_fp)

    function_execution, upload_path = video_processing("output.foo", local_input_path, local_model_path)
    latencies["function_execution"] = function_execution

    start = time()
    with sc.create_blob() as newblob:
        with open(upload_path, "rb") as local_fp:
            shutil.copyfileobj(local_fp, newblob)
        bn = newblob.finalize(b'')
        output_path = ":".join([output_dir, upload_path.split("/")[-1]])
        sc.fs_linkblob(output_path, bn)

    upload_data = time() - start
    latencies["upload_data"] = upload_data
    timestamps["finishing_time"] = time()

    return {"latencies": latencies, "timestamps": timestamps, "metadata": metadata}

def handle(args, syscall):
    global sc
    sc = syscall
    return main(args)
