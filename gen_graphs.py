import benchmark
from pandas import DataFrame
import matplotlib.pyplot as plt

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

def gen_mem_graph(Data):
    df = DataFrame(Data, columns=["Memory Usage (MB)", "Length (bp)"])
    df.plot(x="Length (bp)", y="Memory Usage (MB)", kind='line')
    plt.show()

def gen_runtime_graph(Data):
    df = DataFrame(Data, columns=["Runtime (s)", "Length (bp)"])
    df.plot(x="Length (bp)", y="Runtime (s)", kind='line')
    plt.show()

if __name__ == '__main__':
    # test real data
    # print(benchmark.test_func_data("./test_strings/real_comp", "dp"))
    # benchmark.test_func_data("./test_strings/real_comp", "hirschberg")

    # test generated data
    dict_10p = benchmark.test_func_data("./test_strings/artificial_comp/10percent", "dp")
    pd_data = data_dict_to_pd_data(dict_10p)
    gen_mem_graph(pd_data)
    gen_runtime_graph(pd_data)


   
# Data = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
#         'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
#        }
  
# df = DataFrame(Data,columns=['Year','Unemployment_Rate'])
# df.plot(x ='Year', y='Unemployment_Rate', kind = 'line')
# plt.show()