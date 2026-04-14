from datetime import datetime
import json
import chromadb
import ollama
from config import DEFAULT_LLM, RESULTS_PATH
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
    if answer.strip().lower().startswith("i don't know"):
        return 0
    prompt = FAITHFULNESS_PROMPT.format(
        answer=answer, contexts=' '.join(chunks))
    ans = ollama.generate(
        model=model,
        prompt=prompt)
    return 1 if 'YES' in ans.response else 0


CORRECTNESS_PROMPT = """Reference: {reference_answer}
Answer: {answer}

Is the answer correct given the reference?
Answer is correct if it captures the key facts, even if not exhaustive.
Reply ONLY: YES or NO"""


def correctness(answer: str, ref_ans: str, model: str) ->int:
    '''Answer Correctness.  1: Correct, 0: Wrong'''
    if answer.strip().lower().startswith("i don't know"):
        return 0
    prompt = CORRECTNESS_PROMPT.format(
        reference_answer=ref_ans,
        answer=answer)
    ans = ollama.generate(
        model=model,
        prompt=prompt)
    return 1 if 'YES' in ans.response else 0


def eval(col_name: str, top_k: int=3, model: str=DEFAULT_LLM, retrieve_only: bool=False):
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
                result = answer(question['query'], col_name, top_k=top_k, model=model)
                eval_single['faithfulness'] = faithfulness(
                    result['chunks'], result['answer'], model=model)
                ff_sum += eval_single['faithfulness']
                eval_single['correctness'] = correctness(
                    result['answer'], question['reference_answer'], model)
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

eval('all_s800_o80', 3, DEFAULT_LLM, False)


    
"""
    {
        "id": "q01",
        "query": "What does PREV stand for and what is its purpose?",
        "keywords": ["Plan", "Verify", "self-criticism"],
        "reference_answer": "PREV stands for Plan, Reason, Execute and Verify. Its purpose is to address the LLM weakness of jumping into conclusions too early by forcing the LLM to slow down and verify its output."
    },
===
{'query': 'What is CoT?', 'ids': ['advanced.org_014', 'vbs.org_006', 'advanced.org_003'], 'chunks': ["ons.  It generates sub-questions and answer them sequentially.  This pattern is to address LLM's weakness that it tends to jump to conclusion without breaking down.  It's a more structured version of CoT (Chain of Thoughts) pattern.\n\nSample template:\n#+begin_src \nTask: [TASK]\n\nGenerate sub-questions you need to answer to solve this task.\nQ1: [sub-question]\nA1: [answer]\nQ2: [sub-question]\nA2: [answ", 'morized word with a new word.  This way, the learning window has 10 words that you are actively working on.  It shifts through a word book and eventually reaches the end of the book.  Then, the next cycle starts.  This process contines until you memorize everything in the book.\n\nAs you can see, a word book represents the unit of low-frequency repepitions.\n\n* Quick Start\n** Register and login\n- You', "relates to other topics that I learned, etc\n7. If I'm more or less satisfied, move on to the next day\n\nAt first, Copilot was my main tutor because it doesn't have a visible usage cap.  When I don't understand or am not satisfied with its explanations, I turn to (sometimes all of) ChatGPT, Gemini and/or Claude for better explanations.  I found that this is a good approach to avoid their usage caps."], 'distances': [0.714142918586731, 0.7666090726852417, 0.7858465909957886]}
"""

