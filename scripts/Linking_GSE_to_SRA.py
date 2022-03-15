#!/usr/bin/env python
# coding: utf-8

import os 
import sys
import argparse
import GEOparse
import pandas as pd
import numpy as np
import pysradb
import subprocess as sp

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# get commandline values
gse_id = sys.argv[1] #'GSE101498'
outdir = sys.argv[2]

# ## Setting the output path

# # make an output directory
outdir = 'results/hichip_db/gse/'
os.makedirs(outdir, exist_ok=True)

# setting the output filename
output = os.path.join(outdir, "GSE_Query.{}.tsv".format(gse_id))
print('Writing the output to: "{}".'.format(output))

# ## Query GEO for GSE metadata
# query the current GSE ID
geo_query = GEOparse.get_GEO(geo=gse_id, destdir=outdir, include_data=True, silent=True)

# parse through the information and make a useful table
gsm_data = []
for gsm_id, gsm in geo_query.gsms.items():
    
    title = '; '.join(gsm.metadata['title'])
    organism = ', '.join(gsm.metadata['organism_ch1'])
    source = ', '.join(gsm.metadata['source_name_ch1'])
    description = '; '.join(gsm.metadata['description'])
    
    for sra_link in gsm.relations['SRA']:
        # extracting the title, organism, source and description
        info = [gse_id,
                gsm_id,
                title,
                organism,
                source,
                description,
                sra_link]
        gsm_data.append(info)

gsm_data = pd.DataFrame(gsm_data)
gsm_data.columns = ['geo_id', 'gsm_id', 'title', 'organism', 'source', 'description', 'srx_link']

# extract SRA ID's
sra_ids = gsm_data['srx_link'].str.extract('(SRX[0-9]+)').squeeze()
gsm_data['srx_id'] = sra_ids

# loading the SRA tool
sra_querytool = pysradb.sraweb.SRAweb()

# query the SRA 
sra_query = sra_querytool.sra_metadata(gsm_data['srx_id'].values.tolist(), expand_sample_attributes=True)

meta = pd.merge(gsm_data,
                sra_query, left_on='srx_id',
                right_on='experiment_accession',
                suffixes=['_geo', '_sra'])

# calculating the number reads using the total number of spots
meta.loc[:, 'num_reads'] = meta.loc[:, 'total_spots'].astype(int) * 2


# ## Save the merged dataframe with all fields

meta_fn = os.path.join(outdir, '{}.meta.all_columns.xlsx'.format(gse_id))
meta.to_excel(meta_fn, index=False)


# ## Save the merged dataframe with most important columns

# most of these dropped columns are not needed, empty and some are redundant (specified)
# these columns are not dropped explicity with a drop call, but rather I extract only 
# the final columns I am interesting. The list below serves a book keeping purpose. 
drop_cols = ['sample_title', # empty
             'sample_organism', # redundant with organism
             'organism_taxid', 
             'library_name',
             'instrument',
             'instrument_model',
             'instrument_model_desc',
             'srx_link',
             'srx_id',
             'sample_accession',
             'study_accession',
             'study_title',
             'experiment_accession',
             'experiment_title',
             'experiment_desc',
             'organism_taxid',
             'library_name',
             'library_strategy',
             'library_source',
             'library_selection',
             'instrument',
             'instrument_model',
             'instrument_model_desc',
             'total_size',
             'run_total_spots',
             'run_total_bases', 
             'total_spots',
             'library_layout'] # not needed since all HiC data has to be completed with paired data

# setting the final columns
final_cols = ['geo_id',
             'gsm_id',
             'run_accession',
             'title',
             'source',
             'description',
             'organism',
             'num_reads']

# saving a table with the original column names
orig_cols_fn = os.path.join(outdir, '{}.meta.major_columns.original.xlsx'.format(gse_id))
meta[final_cols].to_excel(meta_fn, index=False)

# renaming the columns
final_renames = {'run_accession': 'srr_id',
                 'title': 'geo_title',
                 'source': 'geo_source',
                 'description': 'geo_description'}

# extracting the final data
final_df = meta[final_cols].rename(columns=final_renames)

# saving a table with the new column names
renamed_cols_fn = os.path.join(outdir, '{}.meta.major_columns.renamed.xlsx'.format(gse_id))
final_df.to_excel(renamed_cols_fn, index=False)
