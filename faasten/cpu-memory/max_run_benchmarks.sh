#!/usr/bin/env bash

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

SINGLEVM_PARAM="--no-odirect-root --no-odirect-app --no-odirect-diff"

MEM_SIZE=2048

VCPU_COUNT=32

RUNS=21

# admin_fstools --tikv $WORKBENCH_TIKV bootstrap bootstrap-config.yml
admin_fstools --tikv $WORKBENCH_TIKV mkdir ":home:<faasten,faasten>:output" "faasten,T"

admin_fstools --tikv $WORKBENCH_TIKV create-blob $WORKBENCH_DATA/image/image.jpg ":home:<faasten,faasten>:image.jpg" "faasten,faasten"
admin_fstools --tikv $WORKBENCH_TIKV create-blob $WORKBENCH_DATA/video/SampleVideo_1280x720_10mb.mp4 ":home:<faasten,faasten>:video.mp4" "faasten,faasten"
admin_fstools --tikv $WORKBENCH_TIKV create-blob $WORKBENCH_DATA/model/haarcascade_frontalface_default.xml ":home:<faasten,faasten>:haar_model.xml" "faasten,faasten"
admin_fstools --tikv $WORKBENCH_TIKV create-blob $WORKBENCH_DATA/amzn_fine_food_reviews/reviews100mb.csv ":home:<faasten,faasten>:reviews100mb.csv" "faasten,faasten"


# more data setup

# chameleon
singlevm $SINGLEVM_PARAM \
         --tikv $WORKBENCH_TIKV \
         --kernel $KERNEL \
         --rootfs $PYTHON \
         --appfs $WORKBENCH_IMGS/chameleon.img \
         --memory $MEM_SIZE \
         --vcpu $VCPU_COUNT < \
         <(yes '{"num_of_rows": 100, "num_of_cols": 100, "metadata": 1}' | head -n $RUNS)

# float_operation
singlevm $SINGLEVM_PARAM \
         --tikv $WORKBENCH_TIKV \
         --kernel $KERNEL \
         --rootfs $PYTHON \
         --appfs $WORKBENCH_IMGS/float_operation.img \
         --memory $MEM_SIZE \
         --vcpu $VCPU_COUNT < \
         <(yes '{"n": "123", "metadata": 123}\n{"n": "123", "metadata": 123}' | head -n $RUNS)

# image_processing
singlevm $SINGLEVM_PARAM \
         --tikv $WORKBENCH_TIKV \
         --kernel $KERNEL \
         --rootfs $PYTHON \
         --appfs $WORKBENCH_IMGS/image_processing.img \
         --memory $MEM_SIZE \
         --vcpu $VCPU_COUNT < \
         <(yes '{"input": ":home:<faasten,faasten>:image.jpg", "output_dir": ":home:<faasten,faasten>:output", "metadata": 123}' | head -n $RUNS)

# linpack
singlevm $SINGLEVM_PARAM \
         --tikv $WORKBENCH_TIKV \
         --kernel $KERNEL \
         --rootfs $PYTHON \
         --appfs $WORKBENCH_IMGS/linpack.img \
         --memory $MEM_SIZE \
         --vcpu $VCPU_COUNT < \
         <(yes '{"n": "123", "metadata": 123}' | head -n $RUNS)

# matmul
singlevm $SINGLEVM_PARAM \
         --tikv $WORKBENCH_TIKV \
         --kernel $KERNEL \
         --rootfs $PYTHON \
         --appfs $WORKBENCH_IMGS/matmul.img \
         --memory $MEM_SIZE \
         --vcpu $VCPU_COUNT < \
         <(yes '{"n": "123", "metadata": 123}' | head -n $RUNS)

# ml_video_face_detection
singlevm $SINGLEVM_PARAM \
         --tikv $WORKBENCH_TIKV \
         --kernel $KERNEL \
         --rootfs $PYTHON \
         --appfs $WORKBENCH_IMGS/ml_video_face_detection.img \
         --memory $MEM_SIZE \
         --vcpu $VCPU_COUNT < \
         <(yes '{"input": ":home:<faasten,faasten>:video.mp4", "output_dir": ":home:<faasten,faasten>:output", "model": ":home:<faasten,faasten>:haar_model.xml", "metadata": 123}' | head -n $RUNS)

# model_training
singlevm $SINGLEVM_PARAM \
         --tikv $WORKBENCH_TIKV \
         --kernel $KERNEL \
         --rootfs $PYTHON \
         --appfs $WORKBENCH_IMGS/model_training.img \
         --memory $MEM_SIZE \
         --vcpu $VCPU_COUNT < \
         <(yes '{"dataset": ":home:<faasten,faasten>:reviews100mb.csv", "output": ":home:<faasten,faasten>:output:lr_model.pk", "metadata": 123}' | head -n $RUNS)

# pyaes
singlevm $SINGLEVM_PARAM \
         --tikv $WORKBENCH_TIKV \
         --kernel $KERNEL \
         --rootfs $PYTHON \
         --appfs $WORKBENCH_IMGS/pyaes.img \
         --memory $MEM_SIZE \
         --vcpu $VCPU_COUNT < \
         <(yes '{"length_of_message": 100, "num_of_iterations": 100, "metadata": 1}' | head -n $RUNS)

# video_processing
singlevm $SINGLEVM_PARAM \
         --tikv $WORKBENCH_TIKV \
         --kernel $KERNEL \
         --rootfs $PYTHON \
         --appfs $WORKBENCH_IMGS/video_processing.img \
         --memory $MEM_SIZE \
         --vcpu $VCPU_COUNT < \
         <(yes '{"input_file": ":home:<faasten,faasten>:video.mp4", "output_file": ":home:<faasten,faasten>:output:video_processing.avi", "metadata": 123}' | head -n $RUNS)
