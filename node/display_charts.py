import json
import sys
from typing import Dict, List, Union
import asciichartpy as ascii_chart
import os

def load_data(file_path: str) -> List[Dict[str, Union[float, int]]]:
    data = []
    with open(file_path, "r") as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                # Skip the invalid JSON object
                pass
    return data

def plot_data(data, title):
    os.system('cls' if os.name == 'nt' else 'clear')
    elapsed_times = [x["elapsed_time"] for x in data]
    cpu_percents = [x["cpu_percent"] for x in data]
    memory_percents = [x["memory_percent"] for x in data]

    print(f"{title} - Time")
    print(ascii_chart.plot(elapsed_times, {'height': 10}))

    print(f"{title} - CPU Usage")
    print(ascii_chart.plot(cpu_percents, {'height': 10}))

    print(f"{title} - Memory Usage")
    print(ascii_chart.plot(memory_percents, {'height': 10}))

output_file = sys.argv[1]
language = sys.argv[2]
num_tests = int(sys.argv[3])

data = load_data(output_file)
title = f"{language} Benchmark"
plot_data(data, title)