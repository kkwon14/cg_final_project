import os
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f == "replace_x.py":
        continue
    s = ""
    with open(f) as fi:
        lines = fi.readlines()
        for line in lines:
            for i in range(len(line)):
                if line[i] != 'A' and line[i] != 'T' and line[i] != 'G' and line[i] != 'C' and line[i] != '\n':
                    s = s + 'X'
                else:
                    s = s + line[i]
    print(s)
    with open(f, "w") as fi:
        fi.write(s)
