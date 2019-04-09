#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 22 20:59:59 2018

@author: Yucheng
"""

import scipy
import scipy.cluster.hierarchy as sch
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import string
import re
from collections import defaultdict
import json


## load the comScore data I get on Sep 18, 2018
df = pd.read_stata('/data/transactions2016_books_prod2.dta')
# There are 20978 books in the data

N = len(df)

# load the matched pairs with book names, threshold = 80
filename = '/data/match_80.txt'
data = pd.read_csv(filename,sep="\t", header=(0))
N_p = len(data)


# method 1: hierarchical clusterings 
#dis1 = np.mat(np.zeros((N,N)))
#for i in range(N_p):
#    dis1[data['index1'][i],data['index2'][i]] = data['similarity'][i]
#
#dis2 = 100 - dis1
#disMat = np.array(np.zeros((N*(N-1)/2)))
#k = 0
#for i in range(N):
#    for j in range(i+1,N):
#        disMat[k] = dis2[j,i]
#        k += 1
#
#Z = sch.linkage(disMat,method='single')

# method 2: simply see whether two elements can be "connected" - Union Find Problem

def indices_dict(lis):
    d = defaultdict(list)
    for i,(a,b) in enumerate(lis):
        d[a].append(i)
        d[b].append(i)
    return d

def disjoint_indices(lis):
    d = indices_dict(lis)
    sets = []
    while len(d):
        que = set(d.popitem()[1])
        ind = set()
        while len(que):
            ind |= que 
            que = set([y for i in que 
                         for x in lis[i] 
                         for y in d.pop(x, [])]) - ind
        sets += [ind]
    return sets

def disjoint_sets(lis):
    return [set([x for i in s for x in lis[i]]) for s in disjoint_indices(lis)]

#
list1 = []
for i in range(N_p):
    list1.append((data['index1'][i],data['index2'][i])) 


#lis = [(1,2),(2,3),(4,5),(6,7),(1,7)]
b = disjoint_sets(list1)    
N_s = len(b)

Size_s = np.array(np.zeros(N_s))
#with open('your_file.txt', 'w') as f:
#    for item in b:
#        f.write("%s\n" % item)

df['book_name'] = None

k = 1
for item in b:
    temp = list(item)
    Size_s[k-1] = len(temp)
    for index in temp:
        df['book_name'][index] = k
    k += 1
    print ("%s clusters done" %k)


#df.to_csv('book_name_cluster.txt', header=True, sep='\t', mode='w',index=0)

#
#n, bins, patches = plt.hist(Size_s)
#plt.show()


sort = sorted(Size_s, key=int, reverse=True)
sort_id = np.argsort(Size_s)
sort_id2 = sort_id[::-1]
#
#
with open('sort_size.txt', 'w') as f:
    for i in range(N_s):
        f.write("%s\t" % sort[i])
        temp = list(b[sort_id2[i]])
        f.write("%s\n" % df['prod_name'][temp[0]])

