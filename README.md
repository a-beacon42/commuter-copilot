# Commuter Copilot
is a RAG-based, offline coding assistant. Inspiration for this project came when my commute changed & I found the new route had terrible cell/hotspot/wifi service. My solution was to develop a containerized app so I can run an LLM locally. To improve responses, I indexed tech documentation that was published after the model's knowledge cutoff.  

## design draft
![Commuter Copilot](/docs/images/commuter_copilot_design_draft.jpg)

## etl
![ETL System](/docs/images/data_ingestion_system.png)
### step 1: get Azure raw docs
 - pull updates from [MicrosoftDocs/azure-docs](https://github.com/MicrosoftDocs/azure-docs) to my local storage.  
 - scripted: commuter_copilot/data/etl/extract/update_local_azure_docs_raw.sh

### step 2: process raw docs
- find all md files in repo
- for each file: 
  - get metadata & match index schema
  - break into sections by headers
  - chunk each section
  - compose everything to json
  - write to local storage
- python script: commuter_copilot/data/etl/transform.py

### step 3: index docs to elasticsearch index
- connect to ES client
- get docs from local staging
- write/update docs to index   
- python script: commuter_copilot/data/etl/load.py

<hr>

**todo**:  
- schedule triggers for automated batch updates
- incorporate into main pipeline for regular refresh of search index  
  
<hr>
<hr>  
  
## query service
### retrieve docs
### augment prompt
### generate response

## ui
