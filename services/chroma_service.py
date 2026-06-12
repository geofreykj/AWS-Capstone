import chromadb

client = chromadb.PersistentClient(
    path="./data/chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)

def document_hash_exists(file_hash):

    results = collection.get(
        where={
            "file_hash": file_hash
        }
    )

    return len(results["ids"]) > 0

def save_chunks(chunks, embeddings, filename, file_hash):

    ids = []

    metadatas = []

    for i in range(len(chunks)):
        ids.append(f"{filename}_{i}")

        metadatas.append({
            "source": filename,
            "chunk": i,
            "file_hash": file_hash
        })

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )

def search_documents(query_embedding, n_results=5):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results

def document_exists(filename):
    results = collection.get(
        where={"source": filename}
    )

    return len(results["ids"]) > 0

def collection_has_documents():
    """Check if any documents exist in the collection"""
    results = collection.get(limit=1)
    return len(results["ids"]) > 0

def get_available_documents():
    """Get list of unique documents in collection"""
    results = collection.get()
    if results["ids"]:
        sources = set(
            meta["source"] for meta in results["metadatas"]
        )
        return list(sources)
    return []
