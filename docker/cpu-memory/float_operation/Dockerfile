FROM openwhisk/python3action:95f1358

COPY main.py .
COPY cpu-memory/float_operation/function.py .

ENTRYPOINT ["/usr/local/bin/python", "main.py"]