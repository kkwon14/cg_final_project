# from timeit import Timer
# from septest import *
# from global_alignment_functions import *


# # def test():
# #     "Stupid test function"
# #     ('text.find(char)', setup='text = "sample string"; char = "g"')


# # def time_test():
# #     t = Timer("dp(x, y, s)", 'from global_alignment_functions import dp; x= "ABC"; y="ABC"; s = 1')
# #     print t.timeit()


# # if __name__ == '__main__':
# #     time_test()

# print(dp("ABC", "ABC", 1))

with open("global_alignment_functions.py") as fp:
    for i, line in enumerate(fp):
        if "\xe2" in line:
            print i, repr(line)