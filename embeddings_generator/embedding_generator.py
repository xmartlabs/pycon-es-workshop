import os
import numpy as np
from enum import Enum

from sentence_transformers import SentenceTransformer

embeddings_generator_path = os.environ.get('EMBEDDINGS_GENERATOR_PATH')
symmetric_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2',
                                      cache_folder=embeddings_generator_path)
asymmetric_model = SentenceTransformer('sentence-transformers/msmarco-bert-base-dot-v5',
                                       cache_folder=embeddings_generator_path)


class EmbeddingTypes(Enum):
    SYMMETRIC = 'symmetric'
    ASYMMETRIC = 'asymmetric'


class EmbeddingsManager:

    def get_embedding_sbert(self, text, search_type: EmbeddingTypes = EmbeddingTypes.SYMMETRIC):
        if search_type == EmbeddingTypes.SYMMETRIC:
            return symmetric_model.encode(text).tolist()
        elif search_type == EmbeddingTypes.ASYMMETRIC:
            v = asymmetric_model.encode(text)
            normalized_v = v/np.linalg.norm(v)
            return normalized_v.tolist()
        else:
            raise NotImplementedError
