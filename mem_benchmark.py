from memory_profiler import memory_usage
from global_alignment_functions import *

import argparse

def dummy_function():
    pass

def benchmark(a, b, alignment):
    if alignment == 'dp':
        func = dp
    elif alignment == 'hirschberg':
        func = hirschberg
    else:
        raise ValueError('Invalid alignment {alignment}\n')

    init_mem = memory_usage(dummy_function, max_usage=True)
    total_mem = memory_usage((func, (a, b, get_cost)), max_usage=True)
    net_mem = total_mem - init_mem
    print(net_mem)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('string_a', help='one of the strings to align')
    parser.add_argument('string_b', help='the other string to align')
    parser.add_argument('alignment', help='the type of alignment {dp, hirschberg, motr}')
    args = parser.parse_args()
    benchmark(args.string_a, args.string_b, args.alignment)
