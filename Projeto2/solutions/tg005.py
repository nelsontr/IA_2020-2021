# -*- coding: utf-8 -*-
"""
Grupo tg005
Student id #93695
Student id #93743
"""
import numpy as np


def bigger(ones, zeros):
    if ones > zeros:
        return 1
    elif zeros > ones:
        return 0
    else:
        return np.random.randint(0,2) #low inclusive, high exclusive


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

    if not positives:
        posDivision = 0 
    else:
        posDivision = posTrue/(positives)
    
    if not negatives:
        negDivision = 0
    else:
        negDivision = negTrue/(negatives)

    total = positives + negatives
    
    return calc_entropy(positives/total) - ((negatives/total)*calc_entropy(negDivision) \
        + (positives/total)*calc_entropy(posDivision))
    

def pruning_tree(tree, D, Y, atributos, noise):
    for x in atributos:
        initial_tree = [x,]

        reduced_tree = get_sub_tree(initial_tree, D, Y, atributos, x, noise)
        
        if len(str(reduced_tree)) < len(str(tree)):
            return reduced_tree

    return tree


def get_sub_tree(tree, D, Y, atributos, atribute, noise):
    for i in range(2):
        new_Atributos = []
        new_sub_D, new_sub_Y = [], []

        #New_Atributes
        for j in range(len(atributos)):
            if j != atribute:
                new_Atributos.append(j)
        #New_D and #New_Y
        for j in range(len(Y)):
            if D[j][atribute] == i:
                new_sub_D.append(D[j]) 
                new_sub_Y.append(Y[j])
        #Recursive
        sub_arvore = dtl(np.array(new_sub_D), np.array(new_sub_Y), Y, new_Atributos, noise)
        tree.append(sub_arvore)
    return tree


def dtl(D, Y,  Y_pai, atributos, noise=False):
    #1
    if not len(Y):
        one_pai = np.count_nonzero(Y_pai == 1)
        zero_pai = np.count_nonzero(Y_pai == 0)
        return bigger(one_pai, zero_pai)
    
    #2
    ones = np.count_nonzero(Y == 1)
    zeros = np.count_nonzero(Y == 0)
    if ones == len(Y) or zeros == len(Y):
        if len(atributos) != len(D[0]):
            return bigger(ones, zeros)
    
    #3
    if not atributos:   #atributos is a list, Y is a np.array
        return bigger(ones, zeros)
    
    #4
    features = D.transpose()
    D_list = D.tolist()
    for i in range(len(Y)):
        D_list[i].append(Y[i])

    features_list = []
    for i in range(len(features)):
        features_list.append(i)

    best_atribute = max(features_list, key = lambda a: findMaxGain(a, D_list))
    
    #Noise
    if noise:
        gain = findMaxGain(best_atribute, D_list)
        if gain < 0.05: #If GI is lower than 5% = BAD GI
            return bigger(ones, zeros)
    
    initial_tree = [best_atribute,]
    tree = get_sub_tree(initial_tree, D, Y, atributos, best_atribute, noise)
    return tree


def createdecisiontree(D,Y, noise = False):
    atributos = []
    for i in range(len(D[0])):
        atributos.append(i)
    
    decisionTree = dtl(D, Y, Y, atributos, noise)
    return pruning_tree(decisionTree, D, Y, atributos, noise)
