# coding=utf-8
import random

from bpnn import *


def saveWeight(ni, wi, nh, wo, count):
    """
    权值矩阵
    """
    fo = open("./output/weight.txt", "a")
    fo.write('\n迭代百次:' + str(count))
    fo.write('\nInput weights:\n')
    for i in range(len(wi)):
        fo.write(str(wi[i]) + '\n')
    fo.write('\nOutput weights:\n')
    for j in range(len(wo)):
        fo.write(str(wo[j]) + '\n')

dim = 100
fo = open("./input/data_n.txt", "r")
all_the_text = fo.read()

arr = all_the_text.splitlines()
for i in range(dim):
    arr[i] = arr[i].split("\t")
arr = arr[:dim]
print "all data count:", len(arr)
arrT = zip(*arr)
print "data dim: ", len(arrT)

allSet = []
tag = 1
for j in range(len(arrT)):
    if (j != 0) and (j % 4 == 0):
        tag = tag + 1
    if j % 48 == 0:
        tag = 1
    allSet.append([arrT[j], [float(tag) / 13], [tag]])


myNN = NN(dim, 25, 1)
for l in range(0, 10):
    train = []
    test = []
    rand = random.randint(1, 4)
    for k in range(len(arrT)):
        if k % rand == 0:
            test.append(allSet[k])
        else:
            train.append(allSet[k])
    myNN.train(allSet)
    myNN.test(test)
    saveWeight(myNN.getNI(), myNN.getWI(), myNN.getNH(), myNN.getWO(), l + 1)
