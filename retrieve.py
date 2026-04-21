import time
import random
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
import ollama
from sentence_transformers import CrossEncoder
from google import genai
from google.genai import types
from config import CHROMA_PATH, DEFAULT_EMBEDDING, DEFAULT_ANS_LLM, TOP_K_RERANK, genai_client

QTRANS_PROMPT = """You are a vector DB expert.  Tranform the user query to a more vector-DB-friendly transformed query, removing conversational noise and possibly adding 1-3 keyeords.  Return only the transformed query string you generated.

User query: {query}
Transformed query: """

def retrieve(query: str, col_name: str, top_k: int, model_ans: str, model_embed: str, model_reranker: CrossEncoder, qtrans: bool, rerank: bool) -> dict:
    '''Retrieve top_k contexts similar to query'''
    try:
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        col = client.get_collection(name=col_name)
    except Exception as e:
        print(f'Does ChromaDB collection: {col_name} exist?: {e}')
        raise e
    
    if qtrans:
        prompt = QTRANS_PROMPT.format(query=query)
        if "gemini" in model_ans:
            response = gemini_retry(model_ans, prompt)
            text = response.text
        else:
            response = ollama.generate(
                model=model_ans,
                prompt=prompt,
                options={'temperature': 0, 'seed': 123}
            )
            text = response.response
        print(f'Trans: {text}')  # debug
    else:
        text = query

    text = "search_query: " + text if 'nomic' in model_embed else text
    if rerank:
        results = col.query(
            query_texts=[text],
            n_results=TOP_K_RERANK
        )
        ranks = model_reranker.rank(
            query, results['documents'][0], top_k=top_k, return_documents=True)
        return {
            "query": query,
            "chunks": [rank['text'] for rank in ranks],
            # json.dumps can't serialize np.float32 -> cast with float()
            "distances": [float(rank['score']) for rank in ranks]
        }
    else:
        results = col.query(
            query_texts=[text],
            n_results=top_k
        )
        return {
            "query": query,
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
                

def answer(query: str, col_name: str, top_k: int=3, model_ans: str=DEFAULT_ANS_LLM, model_embed: str=DEFAULT_EMBEDDING, model_reranker: CrossEncoder=None, qtrans: bool=False, rerank: bool=False) -> dict:
    '''Retrieve top_k contexts, and ask LLM to generate an answer'''
    retrieved = retrieve(query, col_name, top_k, model_ans, model_embed, model_reranker, qtrans, rerank)
    chunks_str = ''
    for chunk in retrieved['chunks']:
        chunks_str = chunks_str + '---\n' + chunk
    prompt=f"Concisely answer the question in Query based only on the information in Context.  If you don't know the answer, just say 'I don't know'.\nQuery: {query}\nContext: {chunks_str.lstrip()}\nAnswer: "
    if "gemini" in model_ans:
        response = gemini_retry(model_ans, prompt)
        ans = response.text
    else:
        response = ollama.generate(
            model=model_ans,
            prompt=prompt,
            options={'temperature': 0, 'seed': 123}
        )
        ans = response.response
    return {
        "query": query,
        "answer": ans,
        "chunks": retrieved['chunks'],
        "distances": retrieved['distances']
    }

