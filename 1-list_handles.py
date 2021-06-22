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
import re
import pickle
import pdfplumber
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
        page                page object from pdfplumber

    Return value:
        handles_clean       list of strings, full names and tweeter handles
    """
    text = page.extract_text().split(" ")
    text = [word for word in text if len(word)>2]
    handles_clean = [[text[i-2]+" "+text[i-1],re.sub("\n","",text[i][1:])] 
                     for i in range(len(text)) if text[i][0]=="@"]

    return handles_clean

###########################################################
### main
def main():
    # Magic numbers
    path = os.getcwd()
    handles = []
    # Initialisation
    with pdfplumber.open(path + "/Input/116th-Congress-Twitter-Handles.pdf") as pdf:
        for page in pdf.pages:
            handles.extend(clean_pdf(page))
    
    # Pickle the list
    with open(path + '/Input/tweeter_handles.pkl', 'wb') as f:
        pickle.dump(handles, f)
    
    # Download representatives data
    r = requests.get("https://theunitedstates.io/congress-legislators/legislators-historical.json")
    savejson(r.json(), path+"/Input/us-legislators-database")

    # Output
    print ("Tweeter handles of U.S. representatives have been pickled.\n")

###########################################################
### start main
if __name__ == "__main__":
    main()
