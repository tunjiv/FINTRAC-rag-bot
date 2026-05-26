from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM as Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

CHROMA_DIR = "project1_rag_bot/chroma_db"

PROMPT_TEMPLATE = """You are a compliance officer assistant at a Canadian financial institution.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say: "This is not covered in my documents."
Always cite the specific document your answer comes from.

Context:
{context}

Question: {question}

Answer (with source citation):"""

def answer(question: str) -> dict:
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = Ollama(model="llama3", temperature=0)
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    docs = retriever.invoke(question)
    sources = list(set([
        doc.metadata.get("source", "Unknown") for doc in docs
    ]))
    result = chain.invoke(question)

    return {"answer": result, "sources": sources}

if __name__ == "__main__":
    r = answer("What is a Suspicious Transaction Report and when must it be filed?")
    print("\nAnswer:", r["answer"])
    print("\nSources:", r["sources"])