from llama_index.core import VectorStoreIndex

from core.embeddings.cohere import get_cohere_embedding_model
from core.vector_stores.opensearch import get_opensearch_vector_store


def get_opensearch_vector_store_index() -> VectorStoreIndex:
    """
    Create and return an instance of VectorStoreIndex using the
    - Opensearch vector store
    - Cohere embedding model
    - Default storage context
    """
    vector_store = get_opensearch_vector_store()
    embed_model = get_cohere_embedding_model()
    vectore_store_index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)

    return vectore_store_index
