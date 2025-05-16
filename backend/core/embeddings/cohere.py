from llama_index.embeddings.bedrock import BedrockEmbedding

from agentacademy.settings import (
    BEDROCK_ACCESS_KEY_ID,
    BEDROCK_REGION,
    BEDROCK_SECRET_ACCESS_KEY,
)
from sentence_transformers import SentenceTransformer


COHERE_EMBEDDING_MODEL_ID = "cohere.embed-multilingual-v3"
EMBEDDING_MODEL = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"

# def get_cohere_embedding_model() -> BedrockEmbedding:
#     return BedrockEmbedding(
#         aws_access_key_id=BEDROCK_ACCESS_KEY_ID,
#         aws_secret_access_key=BEDROCK_SECRET_ACCESS_KEY,
#         region_name=BEDROCK_REGION,
#         model_name=COHERE_EMBEDDING_MODEL_ID,
#     )

def get_cohere_embedding_model():
    SentenceTransformer(EMBEDDING_MODEL)