#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-19 15:01:05 trottar"
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
import json
import os

pd.set_option('display.max_colwidth', None)

def import_playlist(url):

    #extract playlist id from url
    query = parse_qs(urlparse(url).query, keep_blank_values=True)
    playlist_id = query["list"][0]
    developerKey = os.getenv("youtube_api")
    
    print(f'get all playlist items links from {playlist_id}')
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = developerKey)

    request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlist_id,
        maxResults = 50
    )
    response = request.execute()

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    print(f"total: {len(playlist_items)}")

    pl_urls = [ 
        f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
        for t in playlist_items
    ]

    videoDict = {}
    df = pd.DataFrame()
    for v_url in pl_urls:
        v_id=v_url.split('v=')[1].split('&list')[0]
        params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % v_id}
        v_url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        v_url = v_url + "?" + query_string
        try:
            with urllib.request.urlopen(v_url) as response:
                response_text = response.read()
                data = json.loads(response_text.decode())
        except urllib.error.HTTPError as e:
            if e.code in (..., 403, ...):
                continue
        title = data['title']
        videoDict.update({"title" : title.lower()})
        videoDict.update({"url" : v_url})
        videoDict.update({"url_id" : v_id})
        videoDict = {k : videoDict[k] for k in sorted(videoDict.keys())}
        df = df.append(videoDict,ignore_index=True)

    # Get list of transcript lines
    for v_id in df['url_id']:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(v_id)
        except:
            continue
        text = ''
        for d in transcript:
            text += d['text']
        print(' '.join([line.strip().lower() for line in text.splitlines()]),"\n\n")
        videoDict.update({"transcript" : ' '.join([line.strip().lower() for line in text.splitlines()])})
        videoDict.update({"type" : "youtube"})
        videoDict = {k : videoDict[k] for k in sorted(videoDict.keys())}
        df = df.append(videoDict,ignore_index=True)
        
    df.drop("url_id",axis=1,inplace=True)
    
    return df
