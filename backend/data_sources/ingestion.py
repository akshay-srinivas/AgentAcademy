from llama_index.core.node_parser import SemanticSplitterNodeParser
from core.vector_stores.opensearch import get_opensearch_vector_store
from core.embeddings.cohere import get_cohere_embedding_model
from llama_index.core.ingestion import (
    DocstoreStrategy,
    IngestionPipeline,
)

from core.readers.happyfox_helpdesk import HappyFoxHelpdeskKBReader
from accounts.models import Account


def run_ingestion_pipeline(account: Account) -> None:
    """
    Run the ingestion pipeline for the HappyFox Helpdesk knowledge base.
    """
    # Create the vector store and embedding model

    embed_model = get_cohere_embedding_model()
    vector_store = get_opensearch_vector_store()

    transformations = []
    transformations.extend(
        [
            SemanticSplitterNodeParser(embed_model=embed_model),
            embed_model,
        ]
    )
    print("Transformations: ", transformations)
    hd_reader = HappyFoxHelpdeskKBReader(account=account)
    documents = hd_reader.load_data()


    pipeline = IngestionPipeline(
        transformations=transformations,
        vector_store=vector_store,
    )
    # Run the ingestion pipeline
    nodes = pipeline.run(show_progress=True, documents=documents)

    return nodes