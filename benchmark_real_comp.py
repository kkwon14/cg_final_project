import pathlib
import csv

from benchmark import test_func_data

#TODO add four russians
global_alignment_funcs = ['dp', 'hirschberg']

base_path = pathlib.Path(__file__).parent
real_comp_dir = (base_path / 'test_strings' / 'real_comp').resolve()

csv_filename = (base_path / 'real_comp_benchmark_data' / 'real_comp_benchmarks.csv').resolve()

def run_benchmarks():
    with open(csv_filename, 'w+', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['Main Seq', 'Comparison Seq', 'Sim/Dif',
                         'Main Seq Length', 'Alignment Type', 'Runtime (s)', 'Memory (MB)'])
        for directory in real_comp_dir.iterdir():
            # iterate through directories in real_comp_dir
            length, main_sec = str(directory.stem).split(maxsplit=1)
            for func in global_alignment_funcs:
                alignment_type = func
                result = test_func_data(directory, func)
                for filename, results in result.items():
                    # remove file extension
                    filename = filename.rsplit('.', 1)[0]
                    # left is if sim or diff, right is seq name
                    sim_dif, comp_seq = filename.split(maxsplit=1)
                    runtime = results['runtime']
                    mem = results['mem_use']
                    writer.writerow([main_sec, comp_seq, sim_dif, length, alignment_type, runtime, mem])            

if __name__ == '__main__':
    run_benchmarks()
