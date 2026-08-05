from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama,OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

pdf_path = Path(__file__).resolve().parent.parent / "data" / "rules_of_ml.pdf"
if not pdf_path.exists():
    raise FileNotFoundError(f"Missing PDF file: {pdf_path}")

# PDF Loader
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

# split the document into chunks

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=70
    
)

chunks=text_splitter.split_documents(documents=docs)

# Embedding the chunks using Ollama embeddings

embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")

# create a qdrant vector store

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="first_collection",
    url="http://localhost:6333",
    force_recreate=True,
)

print("vector store created and documents embedded successfully")