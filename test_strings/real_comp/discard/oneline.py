s = ""

with open("./filetooneline.txt") as f:
    lines = f.readlines()
    for line in lines:
        line.replace('\n', "")
        s = s + line
    

with open("./nospace.txt", "w") as f:
    f.write(s.replace('\n', ''))