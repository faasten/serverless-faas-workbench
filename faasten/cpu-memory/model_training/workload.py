from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

import pandas as pd
from time import time
import re
import io
import shutil
import json

from syscalls import ResponseDict

cleanup_re = re.compile('[^a-z]+')
tmp = '/tmp/'

def path(path: str):
    return list(filter(None, re.split(':<|>:|:', path)))

def cleanup(sentence):
    sentence = sentence.lower()
    sentence = cleanup_re.sub(' ', sentence).strip()
    return sentence

def main(event):
    latencies = {}
    timestamps = {}

    timestamps["starting_time"] = time()

    dataset_object_key = event['dataset'] #object_key
    output_path = event['output']  # example : lr_model.pk
    metadata = event['metadata']

    local_dataset_path = "/tmp/dataset.csv"

    start = time()
    with sc.root().open_at(path(dataset_object_key)) as input_blob:
        with input_blob.get() as input_blob:
            with open(local_dataset_path, "wb+") as local_fp:
                shutil.copyfileobj(input_blob, local_fp)

    download_data = time() - start
    latencies["download_data"] = download_data

    start = time()
    df = pd.read_csv(local_dataset_path)
    df['train'] = df['Text'].apply(cleanup)

    tfidf_vector = TfidfVectorizer(min_df=100).fit(df['train'])

    train = tfidf_vector.transform(df['train'])

    model = LogisticRegression()
    model.fit(train, df['Score'])
    function_execution = time() - start
    latencies["function_execution"] = function_execution

    model_file_path = '/tmp/model.pk'
    joblib.dump(model, model_file_path)

    start = time()
    with sc.create_blob() as newblob:
        with open(model_file_path, "rb") as local_fp:
            shutil.copyfileobj(local_fp, newblob)
        bn = newblob.finalize(b'')
        output_path = path(output_path)
        with sc.root().open_at(output_path[:-1]) as out_dir:
            out_dir.link(newblob, output_path[-1])
    upload_data = time() - start
    latencies["upload_data"] = upload_data
    timestamps["finishing_time"] = time()

    return ResponseDict({"latencies": latencies, "timestamps": timestamps, "metadata": metadata})

def handle(syscall, payload, **kwarg):
    global sc
    sc = syscall
    return main(json.loads(payload))
