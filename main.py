import logging

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

from langchain.llms.openai import OpenAIChat
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler

# Create a logger
logger = logging.getLogger(__name__)

# Create a local file store to cache the embeddings
logger.info("Creating local file store")
store = LocalFileStore("./cache/")

# Initialize the embeddings
logger.info("Initializing embeddings")
core_embedding_model = OpenAIEmbeddings()

# Load the text data from a CSV file
logger.info("Loading data")
loader = CSVLoader(
    file_path="nheb_bible.csv",
    csv_args={
        "delimiter": ",",
    }
)

data = loader.load()

# Create a cache backed embeddings
logger.info("Creating cache backed embeddings")
embedder = CacheBackedEmbeddings.from_bytes_store(
    core_embedding_model,
    store,
    namespace=core_embedding_model.model_name
)

# Store embeddings in vector store
logger.info("Storing embeddings in vector store")
vectorstore = FAISS.from_documents(data, embedder)

# Instantiate a retriever
logger.info("Instantiating a retriever")
retriever = vectorstore.as_retriever()

# Initialize the chatbot
logger.info("Initializing the chatbot")
llm = OpenAIChat()
logger.info("Initialising the output handler")
handler = StdOutCallbackHandler()

# Initialize the QA chain
logger.info("Initializing the QA chain")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    callbacks=[handler],
    return_source_documents=True
)

# Get a question from the user
logger.info("Getting a question from the user")
question = "What is the meaning of life?"
# Ask the question
response = qa_chain({"query":question})

print(response)