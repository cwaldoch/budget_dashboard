# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 08:56:09 2019

@author: CWaldoch
"""

import pandas as pd
from os import walk
import matplotlib.pyplot as plt

#fileDirectory = r'C:\Users\.3\Desktop\cc_statements\\'
#
#def file_walk(directory):
#    file_name_list = []
#    for (dirpath, dirnames, filenames) in walk(directory):
#        file_name_list.extend(filenames)
#        break
#    return(file_name_list)
#
#    
#useFiles = file_walk(fileDirectory)
#
#i = 0
#for fName in useFiles:
#    if fName == useFiles[0]:
#        dfComplete = pd.read_csv(fileDirectory+fName)
#    else:
#        dfInt = pd.read_csv(fileDirectory+fName)
#        dfs = [dfComplete, dfInt]
#        dfComplete = pd.concat(dfs)
#dfComplete = dfComplete[dfComplete['Type'] != 'Payment']

dfComplete = pd.read_csv(r"C:\Users\cwaldoch\Desktop\sfhss\total_charges.csv")

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

termsDict = {'pets':petTerms, 'Gas':gasCoffTerms, 'home goods':homeTerms,
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
    if type(rowResults) == list:
        rowResults = rowResults[0]
    allResults.append(rowResults)

dfComplete['Desc Tags'] = allResults

refinedTags = []
for idx, row in dfComplete.iterrows():
    if row['Desc Tags'] == 'None':
        if row['Category'] == 'Food & Drink':
            refinedTags.append('eating out')
        elif row['Category'] == 'Shopping':
            refinedTags.append('Undefined Purchase')      
        elif row['Category'] == 'Travel':
            refinedTags.append('Travel')  
        else:
            refinedTags.append(row['Category'])
    else:
        refinedTags.append(row['Desc Tags'])

dfComplete['Refined Tags'] = refinedTags

df = dfComplete

df['date2'] = pd.to_datetime(df['Transaction Date'])
df['month_year'] = pd.to_datetime(df['date2']).dt.to_period('M')

#df2 = df.groupby(['month', 'Refined Tags']).sum()

tagDict = {'utilities':'Utilities/Loans/Bills',
 'dental':'Utilities/Loans/Bills',
 'Education':'Discretionary',
 'amazon':'Discretionary',
 'erin':'Discretionary',
 'Gas':'Driving+Work Transit',
 'Travel':'Travel',
 'pets':'Pets',
 'metro':'Driving+Work Transit',
 'Professional Services':'Discretionary',
 'Home':'Discretionary',
 'Personal':'Discretionary',
 'Entertainment':'Enertainment',
 'eating out':'Food Out',
 'shopping':'Discretionary',
 'groceries':'Food In',
 'connor':'Discretionary',
 'Bills & Utilities':'Utilities/Loans/Bills',
 'Undefined Purchase':'Enertainment',
 'Groceries':'Food In',
 'CC':'CC Stuff',
 'wedding':'Wedding',
 'Health & Wellness':'Discretionary',
 'entertainment':'Enertainment',
 'travel':'Travel',
 'Gifts & Donations':'Discretionary',
 'home goods':'Discretionary',}

tag2Dict = {'utilities':'Utilities/Loans/Bills',
 'dental':'Health',
 'Education':'Education',
 'amazon':'Amazon',
 'erin':'Personal',
 'Gas':'Driving+Work Transit',
 'Travel':'Travel',
 'pets':'Pets',
 'metro':'Driving+Work Transit',
 'Professional Services':'Home',
 'Home':'Home',
 'Personal':'Discretionary',
 'Entertainment':'Enertainment',
 'eating out':'Food Out',
 'shopping':'Discretionary',
 'groceries':'Food In',
 'connor':'Personal',
 'Bills & Utilities':'Utilities/Loans/Bills',
 'Undefined Purchase':'Personal',
 'Groceries':'Food In',
 'CC':'CC Stuff',
 'wedding':'Wedding',
 'Health & Wellness':'Health',
 'entertainment':'Enertainment',
 'travel':'Travel',
 'Gifts & Donations':'Discretionary',
 'home goods':'Home',}


df['Final Tags'] = [tagDict[x] for x in df['Refined Tags'].values]
df['Mid Tags'] = [tag2Dict[x] for x in df['Refined Tags'].values]
df['Spend'] = df['Amount']*-1

fig, ax = plt.subplots(figsize=(15,7))
df.groupby(['month_year', 'Mid Tags']).sum()['Spend'].unstack().plot(ax=ax, linewidth=3)
plt.savefig('testg3.png', dpi=300)
df2 = df.groupby(['month_year', 'Final Tags']).sum()['Spend']

df2.to_csv('avg_dfspend_extend.csv', index=False)
df.to_csv('dfspend_extend.csv', index=False)
