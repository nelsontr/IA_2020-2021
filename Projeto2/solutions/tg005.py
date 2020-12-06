# -*- coding: utf-8 -*-
"""
Grupo tg005
Student id #93695
Student id #93743
"""

import numpy as np

def calc_entropy(x,y):
    return -1 * (x*np.log2(x) + y*np.log2(y)) if x != 0 and y != 0 else 0

def findMaxGain(D, Y, atributos):
    gain = 0
    maxGain = 0
    bestColumn = []
    positives = [0,0] #positives on Y==0, Y==1
    negatives = [0,0] #negatives on Y==0, Y==1
    for i in range(len(D[0])):
        column = D[:,i]
        for j in range(len(column)):
            classification = Y[j]

            if column[j]:
                positives[classification]+=1
            else: 
                negatives[classification]+=1
        
        if positives[0] and positives[1]:
            p = positives[0] + positives[1]
            gain += (p/len(Y))*calc_entropy(positives[0]/p, positives[1]/p)
        if negatives[0] and negatives[1]:
            n = negatives[0] + negatives[1]
            gain += (n/len(Y))*calc_entropy(negatives[0]/n, negatives[1]/n)
        
        if gain > maxGain:
            maxGain = gain
            bestColumn = column 

    return bestColumn

def dtl(D, Y, atributos, D_pai, Y_pai, noise):
    #1
    if not Y:
        ones = np.count_nonzero(Y_pai == 1)
        zeros = np.count_nonzero(Y_pai == 0)
        return ones if ones > zeros else zeros
    
    #2
    ones = np.count_nonzero(Y == 1)
    zeros = np.count_nonzero(Y == 0)
    if ones == len(Y) or zeros == len(Y):
        if len(atributos) != len(D[0].size):
            return 1 if ones > zeros else 0
        else:
            return [0,1,1] if ones > zeros else [0,0,0]
    #3
    if not atributos:
        return ones if ones > zeros else zeros
    
    #4
    chosenColumn = findMaxGain(D, Y, atributos)
    #chosenColumn = idx[0]

    tree = [chosenColumn, -1,-1]
    new_sub_D, new_sub_Y = [], []
        
    for i in "01":
        new_Atributos = []
        for j in atributos:
            if j != chosenColumn:
                new_Atributos.append(j)

        for j in range(len(Y)):
            new_sub_D = new_sub_D.append(D[j]) if D[i][chosenColumn]==i else new_sub_D
            new_sub_Y = new_sub_Y.append(Y[j]) if D[i][chosenColumn]==i else new_sub_Y

        sub_arvore = dtl(new_sub_D, new_sub_Y, new_Atributos, D, Y, noise)
        tree[i+1] = sub_arvore
    
    return tree



def createdecisiontree(D,Y, noise = False):
    atributos = []
    for i in range(len(D[0])):
        atributos.append(i)
    
    decisionTree = dtl(D, Y, atributos, D, Y, noise)
    return decisionTree


D2 = np.array([[0,0],
               [0,1],
               [1,0],
               [1,1]])

Y = (np.array([0,0,0,1]))
createdecisiontree(D2,Y, noise = False)

