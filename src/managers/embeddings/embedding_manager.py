import os
import requests

from enum import Enum
from typing import List


class EmbeddingTypes(str, Enum):
    SYMMETRIC = 'symmetric'
    ASYMMETRIC = 'asymmetric'


class EmbeddingsManager:

    def __init__(self):
        self.embedding_endpoint = os.environ.get(
            'EMBEDDING_GENERATOR_ENDPOINT',
            'http://embeddings-generator:8000/embedding'
        )

    def get_embeddings_for_text(self, text: str,
                                embedding_type: EmbeddingTypes) -> List[float]:
        response = requests.post(
            self.embedding_endpoint,
            json={'text': text, 'type': embedding_type}
        )
        return response.json()['embedding']
