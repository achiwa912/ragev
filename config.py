from google import genai
CHROMA_PATH = "chroma"
RESULTS_PATH = "results"
SOURCE_DOCUMENTS = ["data/org/vbs.org", "data/org/homelab.org", "data/org/advanced.org"]
DEFAULT_EMBEDDING = "nomic-embed-text:latest"  # "all-minilm:latest"
DEFAULT_LLM = "llama3.1:8b"
DEFAULT_ANS_LLM = "gemini-2.5-flash-lite"  # "llama3.1:8b"
DEFAULT_EVAL_LLM = "gemini-2.5-flash-lite"  # "llama3.1:8b"
genai_client = genai.Client()
