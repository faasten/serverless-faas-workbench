FROM openwhisk/actionloop-python-v3.6-ai:1.16.0

COPY main.py .
COPY cpu-memory/model_training/* .

RUN pip3 install --upgrade pip &&\
    pip3 install --no-cache-dir -r requirements.txt &&\
    ln -sf /usr/bin/python3 /usr/local/bin/python

ENTRYPOINT ["/usr/local/bin/python", "main.py"]
