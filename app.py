import glob
import json
from flask import Flask, send_from_directory, jsonify, request
from config import EMBED_MODELS, ANS_MODELS

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')


@app.route("/api/files")
def get_files():
    return jsonify(glob.glob('results/*.jsonl'))


@app.route("/api/results")
def get_results():
    file_path = request.args.get('file')
    if not file_path:
        return jsonify([])
    items = []
    with open(file_path, 'r') as f:
        for line in f:
            items.append(json.loads(line))
    return jsonify(items)


@app.route("/api/models")
def get_models():
    models = {
        "embed_models": EMBED_MODELS,
        "ans_models": ANS_MODELS
    }
    return jsonify(models)
