#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-12-21 03:09:28 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import sys
import subprocess

pd.set_option('display.max_colwidth', None)

def searchfiles(keyword,database=''):

    cmd = ['./LucenePlusPlus/src/searchDB.sh','{}'.format(keyword),'../../../database/{}'.format(database)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
    #print(result)
    if keyword == '':
        df = pd.DataFrame()
    else:
        try:
            goodDocs = result.split('Enter query: Searching for: {}'.format(keyword))[1]
            #print(goodDocs,"\n\n")
            passCheck = goodDocs.split('total matching documents')[0]
            if int(passCheck) == 0:
                print('\n\nNo matching entries not found!\n\n')
                df = pd.DataFrame()
            else:
                if 'Press (n)ext page,' in goodDocs:
                    goodFiles = goodDocs.split('total matching documents')[1].replace('Press (n)ext page, (q)uit or enter number to jump to a page: Enter query:','')
                else:
                    goodFiles = goodDocs.split('total matching documents')[1].replace('Press (q)uit or enter number to jump to a page: Enter query:','')
                goodFiles  = goodFiles.strip().split('\n')
                #print(goodFiles, "\n\n")
                df = pd.DataFrame()
                print("{} matches have been found".format(passCheck))
                print("-"*70)
                print("rank",'\t',"score",'\t\t',"file name")
                for i,goodFile in enumerate(goodFiles):
                    rank = goodFile.split('. ../../')[0].strip()
                    score = goodFile.split('. ../../')[1].split('score=')[1].strip()
                    f_name = goodFile.split('. ../../')[1].split('score=')[0].strip()
                    print(rank,'\t',score,'\t',f_name)
                    try:
                        inp_f = pd.read_csv(f_name)
                    except:
                        print("{} not found".format(f_name))
                        continue
                    inp_f = dict(inp_f)
                    df = df.append(inp_f,ignore_index=True)
                print("-"*70)
                print(df['title'])            
        except:
            print('\n\nERROR: Check searchfiles in Lucene++...\n\n')
            sys.exit(0)
    return df

def allfiles(keyword,database=''):

    cmd = ['find','../database/{}'.format(database)]
    ls = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    result = subprocess.Popen(["grep", "-v", "/$"],stdin=ls.stdout,stdout=subprocess.PIPE)
    goodFiles  = result.stdout
    #print(goodFiles, "\n\n")
    df = pd.DataFrame()
    for goodFile in goodFiles:
        if 'csv' in str(goodFile):
            f_name = str(goodFile).strip("'").strip('\\n').strip("b'")
            #print(f_name)
            try:
                inp_f = pd.read_csv(f_name)
            except:
                print("{} not found".format(f_name))
                continue
            inp_f = dict(inp_f)
            df = df.append(inp_f,ignore_index=True)
    print("-"*70)           
    return df
