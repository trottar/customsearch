#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-16 11:51:31 trottar"
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
import requests
from bs4 import BeautifulSoup

bookmarkDict = {}
df = pd.DataFrame()
for url in chrome_bookmarks.urls:
    bookmarkDict.update({"title" : url.name})
    bookmarkDict.update({"url" : url.url})
    bookmarkDict.update({"type" : "bookmark"})
    bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
    df = df.append(bookmarkDict,ignore_index=True)
for url in df['url']:
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
        #data = requests.get(url).text
    except:
        continue
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    bookmarkDict.update({"transcript" : text.strip("\n")})
    bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
    df = df.append(bookmarkDict,ignore_index=True)
print(df)
