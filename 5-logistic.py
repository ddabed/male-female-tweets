#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
logistic.py

Purpose:
    Estimate a logistic regression model

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
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn import svm


###########################################################
### main
def main():
    # Magic numbers
    path = os.getcwd()
    df = pd.read_pickle(path + "/Output/data_w_topics.pkl")
    k = 40 # number of topics
    
    # Aggregate dataset
    coldic = {'topic_'+str(i):'mean' for i in range(k)}
    coldic['female']='mean'
    df.female = pd.to_numeric(df.female)
    data = df.groupby('name').agg(coldic)
    
    # Female count plot
    plt.figure()
    fig, ax = plt.subplots(1,2)
    sns.countplot(x=df.female, palette='hls', ax=ax[0]).set(title="Number of Tweets")
    sns.countplot(x=data.female, palette='hls', ax=ax[1]).set(title="Twitter Accounts", ylabel="")
    plt.savefig(path + '/Output/female_count.png', dpi=300)
    plt.show()
    
    # Estimation
    col_names = ['topic_'+str(i) for i in range(k-5)]
    logit_model=sm.Logit(data.female, data[col_names])
    result=logit_model.fit(method='bfgs', maxiter = 1000)
    print(result.summary2().as_latex())


    
###########################################################
### start main
if __name__ == "__main__":
    main()
