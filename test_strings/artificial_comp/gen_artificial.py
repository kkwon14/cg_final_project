import random
import os.path

'''
Function to generate a random string of ATGC n bytes long
'''
def gen_random_string(n):
    bases = ["A", "T", "G", "C"]
    string = ""
    for i in range(n):
        string = string + bases[random.randint(0, 3)]
    return string

'''
Have an n percent chance of having a random mutation ()...Returns mutated string
    pct = [0, 100]
'''
def create_entropy(string, pct):
    modify_indices = []
    bases = ["A", "T", "G", "C"]
    for i in range(len(string)):
        if pct >= random.randint(0, 100):
            modify_indices.append(i)
    
    for i in (modify_indices):
        rand = random.randint(0, 2)
        if rand == 0:
            # insertion
            string = string[:i] + bases[random.randint(0, 3)] + string[i:]
            # if cursor == len(string) -1:
            #     modify_indices = modify_indices[:cursor].append(map(lambda x: x+1, modify_indices[cursor + 1:])) 
        elif rand == 1:
            # deletion
            string = string[:i] + string[i + 1:]
            # if cursor == len(string) - 1:
            #     modify_indices = modify_indices[:cursor].append(map(lambda x: x-1, modify_indices[cursor + 1:])) 
        else:
            # replacement
            string = string[:i] + bases[random.randint(0, 3)] + string[i+1:]
    
    return string

def run_test(generated_lengths, pct, filename):
    s1 = ""
    s1_mut = ""
    for value in generated_lengths:
        s1 = gen_random_string(value)
        # print(s1)
        # print(create_entropy(s1, pct))
        s1_mut = create_entropy(s1, pct)

        final_filename = os.path.join("./", filename, filename + "_" + str(value) + "long.txt")
        # '.\' + filename + '\' + filename + "_" + str(value) + "long.txt"
        if not os.path.exists(os.path.dirname(final_filename)):
            os.makedirs(os.path.dirname(final_filename))
        with open(final_filename, "w") as f:
            f.write(s1 + "\n" + s1_mut)


if __name__ == '__main__':
    generated_lengths = [50, 500, 1000, 2500, 5000, 10000]

    # 5% mutated
    run_test(generated_lengths, 10, "10percent")
    # 50% mutation
    run_test(generated_lengths, 50, "50percent")
    # 90% mutation
    run_test(generated_lengths, 90, "90percent")