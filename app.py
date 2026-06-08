import streamlit as st
from services.s3_service import upload_file
from services.ingestion_service import get_file_bytes, extract_text
from utils.chunker import chunk_text

st.title("AWS RAG Assistant")

BUCKET_NAME = "rag-capstone-jeff"

uploaded_file = st.file_uploader(
    "Upload PDF or Markdown",
    type=["pdf", "md"]
)

if uploaded_file:
    if st.button("Upload"):

        key = upload_file(uploaded_file)    

        st.success("File uploaded successfully")

        file_bytes = get_file_bytes(
            BUCKET_NAME,
            key
        )

        text = extract_text(
            uploaded_file.name,
            file_bytes
        )

        st.text_area(
            "Extracted Text",
            text,
            height=300
        )

        chunks = chunk_text(text)

        st.write(f"Number of chunks: {len(chunks)}")