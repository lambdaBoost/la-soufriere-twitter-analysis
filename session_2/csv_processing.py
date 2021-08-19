# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 13:28:17 2021

@author: Alex
"""

import pandas as pd


def tidy_df(filePath):
    
    df = pd.read_csv(filePath)
    #read in csv
    
    
    #drop first 4 rows
    
    df = df.iloc[4:,:]
    
    #remove spaces from column names
    
    df.columns = df.columns.str.replace(" ","_")
    
    #remove non  retweets
    df = df[df["Content"].astype(str).str.startswith("RT")]
    
    #remove non ascii characters and backspaces
    
    df['Content'] = df['Content'].str.replace('RT ','')
    df['Retweeter'] = df['Content'].str.split(' ').str[0]
    df['Retweeter'] = df['Retweeter'].str.replace(':','')
    
    df.dropna(axis = 0,how = 'any',subset = ['Retweeter'], inplace = True)
    
    
    df.replace({r'[^\x00-\x7F]+':''},regex = True, inplace = True)
    df.replace(r'\\' , '', regex = True, inplace = True)

    return df

df = tidy_df('retweet_data.csv')

preview = df.head()
