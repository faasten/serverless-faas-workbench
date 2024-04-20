# FROM openwhisk/python3action:95f1358
FROM faasten:base

COPY main.py .
COPY cpu-memory/chameleon/* ./

RUN apk add bash python3 python3-dev py3-setuptools py3-protobuf #py3-opencv py3-scikit-learn py3-pandas git cmake

ENV PYTHON python3.10

RUN apk add --update py-pip
RUN pip install -r requirements.txt

# ENTRYPOINT ["/usr/local/bin/python", "main.py"]
ENTRYPOINT ["python3", "main.py"]