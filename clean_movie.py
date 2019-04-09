# -*- coding: utf-8 -*-
"""
Research assistant work for Prof. Arlene Wong by Yucheng Yang
Classification of comScore Product Names
Email to arlenewong@princeton.edu or yuchengy@princeton.edu
First version: 04/29/2018
This version: 05/02/2018
"""

import pandas as pd
import time
import re

def clean_punc(string):
    return re.sub(r'[^\w\s]','',string)

def del_last_word(string):
    return string.rsplit(' ', 1)[0]

#clean walmart, delete seller's name(separeted by 2 spaces), ASIN, 'AMAZON.COM'
def clean_amazon(prod_name):
   prod_name = prod_name.rsplit('  ', 1)[0]
   regex = r'(?:B\d{2}[\dA-Z]{7})|(?:\d{9}(?:X|\d))'
   pattern = re.compile(regex)
   ASINs = re.findall(pattern, prod_name)
   if ASINs:
       print(ASINs[0])
       temp = prod_name.split(ASINs[0])[0]# clean name endings after the ASIN
   else:
       temp = prod_name
   return temp.replace('AMAZON.COM LLC','').replace('AMAZON.COM','')#remove Amazon.com and Amazon.com LLC



## load the comScore data
df = pd.read_stata('data/e7958f47552a1dfd.dta')

df_movie = df[df['prod_category_id']==23]

"""
Unique purchase websites are: 
amazon.com            5844
ebay.com              3108 (keep 624)
barnesandnoble.com     468
christianbook.com      296
walmart.com            281
yahoo.net              187
bestbuy.com            175
gamestop.com           128
target.com             109
samsclub.com            52 (keep 0)
toysrus.com             48
overstock.com           10
kohls.com                7
frys.com                 5
costco.com               5
kmart.com                2
jet.com                  1
"""

#uppercase, remove punctuations
df_movie['prod_name'] = df_movie['prod_name'].str.upper().apply(clean_punc)

#clean amazon
df_movie_amazon = df_movie[df_movie['domain_name']=='amazon.com']

start = time.clock()
df_movie_amazon['prod_name'] = df_movie_amazon['prod_name'].apply(clean_amazon)
elapsed = (time.clock() - start)
print ("Time used to clean amazon movie names: %s" % elapsed)

#clean ebay, keep only the prod_names that contain 'DVD|DISC|SEASON', delete the last word
df_movie_ebay = df_movie[df_movie['domain_name']=='ebay.com']
df_movie_ebay = df_movie_ebay[df_movie_ebay['prod_name'].str.contains('DVD|DISC|SEASON')]
#624/3108 remained
df_movie_ebay['prod_name'] = df_movie_ebay['prod_name'].apply(del_last_word)

#clean walmart, delete the last word
df_movie_walmart = df_movie[df_movie['domain_name']=='walmart.com']
df_movie_walmart['prod_name'] = df_movie_walmart['prod_name'].apply(del_last_word)

#puttng together
df_movie = df_movie[(df_movie['domain_name']!='amazon.com') & (df_movie['domain_name']!='ebay.com') & (df_movie['domain_name']!='walmart.com') & (df_movie['domain_name']!='samsclub.com')]
df_movie = pd.concat([df_movie, df_movie_amazon, df_movie_ebay, df_movie_walmart])
df_movie.to_csv('data/transactions2016_movies.csv')