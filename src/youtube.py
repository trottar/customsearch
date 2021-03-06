#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-01-05 13:14:45 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse
import urllib
from PyQt5.QtWidgets import QProgressBar,QApplication 
import json, os

import tools

pd.set_option('display.max_colwidth', None)

def import_playlist(playlist,pbar):

    videoDict = {}
    df = pd.DataFrame()
    for vid in playlist:

        print("Importing data for youtube playlist {}...".format(vid))
        
        if None != vid:
            #extract playlist id from url
            query = parse_qs(urlparse(vid).query, keep_blank_values=True)
            playlist_id = query["list"][0]
            developerKey = os.getenv("youtube_api")

            #print(f'get all playlist items links from {playlist_id}')
            youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = developerKey)

            request = youtube.playlistItems().list(
                part = "snippet",
                playlistId = playlist_id,
                maxResults = 50
            )
            try:
                response = request.execute()
            except googleapiclient.errors.HttpError:
                continue

            playlist_items = []
            while request is not None:
                response = request.execute()
                playlist_items += response["items"]
                request = youtube.playlistItems().list_next(request, response)

            #print(f"total: {len(playlist_items)}")

            pl_urls = [ 
                f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
                for t in playlist_items
            ]

            for i,v_url in enumerate(pl_urls):
                v_id=v_url.split('v=')[1].split('&list')[0]
                params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % v_id}
                v_url = "https://www.youtube.com/oembed"
                query_string = urllib.parse.urlencode(params)
                v_url = v_url + "?" + query_string
                try:
                    with urllib.request.urlopen(v_url) as response:
                        response_text = response.read()
                        data = json.loads(response_text.decode())
                except (urllib.error.HTTPError, urllib.error.URLError,ConnectionError) as e:
                    if e.code in (..., 403, ...):
                        continue
                title = data['title']
                #print("\t-> ",title)
                videoDict.update({"title" : title.lower()})
                videoDict.update({"url" : v_url})
                videoDict.update({"type" : "youtube"})
                with open('../database/log/database_titles.txt') as f:
                    if v_url in f.read():
                        continue
                pbar.setMaximum(len(pl_urls)-1)
                pbar.setValue(i)
                pbar.setFormat("Updating youtube data... {0:.0f}%".format((i/len(pl_urls))*100))
                QApplication.processEvents()
                if len(pl_urls) > 1:
                    tools.progressBar(i, len(pl_urls)-1)
                else:
                    tools.progressBar(i, len(pl_urls))
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(v_id)
                except:
                    continue
                text = ''
                for d in transcript:
                    text += d['text']
                #print(' '.join([line.strip().lower() for line in text.splitlines()]),"\n\n")
                videoDict.update({"transcript" : ' '.join([line.strip().lower() for line in text.splitlines()])})
                videoDict = {k : videoDict[k] for k in sorted(videoDict.keys())}
                df = df.append(videoDict,ignore_index=True)
        print("-"*70)
    return df
