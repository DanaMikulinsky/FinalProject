"""
This class is for reading, pre-proccessing and loading the documents into the system
"""

from dbHandler import DBHandler
import os

db_handler = DBHandler()


def load_documents(collection_name):
    db = DBHandler.get_mongo_client()
    collection = db[collection_name]
    documents = list(collection.find({}))  # Retrieve all documents
    return documents


def semantic_chunking(encoder, directory_path, score_threshold):
    """
    Use the semantic chunking to split the documents into semantic chunks
    Args:
        encoder (CohereEncoder): the encoder to be used
        directory_path (str): path to the directory containing the documents
        score_threshold (float): the score threshold for the encoder below which the split is made, between 0 and 1
    Returns:
        splits (list): list of the semantic chunks
    """
    encoder.score_threshold = score_threshold
    splitter = RollingWindowSplitter(
        encoder=encoder,
        dynamic_threshold=False,
        min_split_tokens=100,
        max_split_tokens=400,
        window_size=5,
        plot_splits=True,
        enable_statistics=True
    )

    splits = []
    for file_name in os.listdir(directory_path):
        print(file_name)
        file = open(f'{directory_path}/{file_name}', "r")
        example_faq = file.read()
        file.close()
        splits += splitter([example_faq])

    return splits


def splits_to_langchain(splits):
    """
    Build a list of langchain documents from the splits
    Args:
        splits (list): list of the semantic chunks
    Returns:
        langchain_chunks (list): list of langchain documents
    """
    complete_chunks = []
    for i in range(len(splits)):
        if i == 0:
            complete_chunks.append(' '.join(splits[i].docs + splits[i+1].docs[:200]))
        elif i + 1 == len(splits):
            complete_chunks.append(' '.join(splits[i-1].docs[-200:] + splits[i].docs))
        else:
            complete_chunks.append(' '.join(splits[i-1].docs[-200:] + splits[i].docs + splits[i+1].docs[:200]))

    langchain_chunks = []
    for c in complete_chunks:
        langchain_chunks.append(Document(page_content=c, metadata={'source': 'docs/example_faq_en.txt', 'filename': 'docs/example_faq_en.txt'}))
    return langchain_chunks



