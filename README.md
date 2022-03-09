# geo-paper-tracker
Synthesis of papers from the NCBI-DB/GEO using Python.

# Set up
Create a dedicated conda environment if you would like:
```
conda create -n HiChIP-DB
conda activate HiChIP-DB
```

Install these Python packages using pip or conda:
```
pip install biopython
pip install metapub
```



# Query for new datasets and papers (2 min)
1. Run GEO_Query_for_HiChIP_DB.ipynb on JupyterHub
2. The output Excel file should be GEO_Query.<YYYY_MM_DD_HH_MM>.excel.

### Notes
1. If an error says you don't have access to use its tool, run the following at the top of GEO_Query_for_HiChIP_DB.ipynb:
```
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```
2. Search details `filters` and email address `Entrez.email` are set to defaults, but you can change these variables.
3. Outpute Excel file name `output` is set to default, but you can change this variable.



# Compare new datasets and papers with existing ones (seconds)
If you have a Google Sheet of existing datasets and papers:
1. Run GEO_Compare_for_HiChIP_DB_Initial_Run.ipynb on JupyterHub

If you already have an Excel sheet created by GEO_Query_for_HiChIP_DB.ipynb:
1. Run GEO_Compare_for_HiChIP_DB_Future_Runs.ipynb on JupyterHub
