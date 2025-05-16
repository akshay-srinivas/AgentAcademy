DEFAULT_OS_INDEX_NAME = "kb_index"
DEFAULT_OS_INDEX_ALIAS_NAME = "kb_index_alias"
COHERE_EMBEDDING_MODEL_OUTPUT_DIM = 1024

DEFAULT_BULK_OPS_SETTINGS = {
    # No of times to retry after initial failure
    "max_retries": 3,
    # No of secs to wait before initial retry. Used for calculating wait times for subsequest requests as well.
    "initial_backoff": 10,
    # Max time out.
    "max_backoff": 30,
    # number of docs in one chunk sent to es
    "chunk_size": 20,
    # max size of one chunk sent to es
    "max_chunk_bytes": 10 * 1024 * 1024,
}
