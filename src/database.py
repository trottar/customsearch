#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-16 12:56:09 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd

import youtube
import bookmarks

url = 'https://www.youtube.com/playlist?list=PLW5jnpyxgQHX7i63VJ1LJEgHFHcL3G_QC'
bm_folder = 'Must Read'

b_df = bookmarks.import_bookmarks(bm_folder)
print(b_df.keys())
y_df = youtube.import_playlist(url)
print(y_df.keys())

df = pd.concat([b_df,y_df], axis=0)
df  = df.reindex(sorted(df.columns),axis=1)

print(df['type'])

out_f = '../database/search_database.csv'

df.to_csv(out_f,index=False,header=True,mode='a')
