#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLP.py

Purpose:
    Get the LDA topics for the tweets

Version:
    1       First start

Date:
    2021/06/07

Author:
    Diego Dabed
"""
###########################################################
### Imports
import os
import pandas as pd
import pickle
from tweet_preprocessor import tokenize_tweets
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

# import matplotlib.pyplot as plt
##########################################################
def remove_amp(tweet):
    """Takes a string and removes 'amp ' """
    tweet = tweet.replace('amp ', '')
    return tweet

###########################################################
### main
def main():
    # Magic numbers
    path = os.getcwd()
    df = pd.read_pickle(path + "/Output/clean_data.pkl")
    
    # More cleaning (remove links, stopwords, etc..)
    df = tokenize_tweets(df)
    df.reset_index(inplace=True)
    # Remove word "amp"
    df.tokens = df.tokens.apply(remove_amp)
    
    # Create dictionary
    dictionary = corpora.Dictionary()
    
    # Create BoW
    BoW_corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in df["tokens"].str.split()]
    pickle.dump(BoW_corpus, open(path+'/Output/gensim_corpus_corpus.pkl', 'wb'))
    dictionary.save(path+'/Output/gensim_dictionary.gensim')
    
    # Estimate model
    k = 40
    lda = LdaModel(BoW_corpus, id2word=dictionary,  alpha = "auto", 
                   num_topics = k, decay = 0.8, iterations = 100,
                   random_state = 420, minimum_probability=0.0)
    
    # Print topics
    for topic_id in range(lda.num_topics):
        topk = lda.show_topic(topic_id, 10)
        topk_words = [ w for w, _ in topk ]
        print('{}: {}'.format(topic_id, ' '.join(topk_words)))
    
    # Extract topics
    topic_matrix = []
    for i in range(len(df)):
        topic_matrix.append(lda.get_document_topics(dictionary.doc2bow(df.tokens[i].split())))
    
    # Transpose matrix
    topics = [[p[l][1] for p in topic_matrix] for l in range(k)]
    
    # Attach to dataframe
    for i in range(k):
        df["topic_"+str(i)] = topics[i]
        
    # Store results
    df.to_pickle(path + "/Output/data_w_topics.pkl")
    lda.save(path+'/Output/gensim_model.gensim')
    
    print("NLP topic classification is done.")
    
###########################################################
### start main
if __name__ == "__main__":
    main()
