#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-22 01:03:27 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import os

import youtube
import bookmarks

pd.set_option('display.max_colwidth', None)

'''
!!!!!!!!!!!!!!
Need to improve these three scripts (database, youtube, bookmarks) so that they
check if a bookmark/video already exists plus add in some progress bars. Also
need tp add a list input for running many bookmarks/playlists

'''

def create_database(pbar,layout,button):

    #url = 'https://www.youtube.com/playlist?list=PLW5jnpyxgQHX7i63VJ1LJEgHFHcL3G_QC' # Physics
    url = 'https://www.youtube.com/playlist?list=PLW5jnpyxgQHWuCRcMlfb6LuvF_vfEgkKU' # Test
    #bm_folder = 'Must Read'
    bm_folder = 'Dogs'
    #bm_folder = 'Interesting Articles'

    layout.addRow(pbar)

    button.setText("Updating bookmark data...")
    b_df = bookmarks.import_bookmarks(bm_folder,pbar)
    
    button.setText("Updating youtube data...")
    y_df = youtube.import_playlist(url,pbar)
    
    df = pd.concat([b_df,y_df], ignore_index=True)
    df  = df.reindex(sorted(df.columns),axis=1)

    print("There were {} entries added to the database".format(len(df['title'])))

    out_f = '../database/search_database'

    for i,row in df.iterrows():
        dfRow = pd.DataFrame(row)
        dfRow = dfRow.T
        dfRow.to_csv("{0}_{1}.{2}".format(out_f,i,'csv'),index=False,header=True,mode='w')
