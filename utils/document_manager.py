import os
import shutil
import chromadb

UPLOAD_FOLDER = "data/uploads"
CHROMA_FOLDER = "data/chroma_db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

client = chromadb.PersistentClient(
    path=CHROMA_FOLDER
)

collection = client.get_or_create_collection(
    name="documents"
)


# ---------------------------------------------------
# Return all uploaded documents
# ---------------------------------------------------
def list_documents():

    documents = []

    for filename in sorted(os.listdir(UPLOAD_FOLDER)):

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if not os.path.isfile(filepath):
            continue

        try:

            results = collection.get(
                where={
                    "source": filename
                },
                include=["metadatas"]
            )

            chunks = len(results["ids"])

        except Exception:

            chunks = 0

        documents.append(
            {
                "name": filename,
                "pages": "-",
                "chunks": chunks,
                "embeddings": chunks,
                "status": "Indexed"
            }
        )

    return documents


# ---------------------------------------------------
# Compatibility
# ---------------------------------------------------
def get_documents():
    return list_documents()


# ---------------------------------------------------
# Delete one document
# ---------------------------------------------------
def delete_document(filename):

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)

    try:

        results = collection.get(
            where={
                "source": filename
            }
        )

        ids = results.get("ids", [])

        if ids:

            collection.delete(
                ids=ids
            )

    except Exception:
        pass


# ---------------------------------------------------
# Rebuild database
# ---------------------------------------------------
def rebuild_database():

    if os.path.exists(CHROMA_FOLDER):
        shutil.rmtree(CHROMA_FOLDER)

    os.makedirs(
        CHROMA_FOLDER,
        exist_ok=True
    )