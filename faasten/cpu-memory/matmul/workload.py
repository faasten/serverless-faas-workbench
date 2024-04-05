import numpy as np
from time import time
import json

from syscalls import ResponseDict

def matmul(n):
    A = np.random.rand(n, n)
    B = np.random.rand(n, n)

    start = time()
    C = np.matmul(A, B)
    latency = time() - start
    return latency


def main(event):
    latencies = {}
    timestamps = {}

    timestamps["starting_time"] = time()
    n = int(event['n'])
    metadata = event['metadata']
    result = matmul(n)
    latencies["function_execution"] = result
    timestamps["finishing_time"] = time()

    return ResponseDict({"latencies": latencies, "timestamps": timestamps, "metadata": metadata})

def handle(syscall, payload, **kwarg):
    return main(json.loads(payload))

if __name__ == "__main__":
    print(main({'n': 100, 'metadata': 1}))
