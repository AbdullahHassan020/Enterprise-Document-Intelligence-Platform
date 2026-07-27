import chromadb

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def store_embeddings(
    filename,
    chunks,
    embeddings
):

    ids = []
    documents = []
    vectors = []
    metadatas = []

    for i, text in enumerate(chunks):

        ids.append(f"{filename}_{i}")

        documents.append(text)

        vectors.append(
            embeddings[i].tolist()
        )

        metadatas.append(
            {
                "source": filename,
                "chunk": i
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=vectors,
        metadatas=metadatas
    )


def total_documents():

    return collection.count()