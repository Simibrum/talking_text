import logging
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import JSONLoader
from langchain.embeddings import HuggingFaceEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.llms.openai import OpenAIChat
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler

from config import logger

class DataSource:
    def __init__(self, file_path: str):
        self.logger = logger
        self.logger.info("Initializing data source")
        
        self.file_path = file_path
        self.data = None

        # Initialize common functionalities
        self.store = LocalFileStore("../cache/")
        self.core_embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = OpenAIChat()

        # Initialize these after data is loaded
        self.embedder = None
        self.vectorstore = None
        self.qa_chain = None

    def load_data(self):
        raise NotImplementedError("This method should be overridden by subclass")

    def post_data_load_setup(self):
        self.logger.info("Creating cache backed embeddings")
        self.embedder = CacheBackedEmbeddings.from_bytes_store(
            self.core_embedding_model,
            self.store,
            namespace=self.core_embedding_model.model_name
        )
        self.logger.info("Storing embeddings in vector store")
        self.vectorstore = FAISS.from_documents(self.data, self.embedder)
        self.logger.info("Initializing the QA chain")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            callbacks=[StdOutCallbackHandler()],
            return_source_documents=True
        )

    def get_answers_and_documents(self, query):
        self.logger.info("Getting answers and documents")
        return self.qa_chain({"query": query})


class BibleDataSource(DataSource):
    def load_data(self):
        self.logger.info("Loading Bible CSV data")
        loader = CSVLoader(
            file_path=self.file_path,
            csv_args={"delimiter": ","}
        )
        self.data = loader.load()
        self.post_data_load_setup()

def populate_metadata(record: dict, metadata: dict) -> dict:
    """
    Populates metadata using fields from the given record.

    Parameters:
        record (dict): The record dictionary containing chapter and verse information.
        metadata (dict): The metadata dictionary to populate.

    Returns:
        dict: The populated metadata dictionary.
    """
    for key, value in record.items():
        if key != "english_translation":  # Skip the "english_translation" field
            metadata[key] = value

    return metadata

class QuranDataSource(DataSource):
    def load_data(self):
        self.logger.info("Loading Quran JSON data")
        loader = JSONLoader(
            file_path=self.file_path,
            jq_schema='.[]',
            content_key="english_translation",
            metadata_func=populate_metadata
        )
        self.data = loader.load()
        self.post_data_load_setup()
