"""
class Extractor:
    def extract():
        1. update forked repo from upstream
            - git fetch upstream (MicrosoftDocs/azure-docs)
            - git checkout main
            - git merge upstream/main
        2. fetch updates from commuter-copilot/azure-docs
        3. return list of files to be processed

    break steps into functions & write tests for each function
"""

import os


class Extractor:
    def __init__(self, source_path: str, source_type: str):
        self.source_path = source_path
        self.source_type = source_type

    def extract(self) -> list:
        if self.source_type == ".md":
            return find_all_target_docs(self.source_path)
        else:
            raise ValueError("Unsupported source type")


# find all target file type in repo
def find_all_target_docs(path_to_docs: str, target_doc_type: str = ".md") -> list:
    """Crawl through the repo and get paths to all markdown files."""
    markdown_files = []
    for dirpath, dirnames, filenames in os.walk(path_to_docs):
        for file in filenames:
            if file.endswith(target_doc_type):
                markdown_files.append(os.path.join(dirpath, file))
    return markdown_files


# # %%
# """
# forked & cloned the azure docs repo to `../../../azure-docs`
# 1. find_all_docs(path_to_docs:str, doc_type:str = 'md'):
#         crawl through repo & get path to all markdown files
#         return [paths, to, markdown, files]
# 2. process_raw_doc_to_json(path_to_doc:str, doc_type:str = 'md'):
#         read in raw doc_type file
#         return json {text, title, metadata}
# 3. load_processed_doc_to_staging(processed_doc:json, path_to_staging: str):

# """
# import os

# target_file_type = "md"

# # extract = get from repo -> filter for md -> convert to json -> load to staging (../local_files/data/staging/azure_docs)


# # placeholder for fetching azure doc updates
# # ? how to run git commands in python?


# def process_raw_doc_to_json(path_to_doc: str, doc_type: str = "md") -> dict:
#     """Read in raw doc_type file and return json {text, title, metadata}."""
#     with open(path_to_doc, "r", encoding="utf-8") as file:
#         content = file.read()
#     # placeholder for processing logic
#     # ? how to extract metadata from markdown files?
#     # ? how to chunk content into smaller pieces?
#     # ? how to generate embedding of chunk?

#     return {"text": content, "title": os.path.basename(path_to_doc), "metadata": {}}


# def stage_processed_doc(processed_doc: dict, path_to_staging: str) -> None:
#     """Load processed doc to staging."""
#     os.makedirs(path_to_staging, exist_ok=True)
#     file_name = os.path.join(path_to_staging, processed_doc["title"] + ".json")
#     with open(file_name, "w", encoding="utf-8") as file:
#         file.write(str(processed_doc))
