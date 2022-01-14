#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-01-12 04:39:23 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import feedparser
from pylatexenc.latex2text import LatexNodes2Text

import tools

pd.set_option('display.max_colwidth', None)

def import_rss():

    rssDict = {}
    df = pd.DataFrame()

    #print('arXiv Nuclear Experiment')
    #print('='*70)
    nucl_ex = feedparser.parse("http://export.arxiv.org/rss/nucl-ex")
    #print('Number of RSS posts :', len(nucl_ex.entries))

    for post in nucl_ex.entries:
        ex_entry = post
        #print(ex_entry.keys())
        #print('Post Title :',ex_entry.title)
        #print("******************")
        #print(ex_entry.summary)
        #print("------Link--------")
        #print(ex_entry.link)
        #print('-'*70)
        latex = r"{}".format(ex_entry.title.lower())
        rssDict.update({"title" : LatexNodes2Text().latex_to_text(latex)})
        rssDict.update({"url" : ex_entry.link})
        rssDict.update({"type" : "nucl-ex"})
        rssDict.update({"transcript" : ' '.join([line.strip().lower() for line in ex_entry.summary.splitlines()])})
        rssDict = {k : rssDict[k] for k in sorted(rssDict.keys())}
        df = df.append(rssDict,ignore_index=True)

    #print('\n\narXiv Nuclear Theory')
    #print('='*70)
    nucl_th = feedparser.parse("http://export.arxiv.org/rss/nucl-th")
    #print('Number of RSS posts :', len(nucl_ex.entries))

    for post in nucl_th.entries:
        th_entry = post
        #print(th_entry.keys())
        #print('Post Title :',th_entry.title)
        #print("******************")
        #print(th_entry.summary)
        #print("------Link--------")
        #print(th_entry.link)
        #print('-'*70)
        latex = r"{}".format(th_entry.title.lower())
        rssDict.update({"title" : LatexNodes2Text().latex_to_text(latex)})
        rssDict.update({"url" : th_entry.link})
        rssDict.update({"type" : "nucl-th"})
        rssDict.update({"transcript" : ' '.join([line.strip().lower() for line in th_entry.summary.splitlines()])})
        rssDict = {k : rssDict[k] for k in sorted(rssDict.keys())}
        df = df.append(rssDict,ignore_index=True)

    # Removes duplicate entries
    df.drop_duplicates(subset=['url'], inplace=True)
    df = df.reset_index(drop=True)
        
    #print("-"*70)
    #print(df)
    return df    
