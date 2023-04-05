from time import time
from PIL import Image
import shutil

import ops

FILE_NAME_INDEX = 1


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

    download_path = object_key
    with sc.fs_openblob(download_path) as blob:
        image_processing_latency, path_list = image_processing("image.jpg", blob)
        latencies["function_execution"] = image_processing_latency
        print("PATH_LIST OUTSIDE", path_list)

        start = time()
        for upload_path in path_list:
            local_path = upload_path
            upload_path = ":".join([output_dir, upload_path.split("/")[-1]])
            with sc.create_blob() as newblob:
                with open(local_path, "rb") as local_fp:
                    shutil.copyfileobj(local_fp, newblob)
                bn = newblob.finalize(b'')
                print(upload_path)
                print(sc.fs_linkblob(upload_path, bn))
        upload_latency = time() - start
        latencies["upload_data"] = upload_latency
        timestamps["finishing_time"] = time()

        return {"latencies": latencies, "timestamps": timestamps, "metadata": metadata}

def handle(args, syscall):
    global sc
    sc = syscall
    return main(args)

if __name__ == "__main__":
    print(main({'n': 100, 'metadata': 1}))
