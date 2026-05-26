from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DOCS_DIR   = "project1_rag_bot/docs"
CHROMA_DIR = "project1_rag_bot/chroma_db"

def ingest_documents():
    print("Loading PDFs...")
    loader = PyPDFDirectoryLoader(DOCS_DIR)
    documents = loader.load()
    print(f"  Loaded {len(documents)} pages")

    print("Chunking...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)
    print(f"  Created {len(chunks)} chunks")

    print("Embedding and storing (runs locally)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print(f"  Done. {vectorstore._collection.count()} chunks stored.")

if __name__ == "__main__":
    ingest_documents()