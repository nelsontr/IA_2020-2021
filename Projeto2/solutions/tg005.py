# -*- coding: utf-8 -*-
"""
Grupo tg005
Student id #93695
Student id #93743
"""

import numpy as np

def calc_entropy(x):
    return -1 * (x*np.log2(x) + (1-x)*np.log2(1-x)) if x not in (0,1) else 0

def findMaxGain(a, D):
    posTrue, posFalse, negTrue, negFalse = 0, 0, 0, 0
    
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

    posDivision = 0 if not positives else posTrue/(positives)
    negDivision = 0 if not negatives else negTrue/(negatives)

    total = positives + negatives
    
    return calc_entropy(positives/total) - ((negatives/total)*calc_entropy(negDivision) \
        + (positives/total)*calc_entropy(posDivision))
    

def pruning_tree(tree, D, Y, atributos, noise):
    for x in atributos:
        new_tree = [x,]
        for i in (0,1):
            new_Atributos = []
            for j in range(len(atributos)):
                if j != x:
                    new_Atributos.append(j)

            new_sub_D, new_sub_Y = [], []
            for j in range(len(Y)):
                if D[j][x] == i:
                    new_sub_D.append(D[j]) 
                    new_sub_Y.append(Y[j])
             
            sub_arvore = dtl(np.array(new_sub_D), np.array(new_sub_Y), new_Atributos, Y, noise)
            new_tree.append(sub_arvore)
        
        if len(str(new_tree)) < len(str(tree)):
            return new_tree

    return tree


def dtl(D, Y, atributos, Y_pai, noise=False):
    #1
    if not len(Y):
        one_pai = np.count_nonzero(Y_pai == 1)
        zero_pai = np.count_nonzero(Y_pai == 0)
        if one_pai > zero_pai:
            return 1
        elif zero_pai > one_pai:
            return 0
        else:
            return np.random.randint(0,2) #low inclusive, high exclusive
    
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
        if ones > zeros:
            return 1
        elif zeros > ones:
            return 0 
        else:
            return np.random.randint(0,2)
    
    #4
    features = D.transpose()
    D_list = D.tolist()
    for i in range(len(Y)):
        D_list[i].append(Y[i])
    
    
    best_atribute = max([i for i in range(len(features))], key = lambda a: findMaxGain(a, D_list))
    gain = findMaxGain(best_atribute, D_list)
    
    #Noise
    if gain < 0.05 and noise:
        return 1 if ones > zeros else 0 

    tree = [best_atribute,]
    
    for i in (0,1):
        new_Atributos = []
        new_sub_D, new_sub_Y = [], []

        #New_Atributes
        for j in range(len(atributos)):
            if j != best_atribute:
                new_Atributos.append(j)
        #New_D and #New_Y
        for j in range(len(Y)):
            if D[j][best_atribute] == i:
                new_sub_D.append(D[j]) 
                new_sub_Y.append(Y[j])
        #Recursive
        sub_arvore = dtl(np.array(new_sub_D), np.array(new_sub_Y), new_Atributos, Y, noise)
        tree.append(sub_arvore)
        
    return tree


def createdecisiontree(D,Y, noise = False):
    atributos = []
    for i in range(len(D[0])):
        atributos.append(i)
    
    decisionTree = dtl(D, Y, atributos, Y, noise)
    return pruning_tree(decisionTree, D, Y, atributos, noise)

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

D2 = np.array([
                  [0,0],
                  [0,1],
                  [1,0],
                  [1,1]])
Y = (np.array([2%16,2%8,2%4,2%2])>0).astype('int32')

T = createdecisiontree(D2,Y)
Yp = classify(T,D2)
err = np.mean(np.abs(Yp-Y))
print("tree > ", T, "\nprediction >", Yp,"\n correct >",Y,"\n errors >", err)

print(T)