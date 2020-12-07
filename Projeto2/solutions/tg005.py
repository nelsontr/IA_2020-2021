# -*- coding: utf-8 -*-
"""
Grupo tg005
Student id #93695
Student id #93743
"""

import numpy as np

def calc_entropy(x):
    return -1 * (x*np.log2(x) + (1-x)*np.log2(1-x)) if x not in (0,1) else 0

def findMaxGain(a, D, Y):
    posTrue, posFalse, negTrue, negFalse = 0, 0, 0, 0
    #print("D",D)
    #print("F",Y)
    "Y[a] não existe para a=2 ->16"
    for ex in D:
        if ex[a]==1:
            if Y[a]==1:
                posTrue += 1
            else:
                posFalse += 1
        else:
            if Y[a]==1:
                negTrue += 1
            else:
                negFalse += 1

    positives = posTrue + posFalse
    negatives = negTrue + negFalse
    
    if not positives:
        posDivision = 0
    else:
        posDivision = posTrue/(positives)
    
    if not negatives:
        negDivision = 0
    else:
        negDivision = negTrue/(negatives)

    total = positives + negatives

    return calc_entropy(positives/total) - ((negatives/total)*calc_entropy(negDivision + (positives/total)*calc_entropy(posDivision)))
    

def dtl(D, Y, atributos, D_pai, Y_pai, noise):
    #1
    if not len(Y):
        ones = np.count_nonzero(Y_pai == 1)
        zeros = np.count_nonzero(Y_pai == 0)
        return 1 if ones > zeros else 0
    
    #2
    ones = np.count_nonzero(Y == 1)
    zeros = np.count_nonzero(Y == 0)
    if ones == len(Y) or zeros == len(Y):
        if len(atributos) != len(D[0]):
            return 1 if ones > zeros else 0
        else:
            return [0,1,1] if ones > zeros else [0,0,0]
            
    #3
    if not atributos:
        return 1 if ones > zeros else 0 
    
    #4
    features = list(map(list, zip(*D)))

    best_gain = max([i for i in range(len(features))], key = lambda a: findMaxGain(a, D, Y))
    tree = [best_gain,]
    
    for i in (0,1):
        new_Atributos = []
        for j in range(len(atributos)):
            if j != best_gain:
                new_Atributos.append(j)

        new_sub_D, new_sub_Y = [], []
        for j in range(len(Y)):
            if D[j][best_gain] == i:
                new_sub_D.append(D[j]) 
                new_sub_Y.append(Y[j])
                
        sub_arvore = dtl(np.array(new_sub_D), np.array(new_sub_Y), new_Atributos, D, Y, noise)
        tree.append(sub_arvore)
    
    return tree


def createdecisiontree(D,Y, noise = False):
    atributos = []
    for i in range(len(D[0])):
        atributos.append(i)
    
    decisionTree = dtl(D, Y, atributos, D, Y, noise)
    #print(decisionTree)
    return decisionTree

def classify(T,data):
    
    data = np.array(data)
    out = []
    for el in data:
        #print("el",el,"out",out,"\nT",T)
        wT = T
        for ii in range(len(el)):
            #print(T[0],el[T[0]],T)
            if el[wT[0]]==0:
                if not isinstance(wT[1], list):
                    out += [wT[1]]
                    break
                else:
                    wT = wT[1]
            else:
                if not isinstance(wT[2], list):
                    out += [wT[2]]
                    break
                else:
                    wT = wT[2]
    return np.array(out)

"""
D3 = np.array([
              [0,0,0],
              [0,0,1],
              [0,1,0],
              [0,1,1],
              [1,0,0],
              [1,0,1],
              [1,1,0],
              [1,1,1]])

Y = np.array([0,1,0,1,1,1,1,1])
T = createdecisiontree(D3,Y)
Yp = classify(T,D3)
err = np.mean(np.abs(Yp-Y))
print("tree > ", T, "\nprediction >", Yp,"\n correct >",Y,"\n errors >", err)

print(T)"""