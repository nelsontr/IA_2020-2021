# -*- coding: utf-8 -*-
"""
Grupo tg005
Student id #93695
Student id #93743
"""

import numpy as np


def calc_entropy(x):
    return -1 * (x*np.log2(x) + (1-x)*np.log2(1-x)) if x not in (0,1) else 0

def findMaxGain(a, D, noise):
    
    posTrue, posFalse, negTrue, negFalse, posDivision, negDivision = 0, 0, 0, 0, 0, 0
    for ex in D:
        if ex[a] and ex[-1]:
            posTrue += 1
        elif ex[a] and not ex[-1]:
            posFalse += 1
        elif not ex[a] and ex[-1]:
            negTrue += 1
        elif not ex[a] and not ex[-1]:
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
    
    return calc_entropy(positives/total) - ((negatives/total)*calc_entropy(negDivision)\
         + (positives/total)*calc_entropy(posDivision))
    

def dtl(D, Y, atributos, D_pai, Y_pai, noise=False, short = 0):
    #1
    if not len(Y):
        if np.count_nonzero(Y_pai == 1) > np.count_nonzero(Y_pai == 0):
            return 1
        else:
            return 0
    
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
    features = D.transpose()
    D_list = D.tolist()
    for i in range(len(Y)):
        D_list[i].append(Y[i])
    
    
    
    if(noise>0):
        one = np.count_nonzero(features == 1)
        zero = np.count_nonzero(features == 0)
        best_atribute = 1 if one>zero else 0
    else:
        best_atribute = max([i for i in range(len(features))], key = lambda a: findMaxGain(a, D_list, noise))
        gain = findMaxGain(best_atribute, D_list, noise)
        

    tree = [best_atribute,]
    
    for i in (0,1):
        new_Atributos = []
        for j in range(len(atributos)):
            if j != best_atribute:
                new_Atributos.append(j)

        new_sub_D, new_sub_Y = [], []
        for j in range(len(Y)):
            if D[j][best_atribute] == i:
                new_sub_D.append(D[j]) 
                new_sub_Y.append(Y[j])
                
        sub_arvore = dtl(np.array(new_sub_D), np.array(new_sub_Y), new_Atributos, D, Y, noise)
        tree.append(sub_arvore)

        #Reducing the tree
        if len(tree)>2:
            if tree[1] == tree[2]:
                tree = tree[1]

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

np.random.seed(13102020)
D = np.random.rand(5000,12)>0.5
Y = ((D[:,1] == 0) & (D[:,6] == 0)) | ((D[:,3] == 1) & (D[:,4] == 1) | ((D[:,11] == 1) & (D[:,6] == 1)))

T = createdecisiontree(D,Y)
Yp = classify(T,D)
err = np.mean(np.abs(Yp-Y))
print("tree > ", T, "\nprediction >", Yp,"\n correct >",Y,"\n errors >", err)

print(T)