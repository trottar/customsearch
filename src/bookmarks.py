#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-16 12:45:30 trottar"
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

def import_bookmarks(inp_folder):

    bookmarkDict = {}
    df = pd.DataFrame()
    for folder in chrome_bookmarks.folders:
        if inp_folder == folder.name:
            for url in folder.urls:
                bookmarkDict.update({"title" : url.name})
                bookmarkDict.update({"url" : url.url})
                bookmarkDict.update({"type" : "bookmark"})
                bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
                df = df.append(bookmarkDict,ignore_index=True)
    try:
        for url in df['url']:
            try:
                with urllib.request.urlopen(url) as response:
                    html = response.read()
            except:
                continue
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()
            bookmarkDict.update({"transcript" : text.strip("\n")})
            bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
            df = df.append(bookmarkDict,ignore_index=True)
    except:
        return df

    return df
