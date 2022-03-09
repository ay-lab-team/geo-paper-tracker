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



# Query for new datasets and papers
1. Open GEO_Query_for_HiChIP_DB.ipynb on JupyterHub
2. Run the entire GEO_Query_for_HiChIP_DB Jupyter Notebook should take aroud 2 minutes.

### Notes
1. If an error says you don't have access to use its tool, run the following at the top of GEO_Query_for_HiChIP_DB.ipynb:
```
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```
2. Search details `filters` and email address `Entrez.email` are set to defaults, but you can change these variables.

# Compare new datasets and papers with existing ones
1. Open GEO_Query_for_HiChIP_DB.ipynb on JupyterHub
2. Run the entire GEO_Query_for_HiChIP_DB Jupyter Notebook should take aroud 2 minutes.
