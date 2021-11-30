#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-29 18:28:09 trottar"
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

def build_database(inp_db):

    db_path = '../database/'+inp_db
    
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    else:
        print("{} exists...".format(db_path))

def databaseDict(*args):

    databaseDict = {}
    databaseDict.update({'Must Read' : {'bookmarks' : ['Must Read'],'youtube' : [None],'database' : 'must_read/'}})

    for arg in args:
        for key,val in arg.items():
            #print(val['database'])
            build_database(val['database'])
        databaseDict.update(arg)

    return databaseDict


def create_database(pbar,layout,button,*args):
    '''
    database="" # database dir name
    #url = 'https://www.youtube.com/playlist?list=PLW5jnpyxgQHX7i63VJ1LJEgHFHcL3G_QC' # Physics
    url = 'https://www.youtube.com/playlist?list=PLW5jnpyxgQHWuCRcMlfb6LuvF_vfEgkKU' # Test
    bm_folder = 'Dogs'
    #bm_folder = 'Interesting Articles'
    '''
    
    layout.addRow(pbar)

    for arg in args:
        importDict = databaseDict(*args)
    
    for dir in importDict:
        #print("dir: ",dir)
        for key in importDict[dir]:
            #print("key: ",key)
            if key == 'bookmarks':
                #print("bookmarks: ", importDict[dir][key])
                bm_folder = importDict[dir][key]
                b_df = bookmarks.import_bookmarks(bm_folder,pbar,button)
            elif key == 'youtube':
                #print("youtube: ", importDict[dir][key])
                yt_folder = importDict[dir][key]
                button.setText("Updating youtube data...")
                y_df = youtube.import_playlist(yt_folder,pbar)
            elif key == 'database':
                #print("database: ", importDict[dir][key])
                database = importDict[dir][key]
            else:
                print('{} not found'.format(key))
                
        df = pd.concat([b_df,y_df], ignore_index=True)
        df  = df.reindex(sorted(df.columns),axis=1)

        try:
            with open('../database/log/database_titles.txt', 'a') as f:
                for text in df['url'].tolist():
                    f.write(text + '\n')

            print("There were {} entries added to the database".format(len(df['title'])))

            out_f = '../database/{}search_database'.format(database)
            for i,row in df.iterrows():
                dfRow = pd.DataFrame(row)
                dfRow = dfRow.T
                dfRow.to_csv("{0}_{1}.{2}".format(out_f,i,'csv'),index=False,header=True,mode='w')
        except:
            print('No new entries to add for {}...'.format(dir))
            
    '''
    button.setText("Updating bookmark data...")
    b_df = bookmarks.import_bookmarks(bm_folder,pbar)
    
    button.setText("Updating youtube data...")
    y_df = youtube.import_playlist(url,pbar)
    
    df = pd.concat([b_df,y_df], ignore_index=True)
    df  = df.reindex(sorted(df.columns),axis=1)

    out_f = '../database/search_database'

    for i,row in df.iterrows():
        dfRow = pd.DataFrame(row)
        dfRow = dfRow.T
        dfRow.to_csv("{0}_{1}.{2}".format(out_f,i,'csv'),index=False,header=True,mode='w')
    '''
