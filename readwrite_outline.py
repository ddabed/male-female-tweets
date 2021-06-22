#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
readwrite.py

Purpose:
    Fill in details to read and write a list of jsons

    Bonus: Can you figure out how to ensure you get a compressed file as output? E.g. with gzip?

Version:
    1          Outline only

Date:
    2021/5/12

Author:
    ???? & Charles Bos
"""
###########################################################
### Imports
import json
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

###########################################################
### ir= savejson(aJS, sFile)
def savejson(aJS, sFile):
    """
    Purpose:
        Save the JSON in the list to a file

    Inputs:
        aJS     list of JSON/dictionary elements
        sFile   string, filename to write to

    Return value:
        ir      integer, number of elements succesfully written
    """
    ir= 0
    with open(sFile, "at") as f:
        for jsonobj in aJS:
            jsonstr = json.dumps(jsonobj)
            f.write(jsonstr + "\n")
            ir += 1 

    # Fill in your code

    return ir

###########################################################
### aJS= readjson(sFile)
def readjson(sFile):
    """
    Purpose:
        Read the JSON from a file

    Inputs:
        sFile   string, filename to read from

    Return value:
        aJS     list of JSON/dictionary elements
    """
    aJS= []
    with open(sFile) as f:
        for line in f:
            try:
                aJS.append(json.loads(line))
            except:
                print("Line in a non-valid format.")
    return aJS

###########################################################
### main
def main():
    # Magic numbers
    sFile= 'output/rw.json'
    aJS= [{'user': 'Ines', 'text': 'Let us talk social media'}, {'user': 'Charles', 'text': 'Let us talk tweets'}, {'user': 'student', 'text': 'Really, why?', 'subtext': 'Or rather: Yes please!'}]

    # Initialisation
    print ('The JSON to write to file is:\n', aJS)

    # Estimation
    ir= savejson(aJS, sFile)

    aJSnew= readjson(sFile)

    # Output
    print ('Written %i elements to %s' % (ir, sFile))
    print ('Reading JSON from file gives:\n', aJSnew)

###########################################################
### start main
if __name__ == "__main__":
    main()
