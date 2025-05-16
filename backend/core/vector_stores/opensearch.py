from llama_index.vector_stores.opensearch import (
    OpensearchVectorClient,
    OpensearchVectorStore,
)

from opensearch_manager.constants import (
    COHERE_EMBEDDING_MODEL_OUTPUT_DIM,
    DEFAULT_OS_INDEX_NAME,
)
from opensearch_manager.async_client import AsyncOpensearchClient
from opensearch_manager.client import OpensearchClient


def get_opensearch_vector_store() -> OpensearchVectorStore:
    opensearch_client = OpensearchClient().get_client()
    opensearch_async_client = AsyncOpensearchClient().get_client()
    opensearch_endpoint = OpensearchClient().get_endpoint()

    # storage_context = StorageContext.from_defaults(vector_store=vector_store)

    opensearch_vector_client = OpensearchVectorClient(
        os_client=opensearch_client,
        os_async_client=opensearch_async_client,
        embedding_field="embedding",
        text_field="content",
        dim=COHERE_EMBEDDING_MODEL_OUTPUT_DIM,
        index=DEFAULT_OS_INDEX_NAME,
        endpoint=opensearch_endpoint,
    )
    vector_store = OpensearchVectorStore(opensearch_vector_client)
    return vector_store
