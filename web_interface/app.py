# Simple Flask app front end

from flask import Flask, request, render_template, jsonify
from langchain_interface import LangchainInterface

app = Flask(__name__)
langchain_interface = LangchainInterface(bible_csv_path='nheb_bible.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        answer_and_documents = langchain_interface.get_answers_and_documents(query)
        return render_template('index.html', answer_and_documents=answer_and_documents)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
