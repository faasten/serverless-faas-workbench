from time import time
from PIL import Image
import shutil
import json
import ops
import re

from syscalls import ResponseDict

FILE_NAME_INDEX = 1

def path(path: str):
    return list(filter(None, re.split(':<|>:|:', path)))

def image_processing(file_name, image_path):
    path_list = []
    start = time()
    with Image.open(image_path) as image:
        tmp = image
        path_list += ops.flip(image, file_name)
        path_list += ops.rotate(image, file_name)
        path_list += ops.filter(image, file_name)
        path_list += ops.gray_scale(image, file_name)
        path_list += ops.resize(image, file_name)

    latency = time() - start
    print("PATH_LIST", path_list)
    return latency, path_list

def main(event):
    latencies = {}
    timestamps = {}
    timestamps["starting_time"] = time()

    object_key = event['input']
    output_dir = event['output_dir']
    metadata = event['metadata']

    download_path = path(object_key)
    output_dir    = path(output_dir)

    with sc.root().open_at(download_path) as blob:
        with blob.get() as blob:
            image_processing_latency, path_list = image_processing("image.jpg", blob)
            latencies["function_execution"] = image_processing_latency
            print("PATH_LIST OUTSIDE", path_list)

            start = time()
            for upload_path in path_list:
                local_path = upload_path
                name = upload_path.split("/")[-1]
                with sc.create_blob() as newblob:
                    with open(local_path, "rb") as local_fp:
                        shutil.copyfileobj(local_fp, newblob)
                    bn = newblob.finalize(b'')
                    with sc.root().open_at(output_dir) as out_dir:
                        out_dir.link(newblob, name)
            upload_latency = time() - start
            latencies["upload_data"] = upload_latency
            timestamps["finishing_time"] = time()

        return ResponseDict({"latencies": latencies, "timestamps": timestamps, "metadata": metadata})

def handle(syscall, payload, **kwarg):
    global sc
    sc = syscall
    return main(json.loads(payload))

if __name__ == "__main__":
    print(main({'n': 100, 'metadata': 1}))
