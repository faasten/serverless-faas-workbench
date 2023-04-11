#!/bin/sh

set -e

export RUST_LOG=debug 
WORKBENCH_IMGS=$1
WORKBENCH_DATA=$2

if [[ -z $KERNEL ]]
then
KERNEL=resources/images/vmlinux-4.20.0
fi

if [[ -z $PYTHON ]]
then
PYTHON=rootfs/python3.ext4
fi

MEM_SIZE=2048

admin_fstools --bootstrap bootstrap-config.yml
admin_fstools --mkdir ":home:<faasten,faasten>:output" "faasten,T"

admin_fstools --blob $WORKBENCH_DATA/image/image.jpg ":home:<faasten,faasten>:image.jpg" "faasten,faasten"
admin_fstools --blob $WORKBENCH_DATA/video/SampleVideo_1280x720_10mb.mp4 ":home:<faasten,faasten>:video.mp4" "faasten,faasten"
admin_fstools --blob $WORKBENCH_DATA/model/haarcascade_frontalface_default.xml ":home:<faasten,faasten>:haar_model.xml" "faasten,faasten"


# more data setup

# chameleon
echo '{"num_of_rows": 100, "num_of_cols": 100, "metadata": 1}' | singlevm --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/chameleon.img --mem_size $MEM_SIZE

# float_operation
echo '{"n": "123", "metadata": 123}' | singlevm --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/float_operation.img --mem_size $MEM_SIZE

# image_processing
echo '{"input": ":home:<faasten,faasten>:image.jpg", "output_dir": ":home:<faasten,faaste>:output", "metadata": 123}' | singlevm --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/image_processing.img --mem_size $MEM_SIZE

# linpack
echo '{"n": "123", "metadata": 123}' | singlevm --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/linpack.img --mem_size $MEM_SIZE

# matmul
echo '{"n": "123", "metadata": 123}' | singlevm --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/matmul.img --mem_size $MEM_SIZE

# ml_video_face_detection
echo '{"input": ":home:<faasten,faasten>:video.mp4", "model": ":home:<faasten,faasten>:haar_model.xml", "output_dir": ":home:<faasten,faaste>:output", "metadata": 123}' | singlevm --kernel $KERNEL --rootfs $PYTHON --appfs ../serverless-faas-workbench/faasten/cpu-memory/ml_video_face_detection.img --mem_size $MEM_SIZE

echo '{"length_of_message": 100, "num_of_iterations": 100, "metadata": 1}' | singlevm --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/pyaes.img --mem_size $MEM_SIZE

echo '{"input_file": ":home:<faasten,faasten>:video.mp4", "output_file": ":home:<faasten,faasten>:outputs/video_processing.avi", "metadata": 123}' | singlevm --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/video_processing.img --mem_size $MEM_SIZE
