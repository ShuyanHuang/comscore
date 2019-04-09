#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Research assistant work for Prof. Arlene Wong by Yucheng Yang
Modified by Shuyan Huang
Classification of comScore books' product names
Email to arlenewong@princeton.edu or yuchengy@princeton.edu
First version: 09/19/2018
This version: 03/28/2019 (added multiprocessing, modified output)
"""

import pandas as pd
import numpy as np
import time
import multiprocessing

from scipy.spatial.distance import squareform
from fuzzywuzzy import fuzz


## load the comScore data I get on Sep 18, 2018
df = pd.read_csv('./data/transactions2016_movies.csv')
# There are 20978 books in the data

N = len(df)

test = df['prod_name'].values

# compute the similarity of all the book name pairs
start = time.clock()

I = np.mat(np.zeros((N,N)))
#for i in range(N):
#	for j in range(i+1, N):
#		I[i,j] = fuzz.ratio(test[i], test[j])
#	print ("%s books done" %i)

def similarity(pair):
    return fuzz.ratio(test[pair[0]], test[pair[1]])

#i = range(N)
#j = range(N)
#paramlist = list(itertools.product(i, j))
pairlist = []
for i in range(N):
    for j in range(i+1, N):
        pairlist.append([i, j])
pool = multiprocessing.Pool()
I_lst = pool.map(similarity,pairlist)
I = squareform(I_lst)
for i in range(N):
    for j in range(i):
        I[i, j] = 0
elapsed = (time.clock() - start)
print ("Time used to compute similarity: %s" % elapsed)

thres = 85
indices = np.where(I >= thres)
out_df = pd.DataFrame({'index1':indices[0], 'index2':indices[1], 'similarity':I[indices], 'name1':test[indices[0]], 'name2':test[indices[1]]})
out_df.to_csv('./data/summary_85_movies.csv', index=False) 
    


#with open("Output80_v2.txt", "w") as text_file:
#    for i in range(N):
#        text_file.write("Book 1: {}\n".format(df['prod_name_original'][indices[0][i]]))
#        text_file.write("Book 2: {}\n".format(df['prod_name_original'][indices[1][i]]))
##        text_file.write("Compustat purged: {}\n".format(df['prod_name'][indices[0][i]]))
##        text_file.write("Nielsen purged: {}\n".format(df['prod_name'][indices[1][i]]))
#        text_file.write("Distance Score: {}\n".format(I[indices[0][i],indices[1][i]]))
#        text_file.write("\n")


















