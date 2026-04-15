from google import genai
CHROMA_PATH = "chroma"
RESULTS_PATH = "results"
SOURCE_DOCUMENTS = ["data/org/vbs.org", "data/org/homelab.org", "data/org/advanced.org"]
DEFAULT_EMBEDDING = "all-minilm:latest"
DEFAULT_LLM = "llama3.1:8b"
DEFAULT_ANS_LLM = "gemini-2.5-flash-lite"
#DEFAULT_ANS_LLM = "llama3.1:8b"  # "gemini-2.5-flash-lite"
DEFAULT_EVAL_LLM = "gemini-2.5-flash-lite"
#DEFAULT_EVAL_LLM = "llama3.1:8b"  # "gemini-2.5-flash-lite"
genai_client = genai.Client()
