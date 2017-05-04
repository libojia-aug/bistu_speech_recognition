#!/usr/bin/env python

from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

import numpy as np

import os

from pca import pca

expected_dim = 75
a = []
for j in range(1, 13):
    p = './input/newcut/' + str(j) + '/'
    o = '../oi/'
    t = []
    tt = []
    ttt = []
    for filename in os.listdir(p):
        if filename[0] == '.':
            continue
        (rate, sig) = wav.read(p + filename)
        mfcc_feat = mfcc(sig, samplerate=16000, numcep=1)

        
        tmp = []
        # for i in range(len(mfcc_feat)):
        for i in range(250):
            if(i < len(mfcc_feat)):
                tmp.append(mfcc_feat[i][0] * 500)
            else:
                tmp.append(0)
        t.append(','.join(str(v) for v in tmp))
    #     t.append(tmp)
    # lowDDataMat, reconMat = pca(np.matrix(t), expected_dim)
    # tt = lowDDataMat.tolist()
    # tmp = []
    # for k in range(len(tt)):
    #     print len(tt[k])
    #     print tt[k]
    #     ttt.append(','.join(str(v) for v in tt[k]))

        # print(len(tmp))
    fo = open(o + str(j) + '.txt', 'a')
    fo.write('\n'.join(str(v) for v in t))
    fo.close()

    # fo = open(o + filename[0:-4] + '.txt', 'a')
    # fo.write(','.join(str(v) for v in tmp))
    # fo.close()
    # fo.write('\n')

# d_mfcc_feat = delta(mfcc_feat, 2)
# fbank_feat = logfbank(sig,rate)
# print(mfcc_feat
