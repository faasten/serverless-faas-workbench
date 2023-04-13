#!/bin/sh

set -e

export RUST_LOG=debug 
WORKBENCH_IMGS=$1
WORKBENCH_DATA=$2
WORKBENCH_TIKV=$3

if [[ -z $KERNEL ]]
then
KERNEL=resources/images/vmlinux-4.20.0
fi

if [[ -z $PYTHON ]]
then
PYTHON=rootfs/python3.ext4
fi

SINGLEVM_PARAM="--no_odirect_root --no_odirect_app --no_odirect_diff"

MEM_SIZE=2048

VCPU_COUNT=32

# admin_fstools $WORKBENCH_TIKV --bootstrap bootstrap-config.yml
admin_fstools $WORKBENCH_TIKV --mkdir ":home:<faasten,faasten>:output" "faasten,T"

admin_fstools $WORKBENCH_TIKV --blob $WORKBENCH_DATA/image/image.jpg ":home:<faasten,faasten>:image.jpg" "faasten,faasten"
admin_fstools $WORKBENCH_TIKV --blob $WORKBENCH_DATA/video/SampleVideo_1280x720_10mb.mp4 ":home:<faasten,faasten>:video.mp4" "faasten,faasten"
admin_fstools $WORKBENCH_TIKV --blob $WORKBENCH_DATA/model/haarcascade_frontalface_default.xml ":home:<faasten,faasten>:haar_model.xml" "faasten,faasten"
admin_fstools $WORKBENCH_TIKV --blob $WORKBENCH_DATA/amzn_fine_food_reviews/reviews100mb.csv ":home:<faasten,faasten>:reviews100mb.csv" "faasten,faasten"


# more data setup

# chameleon
echo -e '{"num_of_rows": 100, "num_of_cols": 100, "metadata": 1}\n{"num_of_rows": 100, "num_of_cols": 100, "metadata": 1}' | singlevm $SINGLEVM_PARAM $WORKBENCH_TIKV --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/chameleon.img --mem_size $MEM_SIZE --vcpu_count $VCPU_COUNT

# float_operation
echo -e '{"n": "123", "metadata": 123}\n{"n": "123", "metadata": 123}' | singlevm $SINGLEVM_PARAM $WORKBENCH_TIKV --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/float_operation.img --mem_size $MEM_SIZE --vcpu_count $VCPU_COUNT

# image_processing
echo -e '{"input": ":home:<faasten,faasten>:image.jpg", "output_dir": ":home:<faasten,faasten>:output", "metadata": 123}\n{"input": ":home:<faasten,faasten>:image.jpg", "output_dir": ":home:<faasten,faasten>:output", "metadata": 123}' | singlevm $SINGLEVM_PARAM $WORKBENCH_TIKV --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/image_processing.img --mem_size $MEM_SIZE --vcpu_count $VCPU_COUNT

# linpack
echo -e '{"n": "123", "metadata": 123}\n{"n": "123", "metadata": 123}' | singlevm $SINGLEVM_PARAM $WORKBENCH_TIKV --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/linpack.img --mem_size $MEM_SIZE --vcpu_count $VCPU_COUNT

# matmul
echo -e '{"n": "123", "metadata": 123}\n{"n": "123", "metadata": 123}' | singlevm $SINGLEVM_PARAM $WORKBENCH_TIKV --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/matmul.img --mem_size $MEM_SIZE --vcpu_count $VCPU_COUNT

# ml_video_face_detection
echo -e '{"input": ":home:<faasten,faasten>:video.mp4", "output_dir": ":home:<faasten,faasten>:output", "model": ":home:<faasten,faasten>:haar_model.xml", "metadata": 123}\n{"input": ":home:<faasten,faasten>:video.mp4", "output_dir": ":home:<faasten,faasten>:output", "model": ":home:<faasten,faasten>:haar_model.xml", "metadata": 123}' | singlevm $SINGLEVM_PARAM $WORKBENCH_TIKV --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/ml_video_face_detection.img --mem_size $MEM_SIZE --vcpu_count $VCPU_COUNT

# model_training
echo -e '{"dataset": ":home:<faasten,faasten>:reviews100mb.csv", "output": ":home:<faasten,faasten>:output:lr_model.pk", "metadata": 123}\n{"dataset": ":home:<faasten,faasten>:reviews100mb.csv", "output": ":home:<faasten,faasten>:output:lr_model.pk", "metadata": 123}' | singlevm $SINGLEVM_PARAM $WORKBENCH_TIKV --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/model_training.img --mem_size $MEM_SIZE --vcpu_count $VCPU_COUNT

# pyaes
echo -e '{"length_of_message": 100, "num_of_iterations": 100, "metadata": 1}\n{"length_of_message": 100, "num_of_iterations": 100, "metadata": 1}' | singlevm $SINGLEVM_PARAM $WORKBENCH_TIKV --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/pyaes.img --mem_size $MEM_SIZE --vcpu_count $VCPU_COUNT

# video_processing
echo -e '{"input_file": ":home:<faasten,faasten>:video.mp4", "output_file": ":home:<faasten,faasten>:output:video_processing.avi", "metadata": 123}\n{"input_file": ":home:<faasten,faasten>:video.mp4", "output_file": ":home:<faasten,faasten>:output:video_processing.avi", "metadata": 123}' | singlevm $SINGLEVM_PARAM $WORKBENCH_TIKV --kernel $KERNEL --rootfs $PYTHON --appfs $WORKBENCH_IMGS/video_processing.img --mem_size $MEM_SIZE --vcpu_count $VCPU_COUNT
