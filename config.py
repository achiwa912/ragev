from google import genai
CHROMA_PATH = "chroma"
RESULTS_PATH = "results"
SOURCE_DOCUMENTS = ["data/org/vbs.org", "data/org/homelab.org", "data/org/advanced.org"]
EMBED_MODELS = ["qwen3-embedding:0.6b", "all-minilm:latest", "nomic-embed-text:latest"]
ANS_MODELS = ["gemini-2.5-flash-lite", "llama3.1:8b"]
DEFAULT_EMBEDDING = EMBED_MODELS[0]
DEFAULT_ANS_LLM = ANS_MODELS[0]
DEFAULT_EVAL_LLM = ANS_MODELS[0]
DEFAULT_RERANK = "cross-encoder/ms-marco-MiniLM-L6-v2"
TOP_K_RERANK = 20
genai_client = genai.Client()
