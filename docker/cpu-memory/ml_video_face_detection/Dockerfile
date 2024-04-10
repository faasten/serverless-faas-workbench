FROM openwhisk/actionloop-python-v3.6-ai:1.16.0

COPY main.py .
COPY cpu-memory/ml_video_face_detection/* .

RUN pip3 install --upgrade pip &&\
    pip3 install --no-cache-dir -r requirements.txt &&\
    ln -sf /usr/bin/python3 /usr/local/bin/python

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libsm6 \
    libxrender1 \
    libfontconfig1 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/local/bin/python", "main.py"]