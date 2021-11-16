#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-16 11:03:34 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import chrome_bookmarks

bookmarkDict = {}
df = pd.DataFrame()
for url in chrome_bookmarks.urls:
    print(url.url, url.name)
    bookmarkDict.update({"title" : url.name})
    bookmarkDict.update({"url" : url.url})
    videoDict.update({"type" : "bookmark"})
    bookmarkDict = {k : bookmarkDict[k] for k in sorted(bookmarkDict.keys())}
    df = df.append(bookmarkDict,ignore_index=True)
print(df)
