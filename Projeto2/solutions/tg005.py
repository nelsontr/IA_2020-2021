# -*- coding: utf-8 -*-
"""
Grupo tg005
Student id #93695
Student id #93743
"""

import numpy as np
import random


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
             
            sub_arvore = dtl(np.array(new_sub_D), np.array(new_sub_Y), new_Atributos, D, Y, noise)
            new_tree.append(sub_arvore)
        
        if len(str(new_tree)) < len(str(tree)):
            return new_tree
    
    return tree


def dtl(D, Y, atributos, D_pai, Y_pai, noise=False):
    #1
    if not len(Y):
        if np.count_nonzero(Y_pai == 1) > np.count_nonzero(Y_pai == 0):
            return 1
        elif np.count_nonzero(Y_pai == 1) < np.count_nonzero(Y_pai == 0):
            return 0
        else:
            return random.randint(0,1)
    
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
            return random.randint(0,1)
    
    #4
    features = D.transpose()
    D_list = D.tolist()
    for i in range(len(Y)):
        D_list[i].append(Y[i])
    
    
    best_atribute = max([i for i in range(len(features))], key = lambda a: findMaxGain(a, D_list, noise))
    gain = findMaxGain(best_atribute, D_list, noise)
    if gain < 0.05 and noise:
        return 1 if ones > zeros else 0 

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
        #if len(tree)>2:
        #    if tree[1] == tree[2]:
        #        tree = tree[1]
    
    return tree


def createdecisiontree(D,Y, noise = False):
    atributos = []
    for i in range(len(D[0])):
        atributos.append(i)
    
    decisionTree = dtl(D, Y, atributos, D, Y, noise)
    #print(decisionTree)
    tree = pruning_tree(decisionTree, D, Y, atributos, noise)
    return tree
