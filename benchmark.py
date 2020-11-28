import timeit  # from https://pypi.org/project/memory-profiler/
from memory_profiler import memory_usage
from global_alignment_functions import *
import os, glob, psutil
import subprocess

def mem_benchmark(a, b, alignment):
    """Benchmark one run of given alignment with strings a and b."""
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

'''
Test a function based on real data comparisons in "./test_strings/real_comp".
    Data in text files is formatted "string1 \n string2"
    @func_name = string name of Global Alignment function to test
    Output is "filename: runtime (secs)"
'''
def test_func_data(DATAPATH, func_name):
    SETUP_CODE = '''
from global_alignment_functions import FUNCTION_TEST, get_cost
  '''
    SETUP_CODE = SETUP_CODE.replace("FUNCTION_TEST", func_name)
    TEST_TEMPLATE = 'FUNCTION_TEST("s1","s2", get_cost)'
    TEST_TEMPLATE = TEST_TEMPLATE.replace("FUNCTION_TEST", func_name)

    data = {} # {}

    for filename in glob.glob(os.path.join(DATAPATH, '*.txt')):
        with open(filename, 'r') as f:
            TEST_CODE = TEST_TEMPLATE
            str1 = f.readline()
            str2 = f.readline()

            length_bp = len(str2) -1
            if len(str1) > len(str2):
                length_bp = len(str1) -1
            
            TEST_CODE = TEST_CODE.replace("s1", str1[:-1])
            TEST_CODE = TEST_CODE.replace("s2", str2[:-1])

            '''
            Use replaced TEST_CODE in order to get time data with timeit package
            '''
            t = timeit.Timer(setup=SETUP_CODE, stmt=TEST_CODE)

            # TODO: UNCOMMENT FOR MORE ACCURATE DATA
            # sec_time = t.timeit(100000)/100000  # Average time over 100,000 runs
            sec_time = t.timeit(10) # to test benchmarking is working 

            mem_use = avg_mem_benchmark(1, str1[:-1], str2[:-1], func_name)

            data[os.path.basename(filename)] = {"runtime": sec_time, "mem_use": mem_use, "length": length_bp}
    return data

# if __name__ == '__main__':
#     # test real data
#     #test_func_data("./test_strings/real_comp", "dp")
#     #test_func_data("./test_strings/real_comp", "hirschberg")

#     test_func_data("./test_strings/artificial_comp/10percent", "dp")
#     test_func_data("./test_strings/artificial_comp/10percent", "hirschberg")
