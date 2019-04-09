#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:01:00 2019

@author: hsy
"""

import pandas as pd

df = pd.read_csv('./data/transactions2016_movies.csv')

N = len(df)

# load the matched pairs with book names, threshold = 85
pair_df = pd.read_csv('./data/summary_85_movies.csv')
df['grouped_name'] = df['prod_name']
for i, row in pair_df.iterrows():
    df.loc[row['index2'], 'grouped_name'] = df.loc[row['index1'], 'grouped_name']

#df = df.iloc[df.groupby('grouped_name')['grouped_name'].transform('size').mul(-1).argsort(kind='mergesort')]
df['count'] = df.groupby('grouped_name')['grouped_name'].transform('size')
df = df.sort_values(by=['count', 'grouped_name'], ascending=False)
df.to_csv('./data/transactions2016_moviess_sorted.csv',index=False)