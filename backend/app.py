from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_pipeline import embed_and_store, generate_lineage
import os
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file.save(tmp.name)
            file_path = tmp.name
            file_name = file.filename
        embed_and_store(file_path, file_name)
        os.remove(file_path)
        return jsonify({"message": "File processed successfully."})
    return jsonify({"error": "No file uploaded"}), 400

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data['question']
    answer = generate_lineage(question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
