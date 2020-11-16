import benchmark
from pandas import DataFrame
import matplotlib.pyplot as plt
import os.path

'''
Turn a dictionary of data in formation {filename:{mem_use, runtime, length}} in to
{mem_use:[], runtime:[], length:[]}
'''
def data_dict_to_pd_data(data_dict):
    mem_use = []
    runtime = []
    length = []
    for _, value in data_dict.iteritems():
        mem_use.append(value["mem_use"])
        runtime.append(value["runtime"])
        length.append(value["length"])
    return {"Memory Usage (MB)": mem_use, "Runtime (s)": runtime, "Length (bp)": length}

if __name__ == '__main__':
    # test real data
    # print(benchmark.test_func_data("./test_strings/real_comp", "dp"))
    # benchmark.test_func_data("./test_strings/real_comp", "hirschberg")

    # test generated data dp
    filenames = ["./test_strings/artificial_comp/10percent","./test_strings/artificial_comp/50percent","./test_strings/artificial_comp/90percent"]
    
    for f_name in filenames:
        # GATHERING DATA
        dict_p = benchmark.test_func_data(f_name, "dp")
        dict_h = benchmark.test_func_data(f_name, "hirschberg")

        dp_data = data_dict_to_pd_data(dict_p)
        hirsch_data = data_dict_to_pd_data(dict_h)

        # RUNTIME GRAPHING
        df = DataFrame(dp_data, columns=["Length (bp)"])
        df["Naive DP"] = dp_data["Runtime (s)"]
        df["Hirschberg"] = hirsch_data["Runtime (s)"]
        df = df.sort_values(by = ["Length (bp)"])

        f_name = os.path.basename(f_name)
        fig = df.plot(x="Length (bp)", y=["Naive DP", "Hirschberg"], title=f_name + " Runtime Comparisons")
        fig.set_ylabel("Runtime (s)")
        fig = fig.get_figure()

        final_filename = os.path.join("./bench_graphs", f_name + "runtime.png")
        if not os.path.exists(os.path.dirname(final_filename)):
            os.makedirs(os.path.dirname(final_filename))
        fig.savefig(final_filename)
        plt.close()

        # MEMORY GRAPHING TODO: CLEAN UP CODE
        df = DataFrame(dp_data, columns=["Length (bp)"])
        df["Naive DP"] = dp_data["Memory Usage (MB)"]
        df["Hirschberg"] = hirsch_data["Memory Usage (MB)"]
        df = df.sort_values(by = ["Length (bp)"])

        f_name = os.path.basename(f_name)
        fig = df.plot(x="Length (bp)", y=["Naive DP", "Hirschberg"], title=f_name + " Memory Comparisons")
        fig.set_ylabel("Memory Usage (MB)")
        fig = fig.get_figure()

        final_filename = os.path.join("./bench_graphs", f_name + "memory.png")
        if not os.path.exists(os.path.dirname(final_filename)):
            os.makedirs(os.path.dirname(final_filename))
        fig.savefig(final_filename)
        plt.close()