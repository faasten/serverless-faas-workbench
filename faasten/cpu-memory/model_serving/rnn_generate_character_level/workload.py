import os
import pickle
import numpy as np
import torch
import rnn

from time import time


tmp = "/tmp/"

"""
Language
 - Italian, German, Portuguese, Chinese, Greek, Polish, French
 - English, Spanish, Arabic, Crech, Russian, Irish, Dutch
 - Scottish, Vietnamese, Korean, Japanese
"""


def main(event):
    latencies = {}
    timestamps = {}
    
    timestamps["starting_time"] = time()

    language = event['language']
    start_letters = event['start_letters']
    model_parameter_object_key = event['model_parameter_object_key']  # example : rnn_params.pkl
    model_object_key = event['model_object_key']  # example : rnn_model.pth
    metadata = event['metadata']

    # Check if models are available
    # Download model from S3 if model is not already present
    parameter_path = tmp + "parameters.pkl"
    model_path = tmp + "model.pth"

    start = time()

    with sc.fs_openblob(model_parameter_object_key) as parameter_blob:
        with open(parameter_path, "wb+") as local_fp:
            shutil.copyfileobj(parameter_blob, local_fp)

    with sc.fs_openblob(model_object_key) as model_blob:
        with open(model_path, "wb+") as local_fp:
            shutil.copyfileobj(model_blob, local_fp)


    download_data = time() - start
    latencies["download_data"] = download_data

    start = time()

    with open(parameter_path, 'rb') as pkl:
        params = pickle.load(pkl)

    all_categories = params['all_categories']
    n_categories = params['n_categories']
    all_letters = params['all_letters']
    n_letters = params['n_letters']

    rnn_model = rnn.RNN(n_letters, 128, n_letters, all_categories, n_categories, all_letters, n_letters)
    rnn_model.load_state_dict(torch.load(model_path))
    rnn_model.eval()

    output_names = list(rnn_model.samples(language, start_letters))

    latency = time() - start
    latencies["function_execution"] = latency
    timestamps["finishing_time"] = time()

    return {"output_names": output_names, "latencies": latencies, "timestamps": timestamps, "metadata": metadata}

def handle(args, syscall):
    global sc
    sc = syscall
    return main(args)
