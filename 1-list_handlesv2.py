#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
list_handles.py

Purpose:
    Generate a list of tweeter handles for U.S. legislators (116th congress)
    and download json with data on them

Version:
    1       First start

Date:
    2021/06/07

Author:
    Diego Dabed
"""
###########################################################
### Imports
import pandas as pd
import tabula
import os
import requests
from readwrite_outline import savejson

###########################################################
### handles_clean = clean_pdf(page)
def clean_pdf(page):
    """
    Purpose:
        Extract the tweeter handles from the pdf file's page

    Inputs:
        page                list of tables from tabula

    Return value:
        df_dump             dataframe
    """
    df_dump = pd.DataFrame(columns=['State', 'Name', 'Twitter Handle'])
    for df in page:
        colnames = df.columns
        if "@" in colnames[2]:
            df = df.append(pd.DataFrame([list(df.columns)], 
                                    columns = df.columns), ignore_index = True)
            df.columns = ["State", "Name", "Twitter Handle"]
        df_dump = df_dump.append(df)
        df_dump.reset_index()

    return df_dump

###########################################################
### main
def main():
    # Magic numbers
    path = os.getcwd()
    # Initialisation
    pdf = tabula.read_pdf(path + "/Input/116th-Congress-Twitter-Handles.pdf", pages="all")
    handles = clean_pdf(pdf[:2])
    
    # Pickle the dataframe
    handles.to_pickle(path + '/Input/handles_df.pkl')
    
    # Download representatives data
    r = requests.get("https://theunitedstates.io/congress-legislators/legislators-historical.json")
    savejson(r.json(), path+"/Input/us-legislators-database")

    # Output
    print ("Tweeter handles of U.S. representatives have been pickled.\n")

###########################################################
### start main
if __name__ == "__main__":
    main()
