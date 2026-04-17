from config import SOURCE_DOCUMENTS
from questions import questions_keywords

all_text = ''
for source in SOURCE_DOCUMENTS:
    with open(source, 'r') as f:
        all_text += f.read().lower()

for question in questions_keywords:
    for keyword in question['keywords']:
        if keyword.lower() not in all_text:
            print(f"{keyword} in {question['id']} not found")

