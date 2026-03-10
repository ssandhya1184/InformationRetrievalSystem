import streamlit as st
from src.summarize import summarize
import tempfile

def main():
    st.set_page_config("Information Retrieval")
    st.header("Information Retrieval System ℹ️")
    summary = ""

    with st.sidebar:
        st.title("Menu:")
        uploaded_file = st.file_uploader("Upload your PDF files and click on Submit & Process Button",
                                    #accept_multiple_files=True
                                    type="pdf"
                                    )
        if st.button("Submit & Process"):
                #
            if uploaded_file is not None:

                # Save uploaded PDF temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    pdf_path = tmp_file.name

                st.success("PDF uploaded successfully!")
                summary = summarize(pdf_path)
   
                print("Fetching the summary------>",summary)
                
    if summary != "":
        st.info(summary)
        
                

if __name__ == '__main__':
    main()