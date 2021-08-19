# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 13:47:36 2021

@author: ahall

Completed version of the script from session 2
Takes a directory and trawls through it to find all relevant csv files
Performs processing on the files to make them useable for processing
writes the processed file to disk

To use this script, alter the objects in lines 19-28 (ie the global variables defined in uppercase)
"""
import pandas as pd
import numpy as np
import os
import fnmatch

#this is the location we will save the processed files to
NEO4J_IMPORT = 'C:\\Users\\ahall\\.Neo4jDesktop\\relate-data\\dbmss\\dbms-56c2f425-0f63-4435-9857-d09f5fe08efc\\import'
#path to our unprocessed data
DATA_PATH = 'C:\\Users\\ahall\\Documents\\projects\\la-soufriere-sentiment-analysis\\Sentiment Data - FULL DATASET'

#string which can be used to identify the retweet file names
RETWEET_FILE_IDENTIFIER = '*LaSouf_RTs.csv'
#string which can be used to identify the tweet file names
TWEET_FILE_IDENTIFIER = '*LaSouf_noRTs.csv'




def get_data(path, identifier):
    """
    #trawls through a given directory and retrieved all matching csv files
    concatenates the csvs together and outputs a single table
    
    Parameters
    ----------
    path : str
    path to the directory which contains the raw csv files. The files may be contained recursivley in sub-directories
    identifier : str
    A unique identifier which identifies the required files by name.
    """
    
    #initialise empty list of matching filenames
    matches = []
    
    #walk threough the target directory and get the names of all matching files
    for root, dirnames, filenames in os.walk(DATA_PATH):
        for filename in fnmatch.filter(filenames, identifier):
            matches.append(os.path.join(root, filename))
            
    #initialise an empty dataframe        
    df_out = pd.DataFrame()
    
    #iterate through the list of matching files and append to the output dataframe
    for match in matches:
        df = pd.read_csv(match)
        
        #drop first four rows
        df = df.iloc[4: , :]
        
        df_out = df_out.append(df, ignore_index = True)
        
    return df_out


def tidy_df(df, retweets):
    
    """
    takes a pandas table of tweets or retweets and performs necessary processing
    returns a new dataframe
    
    Parameters
    ----------
    df : DataFrame
    the data frame to be processed
    retweets : bool
    Set true if the data contains retweets. False if it contains only tweets
    """
    
    raw = df
    
    #add id column
    raw['ID'] = np.arange(len(raw))
    
    #remove spaces from column names
    raw.columns = raw.columns.str.replace(' ','_')
    
    #remove non ascii characters from text columns
    #also remove backslashes to make life easier
    raw.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
    raw.replace(r'\\','', regex=True, inplace=True)
    
    if(retweets):
        
        #filter out non retweets
        raw = raw[raw['Content'].astype(str).str.startswith('RT')]
        
        #kludge to get unique ids for retweets
        raw['ID'] = raw['ID'] + 1000000
        
        #split out retweet from author and make new column
        raw['Content'] = raw['Content'].str.replace('RT ', '')
        raw['Retweet_From'] = raw['Content'].str.split(' ').str[0]
        raw['Retweet_From'] = raw['Retweet_From'].str.replace(':', '')
        
        #drop rows with no tweet from author
        raw.dropna(axis = 0, how = 'any',subset = ['Retweet_From'], inplace = True )

    return raw
    

#this line isn't strictly necessary but it allows the script to run if called externally
if __name__ == "__main__":
    
    #call the functions above and save the csv file to the chosen folder
    tweet_data = get_data(DATA_PATH, TWEET_FILE_IDENTIFIER)
    retweet_data = get_data(DATA_PATH, RETWEET_FILE_IDENTIFIER)
    
    tweet_data = tidy_df(tweet_data, False)
    retweet_data = tidy_df(retweet_data, True)
    
    tweet_data.to_csv(os.path.join(NEO4J_IMPORT, 'tweets.csv'))
    retweet_data.to_csv(os.path.join(NEO4J_IMPORT, 'retweets.csv'))