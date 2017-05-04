# coding=utf-8
# 反向传播神经网络
#
# Written in Python.  See http://www.python.org/
# Placed in the public domain.
# Neil Schemenauer <nas@arctrix.com>

import math
import random

random.seed(0)


def rand(a, b):
    """
    创建一个满足 a <= rand < b 的随机数
    :param a:
    :param b:
    :return:
    """
    return (b - a) * random.random() + a


def makeMatrix(I, J, fill=0.0):
    """
    创建一个矩阵（可以考虑用NumPy来加速）
    :param I: 行数
    :param J: 列数
    :param fill: 填充元素的值
    :return:
    """
    m = []
    for i in range(I):
        m.append([fill] * J)
    return m


def randomizeMatrix(matrix, a, b):
    """
    随机初始化矩阵
    :param matrix:
    :param a:
    :param b:
    """
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            matrix[i][j] = random.uniform(a, b)


def sigmoid(x):
    """
    sigmoid 函数，1/(1+e^-x)
    :param x:
    :return:
    """
    # print x;
    # try:
    if x < 0:
        return 1 - 1 / (1 + math.exp(x))
    else:
        return 1 / (1 + math.exp(-x))
    # ans = 1.0 / (1.0 + math.exp(-x))
    # except OverflowError:
    #     ans = float('inf')
    # return ans


def dsigmoid(y):
    """
    sigmoid 函数的导数
    :param y:
    :return:
    """
    return y * (1 - y)


class NN:

    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        """
        构造神经网络
        :param ni:输入单元数量
        :param nh:隐藏单元数量
        :param no:输出单元数量
        """
        self.ni = ni + 1  # +1 是为了偏置节点
        self.nh = nh
        self.no = no

        # 激活值（输出值）
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no

        foIW = open("./input/inputWeight.txt", "r")
        foOW = open("./input/outputWeight.txt", "r")

        IW = foIW.readlines()
        OW = foOW.readlines()
        self.wi = []
        self.wo = []
        if len(IW) == self.ni and len(OW) == self.nh:
            for x in range(len(IW)):
                tl = []
                t = IW[x].split(', ')
                for y in range(len(t)):
                    tl.append(float(t[y]))
                self.wi.append(tl)
            for x in range(len(OW)):
                tl = []
                t = []
                t.append(OW[x])
                for y in range(len(t)):
                    tl.append(float(t[y]))
                self.wo.append(tl)
        else:
            # 权重矩阵
            self.wi = makeMatrix(self.ni, self.nh)  # 输入层到隐藏层
            self.wo = makeMatrix(self.nh, self.no)  # 隐藏层到输出层
            # 将权重矩阵随机化
            randomizeMatrix(self.wi, -0.2, 0.2)
            randomizeMatrix(self.wo, -2.0, 2.0)
        # 权重矩阵的上次梯度
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)



    def runNN(self, inputs):
        """
        前向传播进行分类
        :param inputs:输入
        :return:类别
        """
        if len(inputs) != self.ni - 1:
            print 'incorrect number of inputs'

        for i in range(self.ni - 1):
            self.ai[i] = float(inputs[i])

        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum += (self.ai[i] * self.wi[i][j])
            self.ah[j] = sigmoid(sum)

        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum += (self.ah[j] * self.wo[j][k])
            self.ao[k] = sigmoid(sum)

        return self.ao

    def backPropagate(self, targets, N, M):
        """
        后向传播算法
        :param targets: 实例的类别
        :param N: 本次学习率
        :param M: 上次学习率
        :return: 最终的误差平方和的一半
        """
        # http://www.youtube.com/watch?v=aVId8KMsdUU&feature=BFa&list=LLldMCkmXl4j9_v0HeKdNcRA

        # 计算输出层 deltas
        # dE/dw[j][k] = (t[k] - ao[k]) * s'( SUM( w[j][k]*ah[j] ) ) * ah[j]
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k] - self.ao[k]
            output_deltas[k] = error * dsigmoid(self.ao[k])

        # 更新输出层权值
        for j in range(self.nh):
            for k in range(self.no):
                # output_deltas[k] * self.ah[j] 才是 dError/dweight[j][k]
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] += N * change + M * self.co[j][k]
                self.co[j][k] = change

        # 计算隐藏层 deltas
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error += output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = error * dsigmoid(self.ah[j])

        # 更新输入层权值
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                # print 'activation',self.ai[i],'synapse',i,j,'change',change
                self.wi[i][j] += N * change + M * self.ci[i][j]
                self.ci[i][j] = change

        # 计算误差平方和
        # 1/2 是为了好看，**2 是平方
        error = 0.0
        for k in range(len(targets)):
            error = 0.5 * (targets[k] - self.ao[k]) ** 2
        return error

    def weights(self):
        """
        打印权值矩阵
        """
        print 'Input weights:'
        for i in range(self.ni):
            print self.wi[i]
        print
        print 'Output weights:'
        for j in range(self.nh):
            print self.wo[j]
        print ''

    def getWI(self):
        return self.wi

    def getWO(self):
        return self.wo

    def getNI(self):
        return self.ni

    def getNH(self):
        return self.nh

    def test(self, patterns):
        """
        测试
        :param patterns:测试数据
        """
        tfc = 0
        for p in patterns:
            inputs = p[0]
            # print 'Inputs:', p[0], '-->', self.runNN(inputs), '\tTarget',
            # p[1]
            ao = self.runNN(inputs)
            t = p[1]
            # if abs(ao[0] - t[0]) < (1.0 / 26):
            if ao.index(max(ao)) == t.index(1):
                tf = 1
            else:
                tf = 0
            tfc += tf
            # print ao, '\tTarget', p[1], '\ttf', tf
        print 'acc', float(tfc) / len(patterns)

    def train(self, patterns, max_iterations=1000, N=0.05, M=0.01):
        """
        训练
        :param patterns:训练集
        :param max_iterations:最大迭代次数
        :param N:本次学习率
        :param M:上次学习率
        """
        for i in range(max_iterations):
            # print i
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                # print inputs
                self.runNN(inputs)
                error = self.backPropagate(targets, N, M)
            # if i % 10 == 0:
            # if err or < 0.001:
                # break
            print 'i:', i, 'Combined error:', error
            if i % 10 == 0:
                self.test(patterns)
        # self.test(patterns)


def main():
    # pat = [
    #     [[0, 0, 0], [0, 0]],
    #     [[0, 0, 1], [0, 1]],
    #     [[0, 1, 0], [0, 1]],
    #     [[0, 1, 1], [1, 0]],
    #     [[1, 0, 0], [0, 1]],
    #     [[1, 0, 1], [1, 0]],
    #     [[1, 1, 0], [1, 0]],
    #     [[1, 1, 1], [1, 1]]
    # ]
    pat = [
        # [[100, 100, 100], [0, 0]],
        [[2.1, 2.1, 21], [0, 1]],
        [[2.1, 21, 2.1], [0, 1]],
        [[2.1, 21, 21], [1, 0]],
        [[2, 2.1, 2.1], [0, 1]],
        [[21, 2.1, 21], [1, 0]],
        [[21, 21, 2.1], [1, 0]],
        [[21, 21, 21], [1, 1]]
    ]
    myNN = NN(3, 6, 2)
    myNN.train(pat)


if __name__ == "__main__":
    main()
