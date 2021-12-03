#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-12-03 14:51:35 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import chrome_bookmarks
from urllib.parse import parse_qs, urlparse
import urllib
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QProgressBar,QApplication 

import tools

pd.set_option('display.max_colwidth', None)

        
def import_bookmarks(inp_folder,pbar,button):
    
    bookmarkDict = {}
    df = pd.DataFrame()
    for val in inp_folder:
        button.setText("Updating {} bookmark data...".format(val))
        print("Importing data for bookmarks from {}...".format(val))
        for folder in chrome_bookmarks.folders:
            if val == folder.name:
                for i,url in enumerate(folder.urls):
                    bookmarkDict.update({"title" : url.name.lower()})
                    bookmarkDict.update({"url" : url.url})
                    bookmarkDict.update({"type" : "bookmark"})
                    with open('../database/log/database_titles.txt') as f:
                        if url.url in f.read():
                            continue
                    #print("\t-> ",url.name.lower())
                    pbar.setMaximum(len(folder.urls)-1)
                    pbar.setValue(i)
                    QApplication.processEvents()
                    if len(folder.urls) > 1:
                        tools.progressBar(i, len(folder.urls)-1)
                    else:
                        tools.progressBar(i, len(folder.urls))
                    #print(url, "\n\n","-"*70)
                    url = url.url
                    try:
                        with urllib.request.urlopen(url) as response:
                            html = response.read()
                    except (urllib.error.HTTPError, urllib.error.URLError) as e:
                        continue
                    soup = BeautifulSoup(html, "html.parser")
                    if val == 'Must Read':
                        text = 'MR: '
                    else:
                        text = ''
                    for para in soup.find_all("p"):
                        text += para.get_text()
                    #print(' '.join([line.strip().lower() for line in text.splitlines()]),"\n\n")
                    bookmarkDict.update({"transcript" : ' '.join([line.strip().lower() for line in text.splitlines()])})
                    bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
                    df = df.append(bookmarkDict,ignore_index=True)
    print("-"*70)
    return df
