# Simple Flask app front end

from flask import Flask, request, render_template, jsonify
from langchain_interface import LangchainInterface

app = Flask(__name__)
langchain_interface = LangchainInterface(bible_csv_path='nheb_bible.csv')

def parse_document(page_content):
    lines = page_content.split("\n")
    parsed = {}
    for line in lines:
        key, value = line.split(": ", 1)
        parsed[key.lower()] = value
    return parsed


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        answer_and_documents = langchain_interface.get_answers_and_documents(query)
        # Parse each source document and convert to dictionary
        parsed_docs = []
        for doc in answer_and_documents['source_documents']:
            parsed_content = parse_document(doc.page_content)
            parsed_docs.append({
                'parsed_content': parsed_content,
                'metadata': doc.metadata
            })
        return render_template(
            'index.html', answer_and_documents=answer_and_documents, parsed_docs=parsed_docs)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
