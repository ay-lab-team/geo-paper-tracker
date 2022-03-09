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
Running the entire GEO_Query_for_HiChIP_DB Jupyter Notebook should take 

### Notes
If an error says you don't have access to use its tool, run the following at the top of GEO_Query_for_HiChIP_DB.ipynb:
```
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```
