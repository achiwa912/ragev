import json
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/api/results")
def get_results():
    with open('results/eval_20260424_081257.jsonl', 'r') as f:
        items = []
        for line in f:
            items.append(json.loads(line))
    return items
