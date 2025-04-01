"""
execute the ETL pipeline:

extractor = DataExtractor(source data path, source data type (json, md, html, etc.))
transformer = DataTransformer(transformation steps)
loader - DataLoader(target data path)

etl = ETL(extractor, transformer, loader)

etl.run():
    self.extractor.extract()
    self.transformer.transform()
    self.loader.load()

"""

# todo: translate to GHA -> move to root/.github/.workflows/etl_azure_docs.yml

# %%

from data.etl.extract.extract import Extractor

DATA_SOURCE_PATH = "../../../azure-docs"


extractor = Extractor(source_path=DATA_SOURCE_PATH, source_type=".md")
all_md_filepaths = extractor.extract()
print(f"found {len(all_md_filepaths)} md files in: {DATA_SOURCE_PATH}")

# %%

sample_md_paths = all_md_filepaths[345:365]
one_path = all_md_filepaths[375]

with open(one_path, "r", encoding="utf-8") as file:
    raw_content = file.read()

print(raw_content[:1000])  # Print the first 1000 characters of the raw content
# %%
import re
import yaml


def extract_yaml_frontmatter(text):
    """
    Extracts YAML frontmatter from the markdown text.
    Returns a tuple (metadata, content_without_frontmatter).
    """
    # This regex expects the frontmatter to be enclosed between --- lines at the beginning
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, text, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        content = match.group(2)
        metadata = yaml.safe_load(yaml_text)
        return metadata, content
    # if no frontmatter is found, return empty metadata and full text
    return {}, text


metadata, content = extract_yaml_frontmatter(raw_content)

# %%
