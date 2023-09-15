import pytest
from src.data_sources import DataSource, BibleDataSource, QuranDataSource

def test_data_source_init():
    ds = DataSource('some_path')
    assert ds.logger is not None
    assert ds.file_path == 'some_path'
    assert ds.data is None
    assert ds.vectorstore is None
    assert ds.qa_chain is None
    assert ds.embedder is None
    assert ds.llm is not None
    assert ds.core_embedding_model is not None
    assert ds.store is not None

def test_bible_data_source_loading():
    bible_ds = BibleDataSource('sample_bible.csv')
    bible_ds.load_data()
    assert bible_ds.data is not None
    assert bible_ds.vectorstore is not None
    assert bible_ds.qa_chain is not None
    assert bible_ds.embedder is not None
    assert bible_ds.llm is not None
    assert bible_ds.core_embedding_model is not None
    assert bible_ds.store is not None
    assert bible_ds.file_path == 'sample_bible.csv'
    assert "In the beginning" in bible_ds.data[0].page_content
    assert len(bible_ds.data) == 3

def test_quran_data_source_loading():
    quran_ds = QuranDataSource('sample_quran.json')
    quran_ds.load_data()
    assert quran_ds.data is not None
    assert quran_ds.vectorstore is not None
    assert quran_ds.qa_chain is not None
    assert quran_ds.embedder is not None
    assert quran_ds.llm is not None
    assert quran_ds.core_embedding_model is not None
    assert quran_ds.store is not None
    assert quran_ds.file_path == 'sample_quran.json'
    assert "In the name of Allah" in quran_ds.data[0].page_content
    assert len(quran_ds.data) == 2

def test_get_answers_and_documents_bible():
    bible_ds = BibleDataSource('sample_bible.csv')
    bible_ds.load_data()
    query = "What is the meaning of life?"
    result = bible_ds.get_answers_and_documents(query)
    assert result is not None
    assert "query" in result
    assert "result" in result
    assert "source_documents" in result
    assert result["query"] == query
    assert result["source_documents"] is not None
    assert len(result["source_documents"]) == 3
    assert result["result"] is not None

def test_get_answers_and_documents_quran():
    quran_ds = QuranDataSource('sample_quran.json')
    quran_ds.load_data()
    query = "What is the meaning of life?"
    result = quran_ds.get_answers_and_documents(query)
    assert result is not None
    assert "query" in result
    assert "result" in result
    assert "source_documents" in result
    assert result["query"] == query
    assert result["source_documents"] is not None
    assert len(result["source_documents"]) == 2
    assert result["result"] is not None
