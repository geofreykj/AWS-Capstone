import streamlit as st
from services.s3_service import upload_file
from services.ingestion_service import get_file_bytes, extract_text
from utils.chunker import chunk_text
from services.bedrock_service import get_embedding, generate_answer
from services.chroma_service import save_chunks, search_documents, document_hash_exists, collection_has_documents, get_available_documents
from dotenv import load_dotenv
import os
import hashlib

st.set_page_config(
    page_title="AWS RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AWS RAG Assistant")
st.caption("Upload a PDF or Markdown file and ask questions about it")

BUCKET_NAME = os.getenv("BUCKET_NAME")

# Session state
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------
# Sidebar
# ------------------------

with st.sidebar:

    st.header("📄 Options")

    has_data = collection_has_documents()

    if has_data:
        st.info("✅ Documents found in database")
        available_docs = get_available_documents()
        st.write("Available documents:")
        for doc in available_docs:
            st.caption(f"📄 {doc}")

        if st.button("Query Existing Data"):
            st.session_state.file_processed = True

    st.divider()
    st.subheader("Upload New Document")

    uploaded_file = st.file_uploader(
        "Upload PDF or Markdown",
        type=["pdf", "md"]
    )

    if uploaded_file:

        if st.button("Process Document"):

            with st.spinner("Uploading and processing..."):

                # Step 1: Compute hash from uploaded file FIRST
                file_bytes = uploaded_file.read()
                file_hash = hashlib.md5(file_bytes).hexdigest()

                # Step 2: Check if document already exists in database
                if document_hash_exists(file_hash):
                    st.warning("This document has already been ingested.")
                    st.session_state.file_processed = True

                else:
                    # Step 3: Only upload to S3 if it's new
                    key = upload_file(uploaded_file)

                    # Step 4: Extract text and create chunks
                    text = extract_text(uploaded_file.name, file_bytes)
                    chunks = chunk_text(text)

                    # Step 5: Generate embeddings and save
                    embeddings = [

                        get_embedding(chunk)
                        for chunk in chunks
                    ]

                    save_chunks(
                        chunks,
                        embeddings,
                        uploaded_file.name,
                        file_hash
                    )

                    st.session_state.file_processed = True
                    st.success(f"Processed {len(chunks)} chunks")

                st.session_state.file_processed = True

                st.success(
                    f"Processed {len(chunks)} chunks"
                )
# ------------------------
# Main Chat Area
# ------------------------

if not st.session_state.file_processed:

    st.info(
        "Upload a document from the sidebar to begin."
    )

else:

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask a question about your document..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                query_embedding = get_embedding(
                    question
                )

                results = search_documents(
                    query_embedding,
                    n_results=5
                )

                context = "\n\n".join(
                    results["documents"][0]
                )

                answer = generate_answer(
                    question,
                    context
                )

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )