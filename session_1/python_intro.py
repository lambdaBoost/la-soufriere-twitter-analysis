#variables

#declare variable - numbers
a = 1

#strings
a_string = 'abc'

#booleans
a_bool = True

#lists
a_list = [1,2,3,4,5]
element = a_list[2]

#%%
#flow control

#for loops
for i in a_list:
    print(i)
    

#if statements
for i in a_list:
    if(i%2 != 0):
        print(i)


#%%
#functions

def return_odd(my_list):
    
    for i in my_list:
        if(i%2 != 0):
            print(i)
            

return_odd([4,5,6,7,8,9])
            


#%%
#importing libraries

def find_mean(my_list):
    
    ls_sum = 0
    for i in my_list:
        ls_sum = ls_sum + i
        
    ls_mean = ls_sum / len(my_list)
    
    return ls_mean

import statistics

statistics.mean(a_list)

#shortcut to import a given function
from statistics import mean as mn
mn(a_list)



#%%

import pandas as pd

dataframe = pd.read_csv('2104014_LaSouf_RTs.csv')

dataframe.dtypes

#extract and save a column
col = dataframe['Content']

#as above for rows
row = dataframe.iloc[5]


#import a second dataframe
dataframe_2 = pd.read_csv('trial_tweet_data.csv')

#manipulation / summarisation of a column
mn(dataframe_2['Author Listed Count'])

#column sum
dataframe_2['Author Listed Count'].sum()

#first few rows
df_head = dataframe.head()

#filtering data
liked_tweets = dataframe_2[dataframe_2['Number of Likes'] > 0]
