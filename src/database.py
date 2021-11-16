#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-16 10:38:44 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import youtube

url = 'https://www.youtube.com/playlist?list=PLW5jnpyxgQHX7i63VJ1LJEgHFHcL3G_QC'

y_df = youtube.import_playlist(url)
print(y_df.keys())
