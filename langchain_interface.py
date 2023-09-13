import logging
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.llms.openai import OpenAIChat
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler

class LangchainInterface:
    def __init__(self, bible_csv_path: str = 'nheb_bible.csv'):
        # Initialize logging
        self.logger = logging.getLogger(__name__)

        # Initialize the local file store
        self.logger.info("Creating local file store")
        self.store = LocalFileStore("./cache/")

        # Initialize the embeddings
        self.logger.info("Initializing embeddings")
        self.core_embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Load the text data from a CSV file
        self.logger.info("Loading data")
        loader = CSVLoader(
            file_path=bible_csv_path,
            csv_args={
                "delimiter": ",",
            }
        )
        self.data = loader.load()

        # Create cache-backed embeddings
        self.logger.info("Creating cache-backed embeddings")
        self.embedder = CacheBackedEmbeddings.from_bytes_store(
            self.core_embedding_model,
            self.store,
            namespace=self.core_embedding_model.model_name
        )

        # Store embeddings in vector store
        self.logger.info("Storing embeddings in vector store")
        self.vectorstore = FAISS.from_documents(self.data, self.embedder)

        # Initialize the chatbot
        self.logger.info("Initializing the chatbot")
        self.llm = OpenAIChat()

        # Initialize the QA chain
        self.logger.info("Initializing the QA chain")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            callbacks=[StdOutCallbackHandler()],
            return_source_documents=True
        )

    def get_answers_and_documents(self, query):
        self.logger.info("Getting answers and documents for query")
        return self.qa_chain({"query": query})
