from datetime import datetime
import re
import json
import chromadb
import ollama
from google import genai
from google.genai import types
from config import DEFAULT_EVAL_LLM, DEFAULT_ANS_LLM, RESULTS_PATH, genai_client
from questions import questions_keywords
from retrieve import answer, retrieve, gemini_retry
def recallk(qidx: int, chunks: list[str]) ->float:
    '''Recall@K.  Approximation using keywords'''
    keywords = questions_keywords[qidx]['keywords']
    score = 0
    trans = str.maketrans('-_', '  ')
    for keyword in keywords:
        keyword = keyword.lower().translate(trans)
        for chunk in chunks:
            if keyword in chunk.lower().translate(trans):
                score += 1
                break
    return score/len(keywords)


def reciprocal_rank(qidx: int, chunks: list[str]) ->float:
    '''Reciprocal Rank for a single query'''
    keywords = questions_keywords[qidx]['keywords']
    trans = str.maketrans('-_', '  ')
    for i, chunk in enumerate(chunks, start=1):
        chunk = chunk.lower().translate(trans)
        for keyword in keywords:
            if keyword.lower().translate(trans) in chunk:
                return 1/i
    return 0.0

FAITHFULNESS_PROMPT = """You are an expert evaluator for RAG systems.

Context: {contexts}
Generated Answer: {answer}
Task: Evaluate the faithfulness of the Generated Answer to the Context.

Evaluation steps:
1. Extract all factual claims from the Generated Answer.
2. Verify each claim against the Context. Is it directly supported, contradicted, or unsupported?
3. Consider severity: Minor omissions are okay, but inventions or contradictions are bad.

Scoring rules:
- 1.0: All claims supported
- 0.8–0.9: One vague claim
- 0.6-0.7: Two or more vague claims
- 0.4-0.5: One clearly unsupported claim
- 0.2-0.3: Two or more clearly unsupported claims
- 0.0–0.1: Major hallucinations or contradictions

If a claim cannot be directly traced to the context, it must be flagged as clearly unsupported — even if it sounds plausible.

Provide a score (0.0 to 1.0) and the reasoning.
Return ONLY in this format:
Score: <float between 0.0 and 1.0>
Reasoning: <brief explanation>
"""

def faithfulness(chunks: list[str], answer: str, model: str) ->float:
    '''Answer Faithfulness.  1: faithfull, 0: not'''
    # if "i don't know" in answer.lower():
    #     return 0.0
    prompt = FAITHFULNESS_PROMPT.format(
        answer=answer, contexts = "\n\n---\n\n".join(chunks))
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
    match = re.search(r'\b([01](?:\.\d+)?)\b', ans)
    if match:
        return float(match.group(0))
    return 0.0
        
CORRECTNESS_PROMPT = """
You are an expert fact-checker.

Question: {query}
Expected Answer: {reference_answer}
Generated Answer: {answer}

Task: Rate the correctness of the Generated Answer against the Expected Answer.

Steps:
1. Identify all key facts in the Expected Answer.
2. Check if the Generated Answer includes them accurately.
3. Flag any contradictions or fabricated details.
4. Note omissions of critical information.

Scoring rules:
- 1.0: Fully answers the question; all claims correct
- 0.6–0.9: Answers the question; minor omissions or imprecision
- 0.3–0.5: Partially answers; missing 'key' aspects of the question
- 0.0–0.2: Wrong, contradictory, or does not address the question

Return ONLY in this format:
Score: <float between 0.0 and 1.0>
Reasoning: <brief explanation>
"""


def correctness(query: str, answer: str, ref_ans: str, model: str) ->float:
    '''Answer Correctness.  0(wrong) - 1.0(correct)'''
    if "i don't know" in answer.lower():
        return 0.0
    prompt = CORRECTNESS_PROMPT.format(
        query=query,
        reference_answer=ref_ans,
        answer=answer)
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
    match = re.search(r'\b([01](?:\.\d+)?)\b', ans)
    if match:
        return float(match.group(0))
    return 0.0


def eval(col_name: str='all_s600_o60', top_k: int=6, model_ans: str=DEFAULT_ANS_LLM, model_eval: str=DEFAULT_EVAL_LLM, retrieve_only: bool=False):
    eval_result = []
    recallk_sum = rr_sum = ff_sum = correct_sum = 0.0
    filename = f'{RESULTS_PATH}/eval_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonl'
    print('===', col_name, top_k, model_ans, model_eval, retrieve_only)
    with open(filename, 'w', encoding='utf-8') as f:
        for i, question in enumerate(questions_keywords):
            eval_single = {}
            eval_single['qid'] = question['id']
            eval_single['faithfulness'] = eval_single['correctness'] = 0.0
            if retrieve_only:
                result = retrieve(question['query'], col_name, top_k=top_k)
                result['answer'] = 'N/A'
            else:
                result = answer(question['query'], col_name, top_k=top_k, model=model_ans)
                eval_single['faithfulness'] = faithfulness(
                    result['chunks'], result['answer'], model=model_eval)
                ff_sum += eval_single['faithfulness']
                eval_single['correctness'] = correctness(
                    question['query'], result['answer'],
                    question['reference_answer'], model=model_eval)
                correct_sum += eval_single['correctness']
            eval_single['recallk'] = recallk(i, result['chunks'])
            recallk_sum += eval_single['recallk']
            eval_single['rr'] = reciprocal_rank(i, result['chunks'])
            rr_sum += eval_single['rr']
            print(f"{eval_single['qid']}: recall@k: {eval_single['recallk']:.2f}, RR: {eval_single['rr']:.2f} Faithfulness: {eval_single['faithfulness']} Correctness: {eval_single['correctness']}")
            record = {
                'qid': eval_single['qid'],
                'recallk': eval_single['recallk'],
                'rr': eval_single['rr'],
                'faithfulness': eval_single['faithfulness'],
                'correctness': eval_single['correctness'],
                'query': question['query'],
                'keywords': question['keywords'],
                'answer': result['answer'],
                'reference_answer': question['reference_answer'],
                'chunks': result['chunks']
            }
            f.write(json.dumps(record) + "\n")
            f.flush()
        print(f"Mean: recall@k: {(recallk_sum/len(questions_keywords)):.2f}, MRR: {(rr_sum/len(questions_keywords)):.2f}, Faithfulness: {ff_sum/len(questions_keywords):.2f} Correctness: {correct_sum/len(questions_keywords):.2f}")

# eval('all_s100_o10', 3, model_ans="gemini-2.5-flash-lite", model_eval="gemini-2.5-flash-lite", retrieve_only=False)
eval()
