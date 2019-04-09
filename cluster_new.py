#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:01:00 2019

@author: hsy
"""

import pandas as pd

## load the comScore data I get on Sep 18, 2018
df = pd.read_stata('./data/transactions2016_books_prod2.dta')
# There are 20978 books in the data

N = len(df)

# load the matched pairs with book names, threshold = 80
pair_df = pd.read_csv('./data/summary_80.csv')
df['grouped_name'] = df['prod_name']
for i, row in pair_df.iterrows():
    df.loc[row['index2'], 'grouped_name'] = df.loc[row['index1'], 'grouped_name']

df = df.iloc[df.groupby('grouped_name')['grouped_name'].transform('size').mul(-1).argsort(kind='mergesort')]
df.to_csv('./data/transactions2016_books_sorted.csv',index=False)