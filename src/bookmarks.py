#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-19 14:19:51 trottar"
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

pd.set_option('display.max_colwidth', None)

def import_bookmarks(inp_folder):

    bookmarkDict = {}
    df = pd.DataFrame()
    for folder in chrome_bookmarks.folders:
        if inp_folder == folder.name:
            for url in folder.urls:
                print(url.name.lower(),"\n\n")
                bookmarkDict.update({"title" : url.name.lower()})
                bookmarkDict.update({"url" : url.url})
                bookmarkDict.update({"type" : "bookmark"})
                bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
                df = df.append(bookmarkDict,ignore_index=True)
    print(df['url'])
    try:
        for url in df['url']:
            print(url, "\n\n","-"*70)
            try:
                with urllib.request.urlopen(url) as response:
                    html = response.read()
            except urllib.error.HTTPError as e:
                if e.code in (..., 403, ...):
                    continue
            soup = BeautifulSoup(html, "html.parser")
            # Gets all text
            #text = soup.get_text() 
            # Get all paragraphs
            #print(url, "\n\n","-"*70, soup, "\n\n")
            text = ''
            for para in soup.find_all("p"):
                text += para.get_text()
            print(' '.join([line.strip().lower() for line in text.splitlines()]),"\n\n")
            bookmarkDict.update({"transcript" : ' '.join([line.strip().lower() for line in text.splitlines()])})
            bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
            df = df.append(bookmarkDict,ignore_index=True)
    except:
        return df

    return df
