"""
# placeholder for transformation step:
1. open md file
2. extract metadata
3. extract content
4. chunk content into smaller pieces
5. enrich chunk with metadata
6. generate emedding of chunk
4. convert to json
5. return json
"""

import os
import re
import yaml


class Transformer:
    # todo: refactor this to support multiple source/target types
    def __init__(self):
        self.source_type = ".md"
        self.target_type = "json"

    def transform(self, all_md_filepaths: list) -> list:
        """
        Transform the extracted data into a desired format.
        Args:
            all_md_filepaths (list): List of file paths to the extracted markdown files.
        Returns:
            list: List of transformed documents.
        """
        transformed_docs = []
        for filepath in all_md_filepaths:
            transformed_doc = self.process_markdown_file(filepath)
            transformed_docs.append(transformed_doc)

        return transformed_docs

    # def transform_single_md(
    #     filepath: str,
    # ) -> dict:
    #     """
    #     Transform a single markdown file into a desired format.
    #     Args:
    #         filepath (str): Path to the markdown file.
    #     Returns:
    #         dict: Transformed document.
    #     """
    #     with open(filepath, "r", encoding="utf-8") as file:
    #         raw_content = file.read()
    #         metadata, raw_doc = extract_yaml_frontmatter(raw_content)
    #         doc_sections = split_by_headings(raw_doc)
    #         # Placeholder for actual transformation logic
    #         print(f'{filepath}: {process}')

    def extract_yaml_frontmatter(self, text):
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

    def split_by_headings(self, text):
        """
        Splits the markdown text into sections based on Markdown headings.
        Each section is returned as a tuple (heading, section_text).
        If a section starts with a heading (e.g. "# Heading Title"),
        the heading is extracted and the remainder is considered the body.
        """
        # The regex splits the text when a line starts with '#' (but keeps it in the result)
        sections = re.split(r"\n(?=#)", text)
        enriched_sections = []
        for section in sections:
            lines = section.splitlines()
            heading = ""
            if lines and lines[0].startswith("#"):
                # Extract heading text by stripping '#' characters and whitespace
                heading = lines[0].lstrip("# ").strip()
            enriched_sections.append((heading, section.strip()))
        return enriched_sections

    def chunk_section(self, text, max_words=200):
        """
        Splits the given text into chunks where each chunk has at most max_words.
        If the section is short, it returns a single chunk.
        """
        words = text.split()
        if len(words) <= max_words:
            return [text]
        chunks = []
        # Create chunks using a sliding window (here, a simple non-overlapping window)
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i : i + max_words])
            chunks.append(chunk)
        return chunks

    def process_markdown_file(self, file_path, max_words=200):
        """
        Reads a markdown file, extracts its YAML frontmatter and content,
        splits the content by headings and further chunks sections by word count.
        Returns a list of enriched document dictionaries.
        Each dictionary contains:
        - file: the file name
        - metadata: the YAML metadata from the frontmatter
        - heading: the section heading (if available)
        - chunk_index: an index number for the chunk
        - content: the text chunk
        """
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        metadata, content = self.extract_yaml_frontmatter(text)
        sections = self.split_by_headings(content)

        documents = []
        chunk_counter = 0
        for heading, section in sections:
            # If the section starts with a heading, remove the heading line from the content body
            section_lines = section.splitlines()
            if section_lines and section_lines[0].startswith("#"):
                section_body = "\n".join(section_lines[1:]).strip()
            else:
                section_body = section

            # Skip if there is no meaningful content in the section
            if not section_body:
                continue

            # Further split the section by word count if needed
            chunks = self.chunk_section(section_body, max_words)
            for chunk in chunks:
                doc = {
                    "file": os.path.basename(file_path),
                    "metadata": metadata,
                    "heading": heading,
                    "chunk_index": chunk_counter,
                    "content": chunk,
                }
                documents.append(doc)
                chunk_counter += 1
        return documents


# def process_directory(directory_path, max_words=200):
#     """
#     Processes all Markdown files in the given directory.
#     Returns a list of enriched document dictionaries for all files.
#     """
#     all_documents = []
#     for filename in os.listdir(directory_path):
#         if filename.lower().endswith(".md"):
#             file_path = os.path.join(directory_path, filename)
#             docs = process_markdown_file(file_path, max_words)
#             all_documents.extend(docs)
#     return all_documents


# # --- Example usage ---
# if __name__ == "__main__":
#     # Set the directory path where your Markdown files are located
#     markdown_dir = "./azure_docs_md"  # change this to your directory path

#     # Process all files and get a list of documents
#     docs = process_directory(markdown_dir, max_words=200)

#     # For demo purposes, print out the first few documents
#     for doc in docs[:3]:
#         print("File:", doc["file"])
#         print("Heading:", doc["heading"])
#         print("Chunk Index:", doc["chunk_index"])
#         print("Content snippet:", doc["content"][:150])
#         print("-" * 40)
