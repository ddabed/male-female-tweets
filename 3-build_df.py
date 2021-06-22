#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_df.py

Purpose:
    Build the dataframe with all the necessary information

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
from readwrite_outline import readjson
# import pandas as pd
# import matplotlib.pyplot as plt

###########################################################
### main
def main():
    # Magic numbers
    path = os.getcwd()
    handles = pd.read_pickle(path + '/Input/handles_df.pkl')
    demographics = pd.read_csv(path + "/Input/legislators-current.csv")
    demographics_hist = pd.read_csv(path + "/Input/legislators-historical.csv")
    
    col_names = ["Name", "Twitter Handle", "Tweet", "Female", "govtrack_id"]
    df = pd.DataFrame(columns=col_names)
    
    for index, senator in handles.iterrows():
        name = senator["Name"]
        handle = senator["Twitter Handle"][1:]
        not_found = True
        # Find gender and id of senator
        for index1, historical in demographics.iterrows():
            if historical["last_name"] in name and historical["first_name"] in name:
                govtrack = historical["govtrack_id"]
                if historical["gender"]== "F":
                    female = 1
                else:
                    female = 0
                not_found = False
        # If not actual senator search in the historical data
        if not_found:
            for index1, historical in demographics_hist.iterrows():
                if historical["last_name"] in name and historical["first_name"] in name:
                    govtrack = historical["govtrack_id"]
                    if historical["gender"]== "F":
                        female = 1
                    else:
                        female = 0
        # Load tweets of the senator
        try:
            feed = readjson(path+"/Input/tweets_"+handle+".json")
        except:
            print("No file for tweets of %s" % (handle))
            #continue
        # Attach tweets to dataframe
        for tweet in feed:
            tweet_text = tweet["full_text"]
            temp_df = pd.DataFrame([list([name, handle, tweet_text, female, govtrack])], columns = col_names)
            df = df.append(temp_df)

    # Estimation
    df.to_pickle(path+"/Output/clean_data.pkl")

    # Output
    print ("The dataframe has been pickled.\n")

###########################################################
### start main
if __name__ == "__main__":
    main()
