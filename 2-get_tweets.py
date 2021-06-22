#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
get_tweets.py

Purpose:
    Download the tweets from US senators using tweepy

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
import tweepy
from readwrite_outline import *
# import pandas as pd
# import matplotlib.pyplot as plt

###########################################################
### jTweets= extract_tweets(handle)
def extract_tweets(handle, api):
    """
    Purpose:
        Extract tweets from a twitter handle

    Inputs:
        handle      string, name of the account
        api         tweepy api object

    Return value:
        jTweets     list of json, tweets
    """
    aTWit = tweepy.Cursor(api.user_timeline, id= handle, tweet_mode='extended').items(300)
    tweets = []
    try:
        for tw in aTWit:
            tweets.append(tw._json)
        savejson(tweets, os.getcwd()+"/Input/tweets_"+handle+".json")
    except tweepy.TweepError:
        print("Couldn't get the tweets of %s" % (handle))
    return tweets

###########################################################
### main
def main():
    # Magic numbers
    path = os.getcwd()
    handles = pd.read_pickle(path + '/Input/handles_df.pkl')
    consumer_token = "GJhkGXtHGnrgHVVyT5iksvYtP"
    consumer_secret = "9jmkYUKf4Kvtv7mMwT1D4SwvB36uJIeegOREaW51eb57RgcLdx"
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
        
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # Initialisation
    for i in range(len(handles)):
        handle = handles.iloc[i]['Twitter Handle']
        if len(handle)>0 and handle[0] == "@":
            aTW = extract_tweets(handle[1:], api)


    # Estimation
    

    # Output
    print ("The tweets have been downloaded.\n")

###########################################################
### start main
if __name__ == "__main__":
    main()
