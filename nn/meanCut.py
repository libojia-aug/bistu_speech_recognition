# coding=utf-8
import os
import numpy as np

p = '../oi/na0t500/'
al = []
exdi = 6
for filename in os.listdir(p):
    if filename[0] == '.':
        continue
    fo = open(p + filename, "r")
    all_the_text = fo.read()
    arr = all_the_text.splitlines()
    a = []
    for j in range(len(arr)):
        tmp = map(float, arr[j].split(', '))
        # print tmp
        v = tmp.index(0.0)
        w = v / exdi
        d = v % exdi

        # print w
        # print d

        lenIdx = []

        for q in range(exdi):
            if d > 0:
                lenIdx.append(w + 1)
                d = d - 1
            else:
                lenIdx.append(w)

        # print lenIdx
        al = []
        for k in range(len(lenIdx)):
            al.append(float(np.mean(tmp[0:lenIdx[k]])))
            tmp = tmp[lenIdx[k]:]

        a.append(','.join(str(v) for v in al))
    fo = open('../oi/na0t500d' + str(exdi) + '/' + filename, "w")

    # print a
    for i in range(len(a)):

        fo.write(a[i] + '\n')
