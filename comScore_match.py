# -*- coding: utf-8 -*-
"""
Research assistant work for Prof. Arlene Wong by Yucheng Yang
Classification of comScore Product Names
Email to arlenewong@princeton.edu or yuchengy@princeton.edu
First version: 04/29/2018
This version: 05/02/2018
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import string
import re

def matchStr(prod_name):
    #regex = "\\s+([a-zA-Z]*\d+[a-zA-Z]+[10])\\s+"  # Regular expression
    regex = "[A-Z\d]{10}"  # Regular expression
    pattern = re.compile(regex)
    ASINs = re.findall(pattern, prod_name)
    for ASIN in ASINs:
        if re.findall(re.compile("[0-9]{2,}"),ASIN):
            return ASIN
    return ""

## load the comScore data
df = pd.read_stata('e7958f47552a1dfd.dta')
# There are 464340 items with 11 features

df_book = df[df['prod_category_id']==21]
# There are 24492 book items
"""
Unique purchase websites are: 
amazon.com                19392 (79.18%)
ebay.com                   1699 (6.94%)
barnesandnoble.com         1203 (4.92%)
christianbook.com           585 (2.39%)
walmart.com                 544 (2.22%)
abebooks.com                310
americangirl.com              5
ancestry.com                  1
bhphotovideo.com             35
costco.com                    7
dickssportinggoods.com       56
ecampus.com                  28
etsy.com                      6
frys.com                      1
gamestop.com                 48
groupon.com                   9
hsn.com                      29
kmart.com                    17
kohls.com                    33
lakeside.com                169
overstock.com                13
qvc.com                      41
rakuten.com                   1
sears.com                     5
staples.com                  12
target.com                   91
toysrus.com                  65
yahoo.net                    87
"""
df_book_amazon = df_book[df_book['domain_name']=='amazon.com']
# There are 19392 book items from Amazon

N = len(df_book_amazon['prod_name'])
df_book_amazon.index = range(N)
df_book_amazon['ASIN'] = None
df_book_amazon['processed_name'] = None

start = time.clock()

for i in range(N):
    book = df_book_amazon['prod_name'][i]
    ASIN = matchStr(book)
    if ASIN != "": # with ASIN
        df_book_amazon.loc[i,'ASIN'] = ASIN
        temp = book.split(ASIN)[0]# clean name endings after the ASIN
        temp = temp.replace('Amazon.com LLC','').replace('Amazon.com','')#remove Amazon.com and Amazon.com LLC
        df_book_amazon.loc[i,'processed_name'] = re.sub(r'[^\w\s]','',temp)#remove punctuations
    else: # without ASIN
        temp = book.replace('Amazon.com LLC','').replace('Amazon.com','')
        df_book_amazon.loc[i,'processed_name'] = re.sub(r'[^\w\s]', '', temp)

elapsed = (time.clock() - start)
print ("Time used to clean book names: %s" % elapsed)

# save as txt
df_book_amazon.to_csv('amazon_pro.txt', header=True, sep='\t', mode='a')








