import os
import uuid
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from utils import load_file_text
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

# Initialize embedding model using Ollama-compatible embeddings
embedding_model = OllamaEmbeddings(model="gemma:latest")
vectorstore_path = "vectorstore_index"

# Initialize offline LLM using Ollama
llm = Ollama(
    model="gemma:latest",
    temperature=0.1,
    top_p=1,
    verbose=True
)

# Chunking configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=400,
    separators=["\n\n", "\n", ".", " "]
)

def chunk_text(text):
    return text_splitter.split_text(text)

def embed_and_store(file_path, file_name):
    print(f"Loading file: {file_path}")
    raw_text = load_file_text(file_path, file_name)
    if not raw_text:
        print("No text extracted from file.")
        return

    chunks = chunk_text(raw_text)
    documents = [Document(page_content=chunk, metadata={"source": file_name, "chunk_id": str(uuid.uuid4())}) for chunk in chunks]

    db = FAISS.from_documents(documents, embedding_model)

    os.makedirs(vectorstore_path, exist_ok=True)
    db.save_local(vectorstore_path)
    print(f"Document embedded and saved to {vectorstore_path}")

def generate_lineage(question):
    print(f"Generating lineage for question: {question}")
    if not os.path.exists(vectorstore_path):
        return "No documents found. Please upload a file first."

    db = FAISS.load_local(
        vectorstore_path,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )

    # Prompt for ETL reasoning
    prompt_template = PromptTemplate.from_template("""
You are an ETL Logic Interpreter. Given a user's question and relevant parts of an ETL specification document, extract the logic used to derive the field, metric, or transformation. Be concise, technical, and infer logic if needed.

User question: {question}
Context: {context}

Answer:
""")

    retriever = db.as_retriever(search_kwargs={"k": 10})
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )

    response = qa_chain.run(question)
    return response
