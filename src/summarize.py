from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

import os

def summarize(doc):

    load_dotenv() 
    api_key = os.getenv("GROQ_API_KEY")
    # 1. Load PDF    
    loader = PyPDFLoader(doc)
    documents = loader.load()
    
    # 2. Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    docs = text_splitter.split_documents(documents)
    
    # 3. Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en"
    )

    # 4. Create FAISS vector store
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # 5. Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k":4})

    # 6. Load local LLM   

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=api_key
    )
    
    # 7. Prompt template
    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant.

    Use the context below to generate a clear summary.

    Context:
    {context}

    Provide a concise summary of the document.
    """)

    # 8. Format retrieved documents
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # 9. LCEL pipeline
    chain = (
        {"context": retriever | format_docs}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # 10. Run summarization
    summary = chain.invoke("Summarize the PDF")

    print("\nPDF SUMMARY:\n")
    
    return summary