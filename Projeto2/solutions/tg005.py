# -*- coding: utf-8 -*-
"""
Grupo tg005
Student id #93695
Student id #93743
"""

import numpy as np

def entropy(x, y):
    return (-(x) * np.log2(x) - y*np.log2(y))

def findMaxGain(columns, lines, D, Y):
    maxGain = 0
    entropy = entropy(D, lines)
    if not entropy:
        return maxGain
    
    for i in range(columns):
        zeros, uns, falses0, trues0, trues1, falses1 = 0
        gain = 0
        trues = 0
        falses = 0
        for j in range(lines):
            if D[i][j]:
                trues += 1
            else:
                falses += 1
        
        total = trues + falses

        if not(x) and not(y):
            gain += Y[0]/lines


def createdecisiontree(D,Y, noise = False):
    zeros, uns, falses0, trues0 = []
    maior = -1
    total = len(D)


    for i in range(total):
        zeros, uns = 0,0
        falses0, trues0, falses1, trues1 = 0,0,0,0
        if not(D[i][0]):
            zeros += 1
            if not(Y[i]):
                falses0 += 1
            else:
                trues0 +=1
        else:
            uns += 1
            if not(Y[i]):
                falses1 +=1            
            else:
                trues1 +=1
        zeros[i].append(zeros)
        uns[i].append(uns)
        falses0[i].append(falses0)
        trues0[i].append(trues0)

        GI


    GI(F0) = 1 - ((2/4) * I((2/2), (0/2)) + (2/4) * I(1/2, 1/2))
    GI(F0) = 1 - ((zeros/total) * entropy(falses com 0/zeros, true com 0 / zeros) + (uns/total) * entropy(falses com 1/uns, true com 1/uns))
    
    return [0,0,1]




def classify(T,data):
