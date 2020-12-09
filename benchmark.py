import timeit  # from https://pypi.org/project/memory-profiler/
from memory_profiler import memory_usage
from global_alignment_functions import *
import os, glob, psutil
import subprocess

def mem_benchmark(a, b, alignment):
    """Benchmark memory of one run of given alignment."""
    # If you do not run python using the python3 command, change below line to
    # the command that you do use.
    out = subprocess.run(['python3', 'mem_benchmark.py', a, b, alignment],
                         capture_output = True,
                         text = True)
    if out.stderr:
        raise ValueError(out.stderr)
    return float(out.stdout)

def avg_mem_benchmark(iters, a, b, alignment):
    """Takes the average memory usage of n=iters runs."""
    total = 0
    for i in range(iters):
        total += mem_benchmark(a, b, alignment)
    avg = total / iters
    return avg

def avg_time_benchmark(iters, a, b, alignment):
    """Benchmark time of one run of given alignment."""
    setup = f'from global_alignment_functions import {alignment}, get_cost'
    stmt = f'{alignment}("{a}", "{b}", get_cost)'
    t = timeit.Timer(setup=setup, stmt=stmt)
    sec_time = t.timeit(iters) / iters
    return sec_time

'''
Test a function based on real data comparisons in "./test_strings/real_comp".
    Data in text files is formatted "string1 \n string2"
    @func_name = string name of Global Alignment function to test
    Output is "filename: runtime (secs)"
'''
def test_func_data(DATAPATH, func_name, iters=10):
    data = {}

    for filename in glob.glob(os.path.join(DATAPATH, '*.txt')):
        with open(filename, 'r') as f:
            str1 = f.readline()[:-1]
            str2 = f.readline()[:-1]
            length_bp = max(len(str1), len(str2))
            
            runtime = avg_time_benchmark(iters, str1, str2, func_name)
            mem_use = avg_mem_benchmark(iters, str1, str2, func_name)

            data[os.path.basename(filename)] = {"runtime": runtime,
                                                "mem_use": mem_use,
                                                "length": length_bp}
    return data

if __name__ == '__main__':
    funcs = ['dp', 'hirschberg']
    filepath = './test_strings/temp_test/'
    for func in funcs:
        print(func)
        print(test_func_data(filepath, func, iters=1))
#     # test real data
     #test_func_data("./test_strings/real_comp", "dp")
     #test_func_data("./test_strings/real_comp", "hirschberg")

     #test_func_data("./test_strings/artificial_comp/10percent", "dp")
     #test_func_data("./test_strings/artificial_comp/10percent", "hirschberg")

