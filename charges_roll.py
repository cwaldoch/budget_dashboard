# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 16:36:51 2019

@author: .3
"""
import pandas as pd
from os import walk

fileDirectory = r'C:\Users\.3\Desktop\cc_statements\\'

def file_walk(directory):
    file_name_list = []
    for (dirpath, dirnames, filenames) in walk(directory):
        file_name_list.extend(filenames)
        break
    return(file_name_list)

    
useFiles = file_walk(fileDirectory)

i = 0
for fName in useFiles:
    if fName == useFiles[0]:
        dfComplete = pd.read_csv(fileDirectory+fName)
    else:
        dfInt = pd.read_csv(fileDirectory+fName)
        dfs = [dfComplete, dfInt]
        dfComplete = pd.concat(dfs)
dfComplete = dfComplete[dfComplete['Type'] != 'Payment']

groceryTerms = ['HARRIS TEETER', 'JEWEL-OSCO', 'GIANT', 'SAFEWAY',
                'TRADER JOE', 'FARM', 'COSTCO', 'WHOLEFDS', 'KROGER',
                'FOOD CITY', 'WEGMANS']
petTerms = ['PETCO', 'ANIMAL', 'CHEWY', 'ROVER', 'VCA OLD', 'PETSMART']
gasCoffTerms = ['SHELL', 'SUNOCO', 'PETRO', 'EXXON', '7-ELEVEN', 'STARBUCKS', 
                'LUBE CENTER', 'PRIDE OF', 'GAS N GO', ' MART', 'DELIMART', 
                'BP#', 'DISCOUNT TIRE']
homeTerms = ['HOME DEPOT', 'TARGET', 'WAYFAIR', 'OVERSTOCK', 'Tree Service', 
             'HOMEDEPOT', 'LANDSCAPING', 'MERRIFIELD', 'BED BATH', 'BEACHCAMERA',
             'MICROSOFT', 'MICRO CENTER', 'GTBAD', 'BURPEE']
shoppingTerms = ['EXPRESS', 'MACYS', 'MARSHALL', 'ECCO', 'NORDSTROM', 'REI #',
                 'COST PLUS', 'OLD NAVY', 'BR FACTORY', 
                 'ETSY', 'ZAPPOS', 'Zappos', 'H&AMP']
amazonTerms = ['AMZN', 'AMAZON', 'Kindle', 'Amazon', 'Prime Video', 'Audible']
conTerms = ['KABOB', 'CVS', 'FREDDY', 'WAFC', 'DC FRAY', 'METRO FARE', 
            'MARIANNAGAI', 'BESTBUY', 'NAME-CHEAP']
erinTerms = ['LUSH', 'ULTA', 'Trunk Club', 'DEVACURL', 'ORANGETHEORY',
             'DAILY BURN', 'THRIVEWORKS', 'OTF OLD']
weddingTerms = ['CLINCH', 'ANDERSON', 'ZOLA', 'NORRIS', 'PRETENTIOUS BEER', 
                'SABRA', 'SIRENS', 'RADIANT GATHERING']
travelTerms = ['HOTEL', 'CHEAPOAIR', 'FRONTIER', 'DELTA', 'UNITED', 
               'SOUTHWEST', 'AMTRAK', 'Hotel', 'AMERICAN AIR', 'JETBLUE',
               'MAGPIES', 'MALNATIS', 'AUTOZONE', 'ZIEBART']
entertainmentTerms = ['PLAYSTATION', 'NINTENDO', 'BEST BUY',
            'EPIC GAMES', 'GMGINC', 'ORIGINCOM', 'CINEMA', 'ST PARK', 'TICKET',
            'LIVE NATION', 'PARKING', 'SLEEP NO', 'STEAM GAME', 'HISTORIC', 
            'IPHONE', 'NHP-','HUMBLEBUNDLE', 'BLIZZARDENT', 'MUSEUM', 'ARTECHOUSE']
dentalTerms = ['DENTAL']
utilityTerms = ['ARLINGTON', 'NOVA SOIL']

termsDict = {'pets':petTerms, 'gas and coffee':gasCoffTerms, 'home goods':homeTerms,
             'shopping':shoppingTerms, 'amazon':amazonTerms, 
             'connor':conTerms, 'groceries':groceryTerms, 'wedding':weddingTerms,
             'travel':travelTerms,'dental':dentalTerms,
             'entertainment':entertainmentTerms, 'erin':erinTerms, 
             'utilities':utilityTerms}

allWords = []
for idx,row in dfComplete.iterrows():
    descWords = row['Description'].split(' ')
    for word in descWords:
        allWords.append(word)
         
dfWords = pd.DataFrame(allWords, columns = ['word pieces'])
dfWords.to_csv('all_words.csv', index=False)

allResults = []
for idx,row in dfComplete.iterrows():
    rowResults = []
    for key in termsDict.keys():
        for term in termsDict[key]:
            if term in row['Description']:
                rowResults.append(key)
            else:
                None
    if len(rowResults) == 0:
        rowResults = 'None'
    allResults.append(rowResults)

dfComplete['Desc Tags'] = allResults

refinedTags = []
for idx, row in dfComplete.iterrows():
    if row['Desc Tags'] == 'None':
        if row['Category'] == 'Food & Drink':
            refinedTags.append(['eating out'])
        elif row['Category'] == 'Shopping':
            refinedTags.append(['Undefined Purchase'])      
        elif row['Category'] == 'Travel':
            refinedTags.append(['Travel'])  
        else:
            refinedTags.append(row['Category'])
    else:
        refinedTags.append(row['Desc Tags'])


    
dfComplete['Refined Tags'] = refinedTags
        



dfComplete.to_csv(r'C:\users\.3\Desktop\billing_output.csv', index=False)