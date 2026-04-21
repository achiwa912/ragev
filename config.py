from google import genai
CHROMA_PATH = "chroma"
RESULTS_PATH = "results"
SOURCE_DOCUMENTS = ["data/org/vbs.org", "data/org/homelab.org", "data/org/advanced.org"]
DEFAULT_EMBEDDING = "nomic-embed-text:latest"  # "all-minilm:latest"
DEFAULT_LLM = "llama3.1:8b"
DEFAULT_ANS_LLM = "gemini-2.5-flash-lite"  # "llama3.1:8b"
DEFAULT_EVAL_LLM = "gemini-2.5-flash-lite"  # "llama3.1:8b"
DEFAULT_RERANK = "cross-encoder/ms-marco-MiniLM-L6-v2"
TOP_K_RERANK = 20
genai_client = genai.Client()
