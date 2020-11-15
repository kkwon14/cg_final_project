import timeit  # from https://pypi.org/project/memory-profiler/
from memory_profiler import memory_usage
from global_alignment_functions import *
import os
import glob

# import os
# import psutil

# process = psutil.Process(os.getpid())

# process.get_ext_memory_info().peak_wset

'''
Test a function based on real data comparisons in "./test_strings/real_comp".
    Data in text files is formatted "string1 \n string2"
    @func_name = string name of Global Alignment function to test
    Output is "filename: runtime (secs)"
'''
def test_func_real_data(func_name):
    SETUP_CODE = '''
from global_alignment_functions import FUNCTION_TEST, get_cost
  '''
    SETUP_CODE = SETUP_CODE.replace("FUNCTION_TEST", func_name)
    TEST_TEMPLATE = 'FUNCTION_TEST("s1","s2", get_cost)'
    TEST_TEMPLATE = TEST_TEMPLATE.replace("FUNCTION_TEST", func_name)
    for filename in glob.glob(os.path.join("./test_strings/real_comp", '*.txt')):
        with open(filename, 'r') as f:
            TEST_CODE = TEST_TEMPLATE
            str1 = f.readline()
            str2 = f.readline()
            TEST_CODE = TEST_CODE.replace("s1", str1[:-1])
            TEST_CODE = TEST_CODE.replace("s2", str2[:-1])

            '''
            Use replaced TEST_CODE in order to get time data with timeit package
            '''
            t = timeit.Timer(setup=SETUP_CODE, stmt=TEST_CODE)

            # TODO: UNCOMMENT FOR MORE ACCURATE DATA
            # sec_time = t.timeit(100000)/100000  # Average time over 100,000 runs
            sec_time = t.timeit(1) # to test benchmarking is working 

            print(str(filename) + ": " + str(sec_time))



    # mem_usage = memory_usage(dp("s1", "s2", get_cost))
    # print(max(mem_usage))

if __name__ == '__main__':
    test_func_real_data("dp")
    test_func_real_data("hirschberg")
