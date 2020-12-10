# Group 42 EN.601.447 Computational Genomics: Sequences Final Project

### Navigating the Code
  Implementation for Naive DP, Hirschberg's Algorithm, Four Russians can be found in global_alignment_functions.py.  
  Code for timing and measuring memory usage is found in benchmark.py and mem_benchmark.py (mem_benchmark.py is isolated in order to accurately get memory usage of the Python program without interference from other parts of the code, the rest is in benchmark.py)  
  Generating graphs for artificially generated strings is found in gen_graphs.py. The generated graphs are found in bench_graphs/ and the input strings are in test_strings/artificial_comp/  
  Generating the csv for real genomes is found in benchmark_real_comp.py. The generated CSV is in real_comp_benchmark_data/ and the input strings are in test_strings/real_comp/

### Running the Code
  Implemented in Python 3.8  
  Required packages found in requirements.txt  
  Note: There's a section of code that uses subprocess. This requires that the command used to run a Python program is python3. If this is not the command for your computer (like if it's just python), change "python3" in line 11 of benchmark.py to that command.  
  
  Install requirements
  ```
  pip install -r requirements.txt
  ```
  
  To independently run each algorithm:
  ```
  from global_alignment_functions.py import *
  # to run naive DP
  dp('<input string 1>', '<input string 2>', get_cost)
  # to run Hirschberg
  hirschberg('<input string 1>', '<input string 2>', get_cost)
  # to do preprocessing for Four Russians
  create_preprocess_file(<int for t>)
  # to run Four Russians (needs preprocessed file - takes ton of memory to generate)
  four_russians('<input string 1>', '<input string 2>')
  ```
  To run benchmarks,
  ```
  # Generate graphs for artificially generated strings
  python3 gen_graphs.py
  # Generate CSV for actual strings
  python3 benchmark_real_comp.py
  ```
