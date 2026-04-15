from datetime import datetime
import json
import chromadb
import ollama
from google import genai
from google.genai import types
from config import DEFAULT_EVAL_LLM, DEFAULT_ANS_LLM, RESULTS_PATH
from questions import questions_keywords
from retrieve import answer, retrieve

def recallk(qidx: int, chunks: list[str]) ->float:
    '''Recall@K.  Approximation using keywords'''
    keywords = questions_keywords[qidx]['keywords']
    score = 0
    for keyword in keywords:
        for chunk in chunks:
            if keyword.lower() in chunk.lower():
                score += 1
                break
    return score/len(keywords)


def reciprocal_rank(qidx: int, chunks: list[str]) ->float:
    '''Reciprocal Rank for a single query'''
    keywords = questions_keywords[qidx]['keywords']
    for i, chunk in enumerate(chunks, start=1):
        for keyword in keywords:
            if keyword.lower() in chunk.lower():
                return 1/i
    return 0.0
    

FAITHFULNESS_PROMPT = """Answer: {answer}
Context: {contexts}

Is the answer fully supported by the context?
Reply ONLY: YES or NO"""

def faithfulness(chunks: list[str], answer: str, model: str) ->int:
    '''Answer Faithfulness.  1: faithfull, 0: not'''
    if "i don't know" in answer.lower():
        return 0
    prompt = FAITHFULNESS_PROMPT.format(
        answer=answer, contexts=' '.join(chunks))
    if "gemini" in model:
        genai_client = genai.Client()
        response = genai_client.models.generate_content(
            model=model, contents=prompt,
            config=types.GenerateContentConfig(temperature=0))
        ans = response.text
    else:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={'temperature': 0, 'seed': 42}
        )
        ans = response.response
    return 1 if 'YES' in ans else 0


CORRECTNESS_PROMPT = """Reference: {reference_answer}
Answer: {answer}

Is the answer correct given the reference?
Reply ONLY: YES or NO"""

# Answer is correct if it captures the key facts, even if not exhaustive.


def correctness(answer: str, ref_ans: str, model: str) ->int:
    '''Answer Correctness.  1: Correct, 0: Wrong'''
    if "i don't know" in answer.lower():
        return 0
    prompt = CORRECTNESS_PROMPT.format(
        reference_answer=ref_ans,
        answer=answer)
    if "gemini" in model:
        genai_client = genai.Client()
        response = genai_client.models.generate_content(
            model=model, contents=prompt,
            config=types.GenerateContentConfig(temperature=0))
        ans = response.text
    else:
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={'temperature': 0, 'seed': 42}
        )
        ans = response.response
    return 1 if 'YES' in ans else 0


def eval(col_name: str, top_k: int=3, model_ans: str=DEFAULT_ANS_LLM, model_eval: str=DEFAULT_EVAL_LLM, retrieve_only: bool=False):
    eval_result = []
    recallk_sum = rr_sum = ff_sum = correct_sum = 0.0
    filename = f'{RESULTS_PATH}/eval_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jsonl'
    with open(filename, 'w', encoding='utf-8') as f:
        for i, question in enumerate(questions_keywords):
            eval_single = {}
            eval_single['qid'] = question['id']
            eval_single['faithfulness'] = eval_single['correctness'] = 0
            if retrieve_only:
                result = retrieve(question['query'], col_name, top_k=top_k)
                result['answer'] = 'N/A'
            else:
                result = answer(question['query'], col_name, top_k=top_k, model=model_ans)
                eval_single['faithfulness'] = faithfulness(
                    result['chunks'], result['answer'], model=model_eval)
                ff_sum += eval_single['faithfulness']
                eval_single['correctness'] = correctness(
                    result['answer'], question['reference_answer'], model=model_eval)
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

eval('all_s800_o80', 3, model_ans=DEFAULT_ANS_LLM, model_eval=DEFAULT_EVAL_LLM, retrieve_only=False)

