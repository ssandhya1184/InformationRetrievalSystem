from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq


import os

def summarize(doc):
    # 1. Load PDF
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Coming here")
    loader = PyPDFLoader(doc)
    documents = loader.load()
    print("1111111111")
    # 2. Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    docs = text_splitter.split_documents(documents)
    print("222222")
    # 3. Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en"
    )

    # 4. Create FAISS vector store
    vectorstore = FAISS.from_documents(docs, embeddings)
    print("444444")
    # 5. Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k":4})

    # 6. Load local LLM
    

    os.environ["GROQ_API_KEY"] = "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"

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key="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"
    )
    print("555555")
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
    print("88888")
    # 10. Run summarization
    summary = chain.invoke("Summarize the PDF")

    print("\nPDF SUMMARY:\n")
    
    return summary