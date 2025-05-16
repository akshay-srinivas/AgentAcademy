from typing import List

from llama_index.core.indices.base import BaseIndex
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import NodeWithScore


def retrieve_search_results(retriever: BaseRetriever, user_query: str) -> List[NodeWithScore]:
    """
    Search the given retriever for the user's query
    """
    response = retriever.retrieve(user_query)
    return response


async def retrieve_search_results_async(
    index: BaseIndex, retriever: BaseRetriever, user_query: str, close_connection: bool = True
) -> List[NodeWithScore]:
    """
    Search the given retriever for the user's query
    """
    response = await retriever.aretrieve(user_query)

    if close_connection:
        await index.vector_store.client._os_async_client.close()

    return response
