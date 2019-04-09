# comscore

### 3/30/2019 (3h)

-  fuzzy_book.py
  - added multiprocessing
  - changed output
  - **using similarity threshold 80: many pairs are not the same books, prod_name still noisy**
- cluster_new.py
  - used a new clustering method: add a column containing the clustered name of the product, initialized as the original product names; since the pairs are all in ascending order, we can loop all the pairs and for each pair, the clustered name of the second book is changed to the clustered name of the first book.
  - sort the dataframe by the count of the clustered names

### 4/9/2019 (4h)

- clean_movie.py
  - ebay transactions are kept if prod_name contains 'DVD|DISC|SEASON'
  - new function to clean amazon prod_name: seller's names are at the tail of prod_name, following either 2 spaces or ASIN
- fuzzy_book.py
  - threshold set to 85