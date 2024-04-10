FROM openwhisk/python3action:95f1358

COPY main.py .
COPY cpu-memory/chameleon/* ./

RUN apk add --update py-pip
RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/local/bin/python", "main.py"]