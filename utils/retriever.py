import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def retrieve_chunks(query, top_k=10):

    query_embedding = embedding_model.encode(
        query,
        convert_to_numpy=True
    )

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k
    )

    retrieved = []

    if len(results["documents"]) == 0:
        return retrieved

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for doc, meta in zip(docs, metas):

        retrieved.append(
            {
                "text": doc,
                "source": meta["source"],
                "chunk": meta["chunk"]
            }
        )

    return retrieved