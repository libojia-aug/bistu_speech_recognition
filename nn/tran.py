import os

p = '../oi/na0/'
al = []
for filename in os.listdir(p):
    if filename[0] == '.':
        continue
    fo = open(p + filename, "r")
    all_the_text = fo.read()
    arr = all_the_text.splitlines()
    a = []
    for j in range(500):
        tmp = arr[j].split('\t')
        print len(tmp)
        a.append([float(k) for k in tmp])
    arrT = zip(*a)

    fo = open('../oi/na0t500/' + filename, "w")
    for i in range(len(arrT)):
        fo.write(str(arrT[i]) + '\n')
