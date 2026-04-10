import os
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
from config import SOURCE_DOCUMENTS, DEFAULT_EMBEDDING, CHROMA_PATH

def split_file_by_size(path_str: str, size: int, overlap: int) -> list[str]:
    '''split a text file into fixed-size chunks with overlap'''
    if overlap >= size:
        raise Exception(f"overlap:{overlap} >= size:{size}")
    chunks = []
    idx = 0
    with open(path_str, 'r') as f:  # safe for unicodes
        text = f.read()
        while True:
            chunks.append(text[idx:idx+size])
            if idx+size >= len(text):
                break
            idx += size - overlap
        return chunks
    

def ingest_file(collection: Collection, path_str: str, chunks: list[str]):
    '''embed/add chunks into collection'''
    ids = []
    metadatas = []
    for i in range(len(chunks)):
        ids.append(f'{os.path.basename(path_str)}_{i:03d}')
        metadatas.append({"document": os.path.basename(path_str)})

    batch_size = 50
    start = 0
    end = 0
    failures = 0
    print(f'Embedding {path_str}')
    while end < len(chunks):
        end = len(chunks) if start+batch_size>len(chunks) else start+batch_size
        try:
            collection.add(ids=ids[start:end], documents=chunks[start:end],
                           metadatas=metadatas[start:end])
        except:
            print(f'Batch failed, falling back on chunk-by-chunk: {start}-{end}')
            middle = start
            while middle < end:
                try:
                    collection.add(ids=ids[middle:middle+1],
                                   documents=chunks[middle:middle+1],
                                   metadatas=metadatas[middle:middle+1])
                except Exception as e:
                    print(f'Skipping {ids[middle]} - {chunks[middle]}')
                    failures += 1
                    if failures > 50:
                        print(f'Too many embedding errors.  Aborting for {path_str}.')
                        return
                middle += 1
        start = end


def ingest(size: int, overlap: int, embed_str: str=DEFAULT_EMBEDDING):
    '''
    re-create a collection and embed files
    collection naming: <embed_str>_s<size>_o<overlap>
    '''
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
    except e:
        print(f'Initializing ChromaDB failed: {e}')

    coll_str = f'{embed_str[:3]}_s{size}_o{overlap}'

    # for idempotency
    try:
        client.delete_collection(name=coll_str)
        print(f'Deleted collection: {coll_str}')
    except:
        pass

    collection = client.create_collection(
        name=coll_str,
        embedding_function=OllamaEmbeddingFunction(
            url="http://localhost:11434",
            model_name=embed_str,
        ),
        configuration={
            "hnsw": {
                # use cosine similarity (default was squared L2)
                "space": "cosine"  
            }
        }
    )

    for path_str in SOURCE_DOCUMENTS:
        chunks = split_file_by_size(path_str, size, overlap)
        ingest_file(collection, path_str, chunks)


def main():
    breakpoint()
    # ingest(400, 40)
        
if __name__ == "__main__":
    main()

