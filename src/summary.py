#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-12-21 06:53:49 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

import pandas as pd
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import networkx as nx

nltk.download('punkt')
nltk.download('stopwords')


transcript = "Maria Sharapova has basically no friends as tennis players on the WTA Tour. The Russian player has no problems in openly speaking about it and in a recent interview she said: 'I don't really hide any feelings too much. I think everyone knows this is my job here. When I'm on the courts or when I'm on the court playing, I'm a competitor and I want to beat every single person whether they're in the locker room or across the net.So I'm not the one to strike up a conversation about the weather and know that in the next few minutes I have to go and try to win a tennis match. I'm a pretty competitive girl. I say my hellos, but I'm not sending any players flowers as well. Uhm, I'm not really friendly or close to many players. I have not a lot of friends away from the courts.' When she said she is not really close to a lot of players, is that something strategic that she is doing? Is it different on the men's tour than the women's tour? 'No, not at all. I think just because you're in the same sport doesn't mean that you have to be friends with everyone just because you're categorized, you're a tennis player, so you're going to get along with tennis players. I think every person has different interests. I have friends that have completely different jobs and interests, and I've met them in very different parts of my life. I think everyone just thinks because we're tennis players we should be the greatest of friends. But ultimately tennis is just a very small part of what we do. There are so many other things that we're interested in, that we do.'"

def summarize_text(transcript):

    '''
    I will split the sequences into the data by tokenizing them using a list
    '''
    sentences = []
    for s in transcript:
        sentences.append(sent_tokenize(s))

    sentences = [y for x in sentences for y in x]

    '''
    I am going to use the Glove method for word representation, it is an unsupervised 
    learning algorithm developed by Stanford University to generate word integrations 
    by aggregating the global word-to-word co-occurrence matrix from a corpus. To 
    implement this method you have to download a file from here and store it into the 
    same directory where your python file is:
    '''
    word_embeddings = {}
    f = open('models/glove.6B.100d.txt', encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()

    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    clean_sentences = [s.lower() for s in clean_sentences]
    stop_words = stopwords.words('english')
    def remove_stopwords(sen):
        sen_new = " ".join([i for i in sen if i not in stop_words])
        return sen_new
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]    

    '''
    I will create vectors for the sentences
    '''
    sentence_vectors = []
    for i in clean_sentences:
      if len(i) != 0:
        v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
      else:
        v = np.zeros((100,))
      sentence_vectors.append(v)

    '''
    Find similarities between the sentences, and I will use the cosine similarity approach 
    for this task. Let’s create an empty similarity matrix for this task and fill it with 
    cosine similarities of sentences
    '''      
    sim_mat = np.zeros([len(sentences), len(sentences)])
    from sklearn.metrics.pairwise import cosine_similarity
    for i in range(len(sentences)):
      for j in range(len(sentences)):
        if i != j:
          sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]

    '''
    I am going to convert the sim_mat similarity matrix into the graph, the nodes in this graph 
    will represent the sentences and the edges will represent the similarity scores between the 
    sentences
    '''
    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    '''
    Summarize text
    '''    
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
    for i in range(0,len(sentences)):
      print("ARTICLE:")
      print(transcript[i])
      print('\n')
      print("SUMMARY:")
      print(ranked_sentences[i][1])
      print('\n')

summarize_text(transcript)      
