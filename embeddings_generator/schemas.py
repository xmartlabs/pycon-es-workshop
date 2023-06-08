from pydantic import BaseModel, Field
from typing import List

from embedding_generator import EmbeddingTypes


class EmbeddingsRequest(BaseModel):
    text: str
    type: EmbeddingTypes = Field(default=EmbeddingTypes.SYMMETRIC)


class EmbeddingsResponse(BaseModel):
    embedding: List[float]
