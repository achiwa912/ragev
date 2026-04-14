import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
import ollama
from config import CHROMA_PATH, DEFAULT_EMBEDDING, DEFAULT_LLM

def retrieve(query: str, col_name: str, top_k: int=3) -> dict:
    '''Retrieve top_k contexts similar to query'''
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        col = client.get_collection(name=col_name)
    except Exception as e:
        raise(f'Does ChromaDB/{col_name} exist?: {e}')

    results = col.query(
        query_texts=query,
        n_results=top_k
    )
    return {
        "query": query,
        "ids": results['ids'][0],
        "chunks": results['documents'][0],
        "distances": results['distances'][0]
    }

def answer(query: str, col_name: str, top_k: int=3, model=DEFAULT_LLM) -> dict:
    '''Retrieve top_k contexts, and ask LLM to generate an answer'''
    retrieved = retrieve(query, col_name, top_k)
    chunks_str = ''
    for chunk in retrieved['chunks']:
        chunks_str = chunks_str + '---\n' + chunk
    prompt=f"Concisely answer the question in Query based only on the information in Context.  If you don't know the answer, just say 'I don't know'.\nQuery: {query}\nContext: {chunks_str.lstrip()}\nAnswer: "
    #print(prompt)
    ans = ollama.generate(
        model=model,
        prompt=prompt
    )
    return {
        "query": query,
        "answer": ans['response'],
        "ids": retrieved['ids'],
        "chunks": retrieved['chunks'],
        "distances": retrieved['distances']
    }

