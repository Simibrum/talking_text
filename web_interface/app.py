# Simple Flask app front end

from flask import Flask, request, render_template
from src.data_sources import BibleDataSource, QuranDataSource

app = Flask(__name__)

# Load the data sources
BIBLE_DS = BibleDataSource(file_path='data/nheb_bible.csv')
BIBLE_DS.load_data()
QURAN_DS = QuranDataSource(file_path='data/flattened_quran_verses.json')
QURAN_DS.load_data()

def parse_document(page_content):
    lines = page_content.split("\n")
    parsed = {}
    for line in lines:
        key, value = line.split(": ", 1)
        parsed[key.lower()] = value
    return parsed


@app.route('/bible', methods=['GET', 'POST'])
def ask_bible():
    if request.method == 'POST':
        query = request.form['query']
        answer_and_documents = BIBLE_DS.get_answers_and_documents(query)
        # Parse each source document and convert to dictionary
        parsed_docs = []
        for doc in answer_and_documents['source_documents']:
            parsed_content = parse_document(doc.page_content)
            parsed_docs.append({
                'parsed_content': parsed_content,
                'metadata': doc.metadata
            })
        return render_template(
            'askbible.html', answer_and_documents=answer_and_documents, parsed_docs=parsed_docs)

    return render_template('askbible.html')


@app.route('/quran', methods=['GET', 'POST'])
def ask_quran():
    if request.method == 'POST':
        query = request.form['query']
        answer_and_documents = QURAN_DS.get_answers_and_documents(query)
        return render_template(
            'askquran.html', answer_and_documents=answer_and_documents)

    return render_template('askquran.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
