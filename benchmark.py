import timeit  # from https://pypi.org/project/memory-profiler/
from memory_profiler import memory_usage
from global_alignment_functions import *
import os, glob, psutil


def test_run(codestring):
    exec(codestring)

def get_memory_use():
    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0]/2.**30  # memory use in GB...I think
    memoryUse = memoryUse * 1000 # change to MB
    # 1000000000 # change to Bytes
    return memoryUse
    # print('memory use:', memoryUse)

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

            # print(get_memory_use())
            # mem_before = get_memory_use()
            # test_run(TEST_CODE)
            # mem_usage = memory_usage(test_run(TEST_CODE), interval=.05, timeout=(sec_time*1.2 + 1))
            # print("in")
            if func_name == "dp":
                mem_usage = memory_usage((dp, (str1[-1], str2[-1], get_cost)))
            else:
                mem_usage = memory_usage((hirschberg, (str1[-1], str2[-1], get_cost)))
            # print("out")
            net_mem_use = max(mem_usage) 
            # - mem_before
            # net_mem_use = get_memory_use() - mem_before
            data[os.path.basename(filename)] = {"runtime": sec_time, "mem_use": net_mem_use, "length": length_bp}
            # print(ans)
            # print("Memory Use: " + str(mem_used))

            # TODO: Alternative way to track memory use?
            # mem_usage = memory_usage(test_run(TEST_CODE), interval=.1, timeout=(sec_time*1.5))
            # print(mem_usage)
            # print(max(mem_usage))
    return data


# if __name__ == '__main__':
#     # test real data
#     test_func_data("./test_strings/real_comp", "dp")
#     test_func_data("./test_strings/real_comp", "hirschberg")

#     # test generated data

