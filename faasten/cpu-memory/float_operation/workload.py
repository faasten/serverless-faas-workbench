import math
import json
from time import time

from syscalls import ResponseDict


def float_operations(n):
    start = time()
    for i in range(0, n):
        sin_i = math.sin(i)

        cos_i = math.cos(i)
        sqrt_i = math.sqrt(i)
    latency = time() - start
    return latency


def main(event):
    latencies = {}
    timestamps = {}
    timestamps["starting_time"] = time()
    n = int(event['n'])
    metadata = event['metadata']
    latency = float_operations(n)
    latencies["function_execution"] = latency
    timestamps["finishing_time"] = time()
    return ResponseDict({"latencies": latencies, "timestamps": timestamps, "metadata": metadata})

def handle(syscall, payload, **kwarg):
    global sc
    sc = syscall
    return main(json.loads(payload))

if __name__ == "__main__":
    print(main({'n': 100, 'metadata': 1}))
