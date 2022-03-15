#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from Bio import Entrez
import pandas as pd
from datetime import date
from datetime import datetime
import re


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
output = os.path.join(outdir, "GEO_Compare.{}_{}".format(date_str, time_str))


# In[4]:


output


# In[5]:


# get the newest and second newest paper tables
old = "results/hichip_db/HiChIP_Databases.Google_Download.2022_03_09_09_16.xlsx"
new = "results/hichip_db/GEO_Query.2022_03_09_09_47.xlsx"
old_df = pd.read_excel(old)
new_df = pd.read_excel(new)


# ##  Compare old and new GEO IDs

# In[6]:


# make a regex to extract GEO ID
GEO_pattern = re.compile('GSE[0123456789]+')

# make a set of old GEO IDs
old_GEOs = set()
for x in old_df['GEO / Data link'].tolist():
    GEO = GEO_pattern.findall(x)
    old_GEOs.update(GEO)

# make a set of new GEO IDs
new_GEOs = set()
for x in new_df['GEO / Data link'].tolist():
    GEO = GEO_pattern.findall(x)
    new_GEOs.update(GEO)

# compare the sets of GEO IDs
differences_GEOs = new_GEOs.difference(old_GEOs)


# In[7]:


# create an indicate column of papers whose GEO ID is not in the old table 
bools = []
for geoid_strings in new_df['GEO / Data link'].tolist():
    
    geo_status = False
    for geoid in geoid_strings.split():
        if geoid in differences_GEOs:
            geo_status = True
            break
    bools.append(geo_status)

differences_df = new_df.loc[bools]

# replace na with empty string
differences_df.fillna("", inplace=True)


# In[8]:


differences_df


# ## Save the output file

# In[9]:


differences_df.to_excel(output + ".xlsx", index=False)

