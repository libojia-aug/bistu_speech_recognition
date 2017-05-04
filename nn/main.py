# coding=utf-8
import random
import os

from bpnn import *


def saveWeight(ni, wi, nh, wo, count):
    """
    权值矩阵
    """
    fo = open("./output/weight.txt", "a")
    fo.write('\n迭代千次:' + str(count))
    fo.write('\nInput weights:\n')
    for i in range(len(wi)):
        fo.write(str(wi[i]) + '\n')
    fo.write('\nOutput weights:\n')
    for j in range(len(wo)):
        fo.write(str(wo[j]) + '\n')

dim = 12
p = '../oi/na0t500d12/'
allSet = []
for filename in os.listdir(p):
    if filename[0] == '.':
            continue
    fo = open(p+filename, "r")
    all_the_text = fo.read()
    arr = all_the_text.splitlines()
    lin = []
    zer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    zer[int(filename[0:-4])-1] = 1 
    for i in range(len(arr)):
        t = arr[i].split(',')
        lin.append(t)
        lin.append(zer)
        # print i
        allSet.append(lin)
        lin = []
# print allSet

myNN = NN(dim, 25, 12)
for l in range(0, 1000):
    train = []
    test = []
    rand = random.randint(1, 4)
    for k in range(len(allSet)):
        if k % rand == 0:
            test.append(allSet[k])
        else:
            train.append(allSet[k])
    myNN.train(allSet)
    myNN.test(test)
    saveWeight(myNN.getNI(), myNN.getWI(), myNN.getNH(), myNN.getWO(), l + 1)
