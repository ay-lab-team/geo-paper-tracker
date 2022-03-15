#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
from Bio import Entrez

import os 
import pandas as pd
from datetime import date
from datetime import datetime
import numpy as np
import re
from metapub import FindIt
from metapub.convert import pmid2doi
from metapub.convert import doi2pmid
from metapub import PubMedFetcher

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# ## Setting the output path

# In[2]:


# make an output directory
outdir = 'results/hichip_db/'
os.makedirs(outdir, exist_ok=True)


# In[3]:


# determining the current year, month and day
today = date.today()
date_str = today.strftime("%Y_%m_%d")

# determining current hour and minute
now = datetime.now()
time_str = now.strftime("%H_%M")

# setting the output filename
output = os.path.join(outdir, "GEO_Query.{}_{}".format(date_str, time_str))


# ## Query the NCBI database

# In[4]:


# define a search query/filters
filters = "hichip[All Fields] AND (\"Homo sapiens\"[Organism] AND \"published last year\"[Filter]) AND \"gse\"[Filter]"

# set a dummy email 
Entrez.email = "zjiang@lji.org"

# query the NCBI database 
search_result = Entrez.esearch(db="gds", retmax=10000, term=filters)
result = Entrez.read(search_result)

# creating a regex to extract pubmed IDs
PubMedIds_pattern = re.compile('[0123456789]+')


# In[5]:


# parse the results into a dataframe 
dictionary_lst = []
for Id in result["IdList"]:
    handle = Entrez.esummary(db="gds", id=Id, retmode="xml") # get summary of this entry on GEO datasets
    entry = Entrez.parse(handle)
    for column in entry:
        dictionary_lst.append(column)
df = pd.DataFrame(dictionary_lst)


# In[6]:


df.head()


# ## Cleaning the Paper Names and Converting from PMID to DOI

# In[7]:


dictionary_lst = []
for Id in result["IdList"]:
    
    handle = Entrez.esummary(db="gds", id=Id, retmode="xml")
    entry = Entrez.parse(handle)
    
    for column in entry:
        paper_title = column['title']
        new_paper_title = ''
        last_word = re.split('\s|[.]', paper_title)[-1]
        last_two_words = re.split('\s|[.]', paper_title)[-2:]
        
        # remove ".[HiChIP]", ". [HiChIP]", or "(HiChIP)" in paper titles using steps below
        if ('[' in last_word and ']' in last_word) or                 ('(' in last_word and ')' in last_word):
            new_paper_title = re.split('\s|[.]', paper_title)[0:-1]
            new_paper_title = ' '.join(new_paper_title)
            new_paper_title = new_paper_title.strip()
            if new_paper_title.endswith('.'): # remove the last period in paper title
                new_paper_title = new_paper_title[:-1]
                
        # remove ".[Hi ChIP]", ". [Hi ChIP]", or "[Bead Array]" in paper titles using steps below
        elif ('[' in last_two_words[0] and ']' in last_two_words[1]) or                     ('(' in last_two_words[0] and ')' in last_two_words[1]):
            new_paper_title = re.split('\s|[.]', paper_title)[0:-2]
            new_paper_title = ' '.join(new_paper_title)
            new_paper_title = new_paper_title.strip()
            if new_paper_title.endswith('.'): # remove the last period in paper title
                new_paper_title = new_paper_title[:-1]
                
        elif paper_title.endswith('.'):
            new_paper_title = paper_title[:-1] 
            
        else:
            new_paper_title = paper_title
            
        new_paper_title = new_paper_title.replace("\xa0", " ") # remove no-break space
        column['title'] = new_paper_title
        
        # convert PMID to DOI, some have no PMID so empty string
        string = str(column['PubMedIds'])
        pdf_url = ""
        PubMedIds = PubMedIds_pattern.findall(string)
        
        if len(PubMedIds) > 0:
            DOI = pmid2doi(PubMedIds[0])
            column['PubMedIds'] = DOI
        else: column['PubMedIds'] = ""
        dictionary_lst.append(column)
        
df = pd.DataFrame(dictionary_lst)


# ## Reformat the Columns for Google Sheet Compatibility

# In[ ]:


df = pd.DataFrame(dictionary_lst)

# drop extra columns
drop_cols = ['Item', 'Id', 'GDS', 'GPL', 'GSE', 'entryType', 'ptechType',
             'valType', 'SSInfo', 'subsetInfo', 'suppFile', 'Relations', 'ExtRelations',
             'n_samples', 'SeriesTitle', 'PlatformTitle', 'PlatformTaxa', 'SamplesTaxa',
             'Projects', 'FTPLink', 'GEO2R']
df.drop(drop_cols, inplace=True, axis=1)

# rename columns
rename_cols = {"Accession":"GEO / Data link", "PubMedIds":"DOI", "title":"Paper Title",
               "taxon":"Organism", "gdsType":"Any other information", "PDAT":"Year",
               "Samples":"Other matched data"}
df.rename(columns=rename_cols, inplace=True)

# extract just the year
df["Year"] = df["Year"].str[:4]

# add index for merging
df['index'] = np.arange(len(df))

# fill na with empty values
df.fillna("",inplace=True)

# adding missing columns with empty values
df["Journal"] = ""
df["Authors"] = ""
df["Tissue/Cell Line"] = ""
df["Presenter"] = ""
df["Potential HiChIP"] = ""


# ## Assigning Potential HiChIP Samples

# Filter out samples with no HiChIP mention and assigned Yes or Maybe to all others 

# In[ ]:


col = df["Other matched data"]
lst = []
index = 0
for row in col:
    
    temp = []
    state = False
    
    # Check for the term HiChIP in the title
    for ele in row: 
        if ("HiChIP".casefold() in ele["Title"].casefold()) or                 ("Hi-ChIP".casefold() in ele["Title"].casefold()):
            state = True
    
    # keep samples with HiChIP and mark "Yes"
    if state == True: 
            for ele in row:
                if ("HiChIP".casefold() in ele["Title"].casefold()) or                         ("Hi-ChIP".casefold() in ele["Title"].casefold()):
                    temp.append(ele["Accession"] + ": " + ele["Title"])
            temp_str = "\n".join(temp)
            df.at[index, "Potential HiChIP"] = "Yes"

    # otherwise, keep all GSM samples and mark "Maybe"
    else: 
        for ele in row:
            temp.append(ele["Accession"] + ": " + ele["Title"])
        temp_str = "\n".join(temp)
        df.at[index,"Potential HiChIP"]="Maybe"
    lst.append(temp_str)
    index += 1
    
df["Other matched data"] = list(lst)


# ## Merge Rows with the Same Paper Title

# In[ ]:


aggregation_functions = {'Paper Title':'first', 'DOI':'max', 'Journal':'first', 'Authors':'first', 'Year':'first', 'GEO / Data link':lambda x: '\n'.join(x),
       'Any other information':lambda x: '\n'.join(x), 'Organism':'first', 'Tissue/Cell Line':'first',
       'Potential HiChIP':'first', 'Other matched data':lambda x: '\n'.join(x), 'Presenter':'first'}
df_grouped = df.groupby(df['Paper Title']).aggregate(aggregation_functions)
df_grouped['Date Added'] = date_str.replace('_', '-')
df_grouped


# ## Fetch Journal Name and First Author of Each Paper

# In[ ]:


jounrnal_lst = []
authors_lst = []
fetch = PubMedFetcher()
for DOI in df_grouped['DOI']:
    try:
        PMID = doi2pmid(DOI)
        article = fetch.article_by_pmid(PMID)
        jounrnal_lst.append(article.journal)
        authors_lst.append(article.authors[0].split()[0] + " et al.")
    except:
        jounrnal_lst.append("")
        authors_lst.append("")
df_grouped['Journal'] = jounrnal_lst
df_grouped['Authors'] = authors_lst


# In[ ]:


df_grouped


# In[ ]:


# add http address to DOI (for easy access)
df_grouped.loc[(df_grouped['DOI'] != ''), 'DOI'] = 'https://doi.org/' + df_grouped.loc[(df_grouped['DOI'] != ''), 'DOI']


# In[ ]:


reorder = ['Paper Title',
         'Journal',
         'Authors',
         'Year',
         'DOI',
         'GEO / Data link',
         'Any other information',
         'Organism',
         'Tissue/Cell Line',
         'Other matched data',
         'Presenter',
         'Date Added']
#t = df_grouped.loc[:, reorder]
df_grouped = df_grouped.loc[:, reorder]


# ## Save the final output file

# In[ ]:


df_grouped.to_excel(output + ".xlsx", index=False)


# In[ ]:


df_grouped


# In[ ]:




