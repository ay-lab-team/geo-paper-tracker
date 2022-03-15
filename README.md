# geo-paper-tracker
Different tools for the synthesis of papers from the NCBI-DB/GEO using Python.

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

# Query new datasets for HiChIP database
## Query for new datasets and papers 
1. On JupyterHub, run `GEO_Query_for_HiChIP_DB.ipynb` that's inside the `geo-paper-tracker/` folder
2. The output Excel file should be `GEO_Query.<YYYY_MM_DD_HH_MM>.xlsx` in the same folder you ran `GEO_Query_for_HiChIP_DB.ipynb`, so `geo-paper-tracker/`.

### Notes
1. Search details `filters` and email address `Entrez.email` are set to defaults, but you can change these variables
2. Output Excel filename `output` is set to default, but you can change this variable
3. If you get `invalid ID "..." (rejeccted by Eutils)` error on one the cells, just rerun it.
4. (2-7 min depends on the search filters)

## Compare new datasets and papers with existing ones
If you have a Google Sheet of existing datasets and papers, run `GEO_Compare_for_HiChIP_DB_Initial_Run.ipynb` on JupyterHub. The old and new file paths are hard coded.
If you already have an Excel sheet created by `GEO_Query_for_HiChIP_DB.ipynb`, run `GEO_Compare_for_HiChIP_DB_Future_Runs.ipynb` on JupyterHub

# Generate a table linking GEO IDs with GSM and SRR IDs
The script Linking_GSE_to_SRA.py takes as input a GEO ID plus output directory to store the original soft.txt file (from GEO) and stores a table with links between the GSE, GSM and SRR ID's with metadata information.

