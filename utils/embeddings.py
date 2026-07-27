from sentence_transformers import SentenceTransformer

# Load embedding model once
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def generate_embeddings(chunks):
    """
    Generates embeddings from either

    List[str]

    OR

    List[dict]
    """

    texts = []

    for chunk in chunks:

        if isinstance(chunk, dict):

            texts.append(
                chunk["text"]
            )

        else:

            texts.append(chunk)

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=False,
        convert_to_numpy=True
    )

    return embeddings