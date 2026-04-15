import time
import random
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
import ollama
from google import genai
from google.genai import types
from config import CHROMA_PATH, DEFAULT_EMBEDDING, DEFAULT_ANS_LLM, genai_client

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


def gemini_retry(model: str, prompt: str, max_retries: int=3):
    '''call Gemini API with retries'''
    for attempt in range(max_retries):
        try:
            return genai_client.models.generate_content(
                model=model, contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0, seed=123))
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait = (2 ** attempt) + random.uniform(0, 1)
            print(f"Exception from  Gemini {attempt+1}, waiting {wait:.1f}s")
            time.sleep(wait)
                

def answer(query: str, col_name: str, top_k: int=3, model=DEFAULT_ANS_LLM) -> dict:
    '''Retrieve top_k contexts, and ask LLM to generate an answer'''
    retrieved = retrieve(query, col_name, top_k)
    chunks_str = ''
    for chunk in retrieved['chunks']:
        chunks_str = chunks_str + '---\n' + chunk
    prompt=f"Concisely answer the question in Query based only on the information in Context.  If you don't know the answer, just say 'I don't know'.\nQuery: {query}\nContext: {chunks_str.lstrip()}\nAnswer: "
    if "gemini" in model:
        response = gemini_retry(model, prompt)
        ans = response.text
    else:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={'temperature': 0, 'seed': 123}
        )
        ans = response.response
    return {
        "query": query,
        "answer": ans,
        "ids": retrieved['ids'],
        "chunks": retrieved['chunks'],
        "distances": retrieved['distances']
    }

